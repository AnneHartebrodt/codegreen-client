from setuptools import setup

setup(
    name = 'greenerai_client',
    version='0.0.1',
    description='Query the greenerai API',
    py_modules=["client"],
    package_dir={'':'src'}
)