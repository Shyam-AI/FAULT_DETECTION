from setuptools import find_packages, setup
from typing import List


def get_requirements()->List[str]:
    requirement_list:List[str] = []
    try:
        req_file = open("requirements.txt")
        file_contents= req_file.read()
        requirement_list= file_contents.splitlines()
    except FileNotFoundError:
        return "Kindly check the file is missing"
    return requirement_list


setup (
    name="topics",
    version="0.0.1",
    author = "Shyam",
    author_email="shyamdl2803@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements(),
)