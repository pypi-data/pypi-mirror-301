from setuptools import find_packages, setup

setup(
    name="sqlcrudbase",
    version="0.1.2",
    author="Santiago Palacio Vásquez",
    author_email="keycode.santiago@gmail.com",
    url="https://github.com/N3VERS4YDIE/sqlcrudbase-py-lib",
    description="Python library to simplify the creation of CRUD operations in FastAPI applications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="sql crud base peewee fastapi pydantic",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pydantic",
        "peewee",
    ],
)
