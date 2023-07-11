from setuptools import find_packages,setup
from typing import List,Tuple, Set

def get_requirements(file_path:str)->List[str]:

    """
    This fuction takes in file as input and gives output as list of content
    """
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [elements.replace("\n","") for elements in requirements]

    if "-e ." in requirements:
        requirements.remove("-e .")
        
    return requirements

setup(
    name='MLProject',
    version="0.0.1",
    author='Ramesh',
    author_email='vhanamaneramesh@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)