import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tamo",
    version='0.0.1',
    author="Sabreh Vardas",
    author_email="savrehvardas@gmail.com",
    description="A package for interacting with TAMO",
    include_package_data=True,
    install_requires=[
        'pathlib',
        'python-dotenv',
        'requests',
        'bs4',
        'lxml'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sabrehvardas/tamolib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS independent",
    ]
    # python_requires='>=3.6', I don't know
)
