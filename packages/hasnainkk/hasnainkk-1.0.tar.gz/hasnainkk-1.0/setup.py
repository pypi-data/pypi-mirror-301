from setuptools import setup, find_packages

setup(
    name="hasnainkk",
    version="1.0",
    author="Hasnain Khan",
    author_email="hasnainkk98075@gmail.com",
    description="python font module | Fonts",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "numpy>=1.21.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
