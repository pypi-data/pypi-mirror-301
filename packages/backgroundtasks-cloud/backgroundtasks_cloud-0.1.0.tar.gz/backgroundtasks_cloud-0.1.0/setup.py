from setuptools import setup, find_packages

setup(
    name="backgroundtasks_cloud",
    version="0.1.0",
    author="Simeon Emanuilov",
    author_email="simeon.emanuilov@gmail.com",
    description="A package for running background tasks in Python applications",
    url="https://github.com/s-emanuilov/backgroundtasks",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)