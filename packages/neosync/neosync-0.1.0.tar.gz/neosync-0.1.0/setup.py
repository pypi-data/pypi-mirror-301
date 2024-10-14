from setuptools import setup, find_packages

setup(
    name='neosync',
    version='0.1.0',  # This will be updated automatically in the CI/CD pipeline
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='Evis Drenova',
    author_email='evis@neosync.dev',
    description='Neosync Python SDK',
    url='https://github.com/nucleuscloud/neosync',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)