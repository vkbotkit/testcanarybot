import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "testcanarybot",
    version = '1.2.0',
    author = "andprokofieff",
    author_email = "prokofieff@internet.ru",
    description = "asynchronous VK Bot Framework",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/kensoi/testcanarybot/",
    packages = setuptools.find_packages(exclude = ('library', 'library.*', 'docs', 'docs.*', 'kyokou', 'kyokou.*', 'canarybot', 'canarybot.*',  'tildabot', 'tildabot.*', 'tools', 'tools.*')),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ["aiohttp", "six"],
    python_requires = '>=3.7',
)
