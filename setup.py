import setuptools

with open("README.md", "r") as fh:
    long_description = fh.readlines()[3]

setuptools.setup(
    name="frequenpy",
    version="0.2.0",
    author="Tomás Juan Link",
    author_email="tomaslink@gmail.com",
    description="Physics engine for standing waves",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomasjuanlink/frequenpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'frequenpy = frequenpy.cli:main',
        ]
    },
    install_requires=['numpy==1.22.0', 'matplotlib==3.0.2']
)
