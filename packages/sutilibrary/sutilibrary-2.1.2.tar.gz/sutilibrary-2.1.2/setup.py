from setuptools import setup, find_packages

setup(
    name="sutilibrary",
    version="2.1.2",
    author="Your Name",
    author_email="firi8228@gmail.com",
    description="A comprehensive collection of algorithms including sorting, searching, graph algorithms, and more",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "prettytable>=2.0.0",
        "pygments>=2.7.0",
        "networkx>=3.4.1",
        "matplotlib>=3.9.1.post1"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "flake8>=3.9",
            "black>=21.5b1",
        ],
    },
    entry_points={
        "console_scripts": [
            "sort-algo=your_package.sorting.sorting_algorithms:main",
            "search-algo=your_package.searching.searching_algorithms:main",
            "graph-algo=your_package.graph.graph_algorithms:main",
            "other-algo=your_package.other.other_algorithms:main",
        ],
    },
)