import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="belousov-zhabotinsky",
    version="0.7.0",
    author="Lucas Stefan Minuzzi Neumann",
    author_email="neumannmlucas@gmail.com",
    description="Simulation of the Belousov-Zhabotinski reaction with ASCII characters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neumann-mlucas/belousov-zhabotinsky",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["belousov-zhabotinsky=belousov_zhabotinsky.render:main"]
    },
    python_requires=">=3",
    install_requires=["numpy", "scipy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
