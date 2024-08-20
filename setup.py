from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Text based adventure player'
LONG_DESCRIPTION = 'A text base game player'

setup(
    name="Adventure Player",
    version=VERSION,
    author="Jules Graus",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['Jules', 'Adventure Player'],
    classifiers=[
        "Development Status :: Alpha",
        "Intended Audience :: Retro gamers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)