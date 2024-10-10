import json, yaml
import logging
import os
import time
import requests
import boto3
from botocore.client import Config
logger = logging.getLogger(__name__)

QC_URL_PREFIX = "http://180.184.99.163/byteqc/api/v1/"
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BUCKET_NAME = 'byteqc-public'

invoc_id = 1784
queue_id = 1875

def to_pretty_string(input_dict, prefix="  ", title='Index'):

    def to_pretty_string_list(input_dict, prefix=""):
        lines = []
        if isinstance(input_dict, list):
            for i, item in enumerate(input_dict):
                if isinstance(item, dict):
                    lines.append(f"{prefix}{i}:")
                    lines.extend(to_pretty_string_list(item, prefix + "  "))
                else:
                    lines.append(f"{prefix}{i}: {item}")
            return lines
        elif isinstance(input_dict, dict):
            for key, value in input_dict.items():
                if isinstance(value, dict):
                    lines.append(f"{prefix}{key}:")
                    lines.extend(to_pretty_string_list(value, prefix + "- "))
                else:
                    lines.append(f"{prefix}{key}: {value}")
            return lines
        else:
            return [f"{prefix}{input_dict}"]

    return title + "\n" + "\n".join(to_pretty_string_list(input_dict, prefix))


def request_get_list(url, params=None, headers=None, timeout=10, page_size=100):
    if params is None:
        params = {}
    ret = []
    page = 1
    while True:
        resp = requests.get(url,
                            params={
                                **params, "page": page,
                                "page_size": page_size
                            },
                            headers=headers,
                            timeout=timeout)
        resp.raise_for_status()
        data = resp.json().get('data')

        if not data:
            break
        elif not isinstance(data, list):
            return data

        ret.extend(data)
        page += 1

    return ret

def upload_folder(s3_client, bucket_name, local_dir, remote_dir):
    """
    Upload an entire folder to an S3 bucket.

    Parameters:
    - s3_client: The Boto3 S3 client.
    - bucket_name: The name of the S3 bucket.
    - local_dir: The local directory containing the files to upload.
    - remote_dir: The S3 "folder" (prefix) where the files will be uploaded (should end with '/').
    """

    # Walk through all files and directories in the local directory
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            # Full local path of the file
            local_file_path = os.path.join(root, file)

            # Compute the relative path and use it as the S3 key (prefix + relative file path)
            relative_path = os.path.relpath(local_file_path, local_dir)
            s3_key = os.path.join(remote_dir, relative_path).replace("\\", "/")  # Replace backslashes for S3 compatibility

            # Upload the file to S3
            s3_client.upload_file(local_file_path, bucket_name, s3_key)
            logger.info(f"Uploaded {local_file_path} to tos://{bucket_name}/{s3_key}")

def download_folder(s3_client, bucket_name, remote_dir, local_dir):
    """
    Download an entire folder from an S3 bucket to a local directory.

    Parameters:
    - s3_client: The Boto3 S3 client.
    - bucket_name: The name of the S3 bucket.
    - remote_dir: The "folder" in the S3 bucket to download (should end with '/').
    - local_dir: The local directory where the folder will be downloaded.
    """

    # Ensure the local directory exists
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # List all objects within the folder (prefix)
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=remote_dir)
    
    # Check if the folder contains any objects
    if 'Contents' not in response:
        logger.error("No files found in the specified folder.")
        return

    # Download each file in the folder
    for obj in response['Contents']:
        # Extract the file key (full path in S3)
        file_key = obj['Key']
        relative_path = file_key[len(remote_dir):].lstrip('/')  # Remove the remote_dir prefix
        local_file_path = os.path.join(local_dir, relative_path)
        
        # If the object key ends with '/', it's a directory, skip it
        if file_key.endswith('/'):
            continue

        # Ensure the local folder structure is created
        local_subdir = os.path.dirname(local_file_path)
        if not os.path.exists(local_subdir):
            os.makedirs(local_subdir)

        # Download the file
        s3_client.download_file(bucket_name, file_key, local_file_path)
        logger.info(f"Downloaded TOS:{bucket_name}/{file_key} to {local_file_path}")

