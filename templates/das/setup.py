from setuptools import setup, find_packages

from pathlib import Path

HERE = Path(__file__).parent
long_description = (HERE / "README.md").read_text()

requirements = [
    "nodejs",
    "flask",
    "flask-cors",
]

setup(
    name="das",
    version="0.0.1",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # license="MIT",
    author="Joel Stansbury",
    author_email="stansbury.joel@gmail.com",
    url="https://github.com/JoelStansbury/das",
    packages=find_packages(),
    install_requires=requirements,
    # include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
