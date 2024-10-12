from setuptools import setup, find_packages


VERSION = "0.0.11"
DESCRIPTION = "return if 42"
LONG_DESCRIPTION = "A package that returns a boolean if a variable is the number 42"

# Setting up
setup(
    name="isfortytwo",
    version=VERSION,
    author="FLAMIE",
    author_email="<flamiedev1@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
)
