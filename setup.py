from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yandex-music-downloader",
    version="0.2.0",
    author="Igor Dronnikov",
    author_email="dronnikovigor@gmail.com",
    description="A Python library for downloading music from Yandex Music with metadata support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dronnikovigor/yandex-music-downloader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "yandex-music>=2.0.0",
        "mutagen>=1.47.0",
        "requests>=2.32.4",
        "pycryptodomex>=3.23.0",
        "strenum>=0.4.15",
        "pycryptodome>=3.23.0",
    ],
    entry_points={
        "console_scripts": [
            "yandex-music-downloader=ymd.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/dronnikovigor/yandex-music-downloader/issues",
        "Source": "https://github.com/dronnikovigor/yandex-music-downloader",
    },
)
