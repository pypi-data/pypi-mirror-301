from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the README file as long description
README = (HERE / "README.md").read_text()

setup(
    name="random-walk-env", 
    version="0.0.3",  
    author="Falguni Das Shuvo", 
    author_email="dasshuvo7@gmail.com", 
    description="Random Walk Env: A Gymnasium environment for simulating a random walk process.",
    long_description=README,  
    long_description_content_type="text/markdown",  # Specify the content type of the long description
    url="https://github.com/shuvoxcd01/Random-Walk-Env",  # URL to your project (e.g., GitHub repo)
    packages=find_packages(),  # Automatically find and include packages in the project
    classifiers=[
        "Programming Language :: Python :: 3",  # Specify the Python versions supported
        "License :: OSI Approved :: MIT License",  # License for the project
        "Operating System :: OS Independent",  # Operating systems that are compatible
    ],
    python_requires=">=3.6",  # Minimum Python version required
    install_requires=[  # List any dependencies
        "gymnasium",  # Include Gymnasium as a dependency
        "pre-commit",
    ],
)
