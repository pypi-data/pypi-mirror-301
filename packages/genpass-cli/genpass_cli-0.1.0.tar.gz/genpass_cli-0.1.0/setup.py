from setuptools import setup, find_packages

setup(
    name="genpass-cli",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'pyperclip>=1.8.2',
    ],
    entry_points={
        'console_scripts': [
            'genpass=genpass.core:main',
        ],
    },
    author="tahzeer",
    author_email="tahzeer.work@gmail.com",
    description="A simple yet powerful password generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tahzeer/genpass-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
