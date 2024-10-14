from setuptools import setup, find_packages
from geniux import __version__

setup(
    name="geniux",
    version=__version__,
    description="Библиотека для взаимодействия с Genius.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="thswq",
    author_email="admin@vkmusix.ru",
    url="https://github.com/to4no4sv/geniux",
    packages=find_packages(),
    install_requires=[
        "pytz == 2024.1",
        "httpx == 0.27.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)