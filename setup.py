from os import path

from setuptools import find_packages, setup

from wagtail_headless_preview import __version__


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="wagtail-headless-preview",
    version=__version__,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    description="Wagtail previews in headless mode.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/torchbox/wagtail-headless-preview",
    author="Matthew Westcott - POC, Karl Hobley",
    author_email="matthew.westcott@torchbox.com",
    license="BSD",
    install_requires=["wagtail>=2.0"],
    extras_require={"testing": ["tox", "django-cors-headers"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
