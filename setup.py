from setuptools import setup, find_packages
import versioneer
from pathlib import Path

here = Path(__file__).parent
long_description = (here / 'README.md').read_text()

setup(
    version=versioneer.get_version(),
    name='dbee',
    description='SQLAlchemy CLI',
    author='mmngreco',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mmngreco/dbee',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,
    python_requires='>=3.5, <4',
    install_requires=[
        "typer",
        "SQLAlchemy",
        "pyodbc",
        "tabulate",
        "rich",
        "sqlparse",
    ],
)
