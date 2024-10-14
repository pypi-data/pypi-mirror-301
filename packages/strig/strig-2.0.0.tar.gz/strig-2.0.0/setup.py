import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strig",
    version="v2.0.0",
    author="Wibo Kuipers",
    author_email="wkuipersoss@gmail.com",
    description="A simple and intuitive Python package for generating random strings and numbers. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/w-kuipers/strig",
    project_urls={
        "Bug Tracker": "https://github.com/w-kuipers/strig/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
