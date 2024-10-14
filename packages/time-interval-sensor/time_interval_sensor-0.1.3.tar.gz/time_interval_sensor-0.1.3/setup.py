# setup.py
from setuptools import setup, find_packages

# Read the README file content
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='time_interval_sensor',
    version='0.1.3',
    description='A custom Airflow sensor to check if the current time is within a specific interval and time zone.',
    author='Hrishikesh Tiwari',
    long_description=long_description,  # Use README.md for the long description
    long_description_content_type='text/markdown',  # Specify the content type as Markdown
    author_email='htiwari1@gmail.com',
    packages=find_packages(),
    install_requires=[
        'apache-airflow>=2.0.0',
        'pytz'
    ],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
