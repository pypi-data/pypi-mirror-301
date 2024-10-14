from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

# Specify the relative path to your actual package directory
package_dir = os.path.join('protos', 'mgmt', 'v1alpha1')


setup(
    name='neosync',  # Replace with your actual package name
    version='0.4.78',
    package_dir={'': package_dir},
    packages=find_packages(where=package_dir),
    include_package_data=True,
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