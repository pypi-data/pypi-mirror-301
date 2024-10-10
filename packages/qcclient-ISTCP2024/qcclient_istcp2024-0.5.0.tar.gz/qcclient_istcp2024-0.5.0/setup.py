from setuptools import setup

setup(
    name="qcclient-ISTCP2024",
    version="0.5.0",  
    author="Xiaojie Wu",
    author_email="xiaojie.wu@bytedance.com",
    description="This is an experimental client for ISTCP 2024",
    url="",  # URL of the package's homepage or repo
    packages=["qcclient"],  # Only include the 'my_package' folder
    package_dir={"qcclient": "qcclient"},
    package_data={"qcclient": ["configs/*"]},
    include_package_data=True,
    #packages=find_packages(),  # Automatically find and include packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=[
        "boto3",  # List your dependencies
    ],
)
