# from setuptools import setup, find_packages

# # Read the README file for the long description
# with open("README.md", "r") as fh:
#     long_description = fh.read()

# setup(
#     name="sumo_simulator",
#     version='0.1.1',  # Incremented version
#     author="Your Name",
#     author_email="your.email@example.com",
#     description="A traffic simulator package for controlling vehicles in SUMO",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/yourusername/sumo_simulator",  # Update with your repository URL
#     packages=find_packages(),
#     install_requires=[
#         # Add 'traci' as an optional dependency
#         "traci; platform_python_implementation == 'CPython'",
#     ],
#     extras_require={
#         "dev": [
#             "pytest>=6.0",
#         ],
#     },
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )
from setuptools import setup, find_packages

setup(
    name='sumo_simulator',
    version='0.1.1',  # Increment the version here
    packages=find_packages(),
    install_requires=[
        'traci',
        # Add other dependencies here if needed
    ],
    entry_points={
        'console_scripts': [
            'sumo_simulator=sumo_simulator:main',  # Update if you have a main function
        ],
    },
)
