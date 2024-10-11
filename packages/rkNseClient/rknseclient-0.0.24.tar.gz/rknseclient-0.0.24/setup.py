from setuptools import setup, find_packages

setup(
    name="rkNseClient",
    version="0.0.24",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["pandas==2.2.3", "requests==2.32.3"],
    author="kamalkavin96",
    author_email="kamalkavin68@gmail.com",
    description="Python package for Nse Data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kamalkavin68/rkNseClient",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)