def folder_exists(s3_client, bucket_name, folder_path):
    """
    Check if a folder (prefix) exists in an S3 bucket.

    Parameters:
    - s3_client: The Boto3 S3 client.
    - bucket_name: The name of the S3 bucket.
    - folder_path: The folder (prefix) to check for. Should end with '/' to indicate it's a folder.

    Returns:
    - True if the folder exists, False otherwise.
    """
    # Ensure the folder path ends with '/' to indicate it's a folder
    if not folder_path.endswith('/'):
        folder_path += '/'

    # List objects with the specified prefix (folder path)
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path, MaxKeys=1)

    # If 'Contents' is present in the response, the folder exists
    return 'Contents' in response

def signed_download_folder(qc_server_url, bucket_name, folder_prefix, local_folder):
    # Define the parameters for the API request
    params = {
        'bucket_name': bucket_name, 
        'folder_prefix': folder_prefix, 
        'expiration': 3600  # Optional expiration time in seconds (default is 3600 seconds)
    }

    # Send a GET request to the API to get the pre-signed URLs
    response = requests.get(
        qc_server_url + '/generate_presigned_urls_for_download', 
        params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        presigned_urls = response.json().get('presigned_urls')

        # Create the local folder structure to match S3
        os.makedirs(local_folder, exist_ok=True)

        # Download each file using its pre-signed URL
        for file_info in presigned_urls:
            file_name = file_info['file_name']
            presigned_url = file_info['url']

            # Create local directories to mirror the S3 folder structure
            local_file_path = os.path.join(local_folder, file_name)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            # Download the file
            logger.info(f"Downloading {file_name} from {presigned_url}")
            response = requests.get(presigned_url)

            if response.status_code == 200:
                # Save the file to the local path
                with open(local_file_path, 'wb') as file:
                    file.write(response.content)
                logger.info(f"Downloaded {file_name} to {local_file_path}")
            else:
                print(f"Failed to download {file_name}. Status code: {response.status_code}")
    else:
        print(f"Failed to get presigned URLs. Status code: {response.status_code}, Error: {response.text}")


def signed_upload_folder(qc_server_url, bucket_name, folder_prefix, local_folder):
    # Get the list of all files in the local folder
    file_list = []
    for root, dirs, files in os.walk(local_folder):
        for file_name in files:
            # Get the relative file path to maintain folder structure
            relative_path = os.path.relpath(os.path.join(root, file_name), local_folder)
            file_list.append(relative_path)

    # Send a POST request to the API with the folder path and file list
    response = requests.post(
        qc_server_url+'/generate_presigned_urls_for_upload',
        json={
            'bucket_name': bucket_name,
            'folder_prefix': folder_prefix,
            'file_list': file_list,
            'expiration': 3600  # Optional: Expiration time for the URLs in seconds
        })

    # Check if the request was successful
    if response.status_code == 200:
        presigned_urls = response.json().get('presigned_urls')

        # Iterate through the pre-signed URLs and upload each file
        for file_name, presigned_url in presigned_urls.items():
            # Construct the full path to the file
            local_file_path = os.path.join(local_folder, file_name)

            # Read the file and upload it using the pre-signed URL
            with open(local_file_path, 'rb') as file_data:
                logger.info(f"Uploading {file_name} to S3...")
                upload_response = requests.put(presigned_url, data=file_data)

                # Check if the upload was successful
                if upload_response.status_code == 200:
                    logger.info(f"Successfully uploaded {file_name}")
                else:
                    print(f"Failed to upload {file_name}. Status code: {upload_response.status_code}, Error: {upload_response.text}")
    else:
        print(f"Failed to generate presigned URLs. Status code: {response.status_code}, Error: {response.text}")


def split_path(path):
    ''' split path into Bucket Name and Path
    e.g. tos:byteqc-public/folder -> byteqc-public, folder name
    '''
    return path.split(':')[1].split('/',1)

class QCClient:

    displayed_meta = {
        "id": 4,
        "name": 32,
        "job_type": 10,
        "status": 10,
        "created_at": 20,
        "updated_at": 20,
        "finished_at": 20,
        "task_summary": None
    }

    def __init__(self,
                 s3_client=None,
                 s3_bucket_name="byteqc-public",
                 url_prefix=QC_URL_PREFIX,
                 timeout=10,
                 headers=None,
                 username=None,
                 is_submitter=False):

        self.url_prefix = url_prefix
        self.timeout = timeout

        self.s3_client = s3_client
        self.s3_bucket_name = s3_bucket_name
        self.tos_prefix = 'tos:' + s3_bucket_name
        self.username = username
        if username is None:
            import socket
            self.username = socket.gethostname()

        self.is_submitter = is_submitter

        if headers is None:
            self.headers = {"Content-Type": "application/json"}
        else:
            self.headers = headers

    def submit(self, data={}, check=True):
        ''' Submit with job data '''

        data["username"] = self.username
        data["invoc_id"] = invoc_id
        data["queue_id"] = queue_id
        label = data['name']

        if check:
            logger.info(f"Checking submit for {label}")
            print(to_pretty_string(data))

            if not input("Submit? [y/N] ").lower() == 'y':
                logger.warning("Aborted")

        logger.info("Submitting job to server")
        resp = requests.post(f"{self.url_prefix}/jobs/", json=data, headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()

        # Check if the response data label matches the input label
        response_label = resp.json().get('data', {}).get('name')
        if response_label != label:
            raise ValueError(f"Response label {response_label} does not match input label {label}")

        logger.debug("Job submitted successfully in response to server")
        job_id = self.get_job_by_label(label).get('id')
        logger.info(f"Job submitted successfully with ID {job_id}")
        return resp.json()  # Return the JSON response

    def _job_data_to_line(self, job_data: dict = None, displayed_meta=None, header=False) -> str:
        if displayed_meta is None:
            displayed_meta = self.displayed_meta

        line = ""

        if header:
            for key, width in displayed_meta.items():
                if width is None:
                    line += f"{key} | "
                else:
                    line += f"{key:>{width}} | "
        else:
            for key, width in displayed_meta.items():
                if width is None:
                    line += f"{job_data.get(key)} | "
                else:
                    line += f"{job_data.get(key):>{width}} | "

        return line + "\n" + "-" * 150 + "\n"

    def get_job_by_label(self, label):
        resp = requests.get(f"{self.url_prefix}/jobs/",
                            params={"name": label},
                            headers=self.headers,
                            timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json().get('data')
        if len(data) == 0:
            raise ValueError(f"Job with label {label} not found")
        return resp.json().get('data')[0]

    def get_job_data(self, job_id):
        resp = requests.get(f"{self.url_prefix}/jobs/{job_id}", headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json().get('data')

    def get_job(self, job_id):
        return self._job_data_to_line(header=True) + "\n" + self._job_data_to_line(self.get_job_data(job_id))

    def get_job_status(self, job_id):
        return self.get_job_data(job_id).get('status')

    def get_job_summary(self, job_id):
        return self.get_job_data(job_id).get('task_summary')

    def get_tasks(self, job_id):
        data = request_get_list(f"{self.url_prefix}/tasks/",
                                params={"job_id": job_id},
                                headers=self.headers,
                                timeout=self.timeout)
        return data

    def filter_tasks_by_status(self, job_id, status):
        data = request_get_list(f"{self.url_prefix}/tasks/",
                                params={
                                    "job_id": job_id,
                                    "status": status
                                },
                                headers=self.headers,
                                timeout=self.timeout)
        return data

    def get_task_by_id(self, task_id):
        resp = requests.get(f"{self.url_prefix}/tasks/{task_id}", headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json().get('data')

    def get_all_user_jobs_data(self):
        data = request_get_list(f"{self.url_prefix}/jobs/",
                                params={"username": self.username},
                                headers=self.headers,
                                timeout=self.timeout)
        data.sort(key=lambda x: x.get('created_at'), reverse=True)
        return data

    def get_all_user_jobs(self, page_size=10):
        data = self.get_all_user_jobs_data()
        data_str = [self._job_data_to_line(job) for job in data[:page_size]]
        line_str = self._job_data_to_line(header=True) + "\n".join(data_str)
        return line_str

    def get_all_user_jobs_labels(self):
        data = self.get_all_user_jobs_data()
        return [job.get('name') for job in data]

    def get_job_config_list(self):
        config_files = os.listdir(CURRENT_DIR + '/configs/')
        return [filename[:-5] for filename in config_files]

    def get_job_config(self, qc_job_type):
        filename_without_postfix = os.path.join(CURRENT_DIR, 'configs', qc_job_type)
        if os.path.isfile(filename_without_postfix + ".json"):
            filename = filename_without_postfix + ".json"
            filetype = "json"
        elif os.path.isfile(filename_without_postfix + ".yaml"):
            filename = filename_without_postfix + ".yaml"
            filetype = "yaml"
        else:
            raise ValueError(f"Cannot find config file at {filename_without_postfix}.json or .yaml")
        with open(filename) as config_file:
            if filetype == "json":
                config = json.load(config_file)
                config = config[0]
            elif filetype == "yaml":
                config = yaml.safe_load(config_file)
            else:
                raise ValueError(f"Unsupported config file type {filetype}")

        if (qc_job_type.startswith("pysisyphus")):
            assert "driver_name" not in config, "pysisyphus input should not contain a driver_name keyword"
            config["driver_name"] = qc_job_type

        return config

    def wait_finished(self, job_id, timeout=36000, interval=10):
        finished_status = ['succeed', 'failed']
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.get_job_status(job_id) in finished_status:
                return
            logger.debug(f"Waited {time.time() - start_time:.2f}s for job to finish")
            time.sleep(interval)
        raise TimeoutError("Job is not finished within timeout")

    def pull_output(self, job_id=0, local_dir='./', wait_finished=True):
        if wait_finished:
            self.wait_finished(job_id)
        job_data = self.get_job_data(job_id)
        if job_data.get('status') != 'succeed':
            logger.warning(f"Job status is not 'succeed': {job_data.get('status')}")
        remote_url = job_data.get('result_url')
        os.makedirs(local_dir, exist_ok=True)
        remote_dir = remote_url.split('/', 1)[1]
        
        # If S3 Client is None, fall back to the default TOS Bucket
        if self.s3_client is None:
            signed_download_folder(self.url_prefix, BUCKET_NAME, remote_dir, local_dir)
        else:
            download_folder(self.s3_client, self.s3_bucket_name, remote_dir, local_dir)

    def push_input(self, input_dir, label='no_label'):
        '''If the input folder is not TOS/S3, upload the entire folder first'''
        if not input_dir.startswith('tos:'):
            input_target_tos = os.path.join('jobs', label, "input")
            
            # If S3 Client is None, fall back to the default TOS Bucket
            if self.s3_client is None:
                signed_upload_folder(self.url_prefix, BUCKET_NAME, input_target_tos, input_dir)
            else:
                upload_folder(self.s3_client, self.s3_bucket_name, input_dir, input_target_tos)
            logger.info(f"Input pushed to {input_target_tos}")
            input_dir = os.path.join(f'tos:{self.s3_bucket_name}', input_target_tos)
        else:
            bucket_name, folder_path = split_path(input_dir)
            is_exist = folder_exists(self.s3_client, bucket_name, folder_path)
            if not is_exist:
                logger.error(f"{input_dir} is not found in TOS Bucket")
        return input_dir
    
    def _retry_job(self, job_id):
        job_data = self.get_job_data()
        # 加入running是为了支持重试job处于running，task没全跑完，但已经有task failed的情况
        assert job_data.get('status') in ['failed', 'running'], f"Job is {job_data.get('status')}"
        job_update_data = {"status": "retrying"}
        resp = requests.put(f"{self.url_prefix}/jobs/{job_id}",
                            json=job_update_data,
                            headers=self.headers,
                            timeout=self.timeout)
        resp.raise_for_status()

    def retry_tasks(self, task_ids):
        for task_id in task_ids:
            task_data = self.get_task_by_id(task_id)
            #assert task_data.get('job_id') == self.job_id, f"Task {task_id} is not in job {self.job_id}"
            if task_data.get('status') != 'failed':
                logger.warning(f"Task {task_id} status is not 'failed': {task_data.get('status')}")

            task_update_data = {"status": "retrying"}
            resp = requests.put(f"{self.url_prefix}/tasks/{task_id}",
                                json=task_update_data,
                                headers=self.headers,
                                timeout=self.timeout)
            resp.raise_for_status()
            job_id = task_data.get('job_id')
        self._retry_job(job_id)
        logger.info(f"Retried {len(task_ids)} tasks")

    def retry_failed(self):
        job_data = self.get_job_data()
        if job_data.get('status') != 'failed':
            logger.warning(f"Job status is not 'failed': {job_data.get('status')}")
        failed_tasks = self.filter_tasks_by_status('failed')
        task_ids = [task.get('id') for task in failed_tasks]
        self.retry_tasks(task_ids)

    def stop_job(self, job_id):
        job_data = self.get_job_data()
        if job_data.get('status') not in ['running']:
            logger.warning(f"Job status is not 'running': {job_data.get('status')}")
        job_update_data = {"status": "stop"}
        resp = requests.put(f"{self.url_prefix}/jobs/{job_id}",
                            json=job_update_data,
                            headers=self.headers,
                            timeout=self.timeout)
        resp.raise_for_status()
        logger.info("Job is stopping")
