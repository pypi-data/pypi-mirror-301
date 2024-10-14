import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpleUID",
    version="v1.1.3",
    author="Wibo Kuipers",
    author_email="wkuipersoss@gmail.com",
    description="A simple and intuitive Python package for generating unique IDs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/w-kuipers/simpleUID",
    project_urls={
        "Bug Tracker": "https://github.com/w-kuipers/simpleUID/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
