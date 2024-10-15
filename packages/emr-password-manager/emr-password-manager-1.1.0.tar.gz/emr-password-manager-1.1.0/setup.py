from setuptools import setup, find_packages

setup(
    name='emr-password-manager', 
    version='1.1.0', 
    author='Emr', 
    author_email='', 
    description='A simple password manager for generating and validating passwords.', 
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    url='https://github.com/EmrD/python-password-manager-library', 
    packages=find_packages(), 
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)
