import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='format_logger',
    version='0.0.5',
    author='Eloy Chang',
    author_email="echang.epsilondl@gmail.com",
    description='Description.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/echang1802/format-logger",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'normandy = normandy.normandy:run'
        ]
    }
)