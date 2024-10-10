from . import QCClient

class QCConfig(dict):

    def __init__(self,
                 qcclient: QCClient = None,
                 qc_job_type: str = 'sp',
                 **kwargs):
        self.qc_job_type = qc_job_type
        super().__init__()

        if qcclient is None:
            self.qcclient = QCClient()
        else:
            self.qcclient = qcclient

        self.template = self._get_template(qc_job_type)
        self.update(self.template)
        self.update(kwargs)

    def _get_template(self, qc_job_type) -> dict:
        data = self.qcclient.get_job_config(qc_job_type)
        return data

    def get_configurable_options(self, default=type(None)):
        '''
        return configurable keys and types
        '''
        def get_dict_types(data):
            key_types = {}
            for key, value in data.items():
                if value is None:
                    key_types[key] = default
                elif isinstance(value, dict):
                    key_types[key] = get_dict_types(value)
                else:
                    key_types[key] = type(value)
            return key_types
        return get_dict_types(self.template)
