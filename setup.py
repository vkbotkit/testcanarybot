import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "testcanarybot",
    version = '01.00.003',
    author = "andprokofieff",
    author_email = "prokofieff@internet.ru",
    description = "asynchronous VK Bot Framework",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/kensoi/testcanarybot/",
    packages = setuptools.find_packages(exclude = ('assets', 'assets.*', 'examples', 'examples.*', 'library', 'library.*', 'modules', 'modules.*')),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ["aiohttp"],
    python_requires = '>=3.7',
)
