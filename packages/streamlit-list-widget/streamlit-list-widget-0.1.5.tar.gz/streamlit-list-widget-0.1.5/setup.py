from pathlib import Path
import toml  # Add this import

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read version from pyproject.toml
pyproject = toml.load(this_directory / "pyproject.toml")  # Add this line
version = pyproject['tool']['poetry']['version']  # Add this line

setuptools.setup(
    name="streamlit-list-widget",
    version=version,  # Update this line
    author="Marco Sanguineti",
    author_email="marco.sanguineti.info@gmail.com",
    description="Streamlit component that allows you to do handle a list of clickable items",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
    extras_require={
        "devel": [
            "wheel",
            "pytest==7.4.0",
            "playwright==1.39.0",
            "requests==2.31.0",
            "pytest-playwright-snapshot==1.0",
            "pytest-rerunfailures==12.0",
        ]
    }
)
