from setuptools import setup, find_packages

setup(
    name='list_search',
    version='0.1.0',
    author='Dmitry Buslov',
    author_email='buslovdmitrij0@gmail.com',
    description='Search in list of dictionaries with lookups! Like in ORM!',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
