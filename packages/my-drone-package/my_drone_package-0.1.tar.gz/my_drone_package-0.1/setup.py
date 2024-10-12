from setuptools import setup, find_packages

setup(
    name="my_drone_package",
    version="0.1",
    description="A package for controlling a drone either via simulation or with a real Tello drone.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bhavya Bipin Gada",
    author_email="bgada1@umbc.edu",
    url="https://github.com/bhavyabgada/drone_teaching_package",
    packages=find_packages(),
    install_requires=[
        "DroneBlocksTelloSimulator",
        "easytello"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
