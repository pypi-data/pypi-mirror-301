from setuptools import setup, find_packages

setup(
    name='alteryse-py',
    version='0.1.0',
    author='Alteryse',
    author_email='hello@alteryse.cloud',
    description='A Python library for interacting with Alteryse Instances.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/alteryse/alteryse-py',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
