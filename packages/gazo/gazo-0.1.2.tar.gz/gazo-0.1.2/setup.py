from setuptools import setup, find_packages

setup(
    name="gazo",
    version="0.1.2",
    description="A CLI application to display image files in the terminal.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="suzukitakac",
    author_email="suzukitakac@outlook.jp",
    url="https://github.com/suzukitakac/gazo",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pillow",
    ],
    entry_points={
        "console_scripts": [
            "gazo=gazo.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
    ],
    python_requires=">=3.6",
)