from setuptools import setup, find_packages

setup(
    name="mindframe",
    version="0.1.0",
    description="A Python package for the Mindframe project",
    author="Ben Whalley",
    author_email="ben.whalley@plymouth.ac.uk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
