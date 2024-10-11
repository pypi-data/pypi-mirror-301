from setuptools import setup, find_packages

setup(
    name="grupob_zoho",
    version="0.1.1",
    author="Gelson Júnior",
    author_email="gelson.junior@grupobachega.com.br",
    description="Uma biblioteca para manipular dados no zoho",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/juniorppp/zoho",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
