from setuptools import setup, find_packages
from typing import List
from pathlib import Path

HYPEN_E_DOT='-e .'

def get_requirements(file_path: str) -> List[str]:
    if not Path(file_path).exists():
        return []

    with open(file_path) as file_obj:
        requirements = [req.strip() for req in file_obj.readlines()]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

# ✅ Read README.md contents
long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="ytdl-core",
    version="0.1.0",
    author="Apoorva Saxena",
    description="YouTube video and playlist downloader with CLI and GUI support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "yt-downloader=ytdl_core.main:main",
        ]
    },
    python_requires=">=3.7",
    include_package_data=True,
)