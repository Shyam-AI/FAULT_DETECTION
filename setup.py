# from setuptools import find_packages,setup
# from typing import List

# def get_requirements()->List[str]:
#     """
#     This function will return list of requirements
#     """
#     requirement_list:List[str] = []

#     """
#     Write a code to read requirements.txt file and append each requirements in requirement_list variable.
#     """
#     return requirement_list

# setup(
#     name="sensor",
#     version="0.0.1",
#     author="Shyam U",
#     author_email="shyamdl2803@gmail.com",
#     packages = find_packages(),
#     install_requires=get_requirements(),#["pymongo==4.2.0"],
# )

from setuptools import find_packages, setup
from typing import List
# list_of_requirements = [pymongo[srv]==4.2.0,certifi,-e .]

def get_requirements()->List:
    requirement_list:List = []
    try:
        req_file = open("requirements.txt")
        file_contents= req_file.read()
        requirement_list= file_contents.splitlines()
    except FileNotFoundError:
        return "Kindly check the file is missing"
    return requirement_list


setup (
    name="aps_sensor",
    version="0.0.1",
    author = "Shyam",
    author_email="shyamdl2803@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)