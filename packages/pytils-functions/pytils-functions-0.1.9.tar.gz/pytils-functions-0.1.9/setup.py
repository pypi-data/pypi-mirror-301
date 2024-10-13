import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytils-functions",
    version="0.1.9",
    author="Whispered",
    author_email="bluden99@example.com",
    description="Utils for data python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Whisperes/pytils",
    packages=setuptools.find_packages(exclude=("tests.*","docs.*")),
    install_requires=['requests','dill','coloredlogs', 'pytest'],
    # TODO: from pip.req import parse_requirements
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)