from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cerina",
    version="0.2.8",
    description='Next-gen Sync & Async AI agents with 100+ functionalities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "nest_asyncio",
        "requests",
        "pytest",
        "webdriver-manager",
        "selenium",
    ],
)