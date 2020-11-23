"""
Installs the mqml package
"""

from setuptools import setup, find_packages
from pathlib import Path

import versioneer

readme_file_path = Path(__file__).absolute().parent / "README.md"

required_packages = [
    'opencensus-ext-azure',
    'qcodes'
]

package_data = {"mqml": ["conf/telemetry.ini"] }


setup(
    name="mqml",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    python_requires=">=3.7",
    install_requires=required_packages,
    author= "Farzad Bonabi",
    author_email="farzadb58@gmail.com",
    description="Package required to easily run measurements and analysis for the Microsoft Quantum Materials Lyngby lab. The source codes do not include Microsoft IP and are open source, so these packages could be generally useable.",
    long_description=readme_file_path.open().read(),
    long_description_content_type="text/markdown",
    license="MIT",
    package_data=package_data,
    packages=find_packages(exclude=["*.tests", "*.tests.*"]),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
    ],
)
