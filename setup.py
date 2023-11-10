import setuptools

from frequenpy.constants import APP_DESCRIPTION
from frequenpy.version import __version__

setuptools.setup(
    name="frequenpy",
    version=__version__,
    author="Tomás Juan Link",
    author_email="tomaslink@gmail.com",
    description=APP_DESCRIPTION,
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
