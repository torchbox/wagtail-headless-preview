from os import path

from setuptools import find_packages, setup

from src.wagtail_headless_preview import __version__


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="wagtail-headless-preview",
    version=__version__,
    description="Enhance Wagtail previews in headless setups.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dan Braghis",
    author_email="dan.braghis@torchbox.com",
    url="https://github.com/torchbox/wagtail-headless-preview",
    project_urls={
        "Changelog": "https://github.com/torchbox/wagtail-headless-preview/blob/main/CHANGELOG.md",  # noqa:B950 E501
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    license="BSD",
    python_requires=">=3.8",
    install_requires=["wagtail>=4.1"],
    extras_require={"testing": ["tox", "django-cors-headers"]},
    keywords=["wagtail", "django", "headless"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 4",
        "Framework :: Wagtail :: 5",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
