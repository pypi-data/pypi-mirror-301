from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="multipal",
    version="0.1.0",
    author="Ivan G. Aurelius",
    author_email="ivan.gadingaurelius@gmail.com",
    description="A distributed computing framework for multi-machines over the network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pigman13/multipal",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=[
        "tensorflow==2.6.0",
        "psutil==5.8.0",
        "tqdm==4.62.3",
        "numpy==1.21.2",
        "socket",
        "threading",
        "sqlite3",
        "json",
        "pickle",
    ],
    extras_require={
        "dev": ["pytest", "flake8"],
    },
)
