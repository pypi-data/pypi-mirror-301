from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "1.0.2"
DESCRIPTION = "Simple Python package for directly downloading applications from Cafe Bazaar."
LONG_DESCRIPTION = (
    "Simple Python package for directly downloading applications from Cafe Bazaar (cafebazaar.ir)."
)

# Setting up
setup(
    name="Bazaar-Dl",
    version=VERSION,
    author="Matin Baloochestani (Matin-B)",
    author_email="MatiinBaloochestani@Gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=["python", "bazaar_dl", "bazaar-dl", "Cafe-Bazaar"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)