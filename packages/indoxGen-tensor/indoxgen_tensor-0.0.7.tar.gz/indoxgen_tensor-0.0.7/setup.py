from setuptools import setup, find_packages
import os

# Get the absolute path of the current file
here = os.path.abspath(os.path.dirname(__file__))

# Read the requirements file
with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

# Read the README file for the long description
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='indoxGen-tensor',
    version='0.0.7',  # Increment the version number
    license='AGPL-3.0-or-later',
    packages=find_packages(include=['indoxGen_tensor', 'indoxGen_tensor.*']),
    package_data={
        'indoxGen_tensor': ['*', '**/*'],
    },
    include_package_data=True,
    description='Indox Synthetic Data Generation (GAN-tensorflow)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='nerdstudio',
    author_email='ashkan@nematifamilyfundation.onmicrosoft.com',
    url='https://github.com/osllmai/IndoxGen/tree/master/libs/indoxGen_tensor',
    keywords=[
        'AI', 'deep learning', 'language models', 'synthetic data generation',
        'machine learning', 'NLP', 'GAN', 'tensorflow'
    ],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.9',
)