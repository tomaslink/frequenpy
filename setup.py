import setuptools

DESCRIPTION = "High-precision physics engine dedicated to the study of standing waves."

setuptools.setup(
    name="frequenpy",
    version="0.2.0",
    author="Tomás Juan Link",
    author_email="tomaslink@gmail.com",
    description=DESCRIPTION,
    url="https://github.com/tomasjuanlink/frequenpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'frequenpy = frequenpy.cli:main',
        ]
    },
    install_requires=[
        'numpy<2',
        'matplotlib<4'
    ]
)
