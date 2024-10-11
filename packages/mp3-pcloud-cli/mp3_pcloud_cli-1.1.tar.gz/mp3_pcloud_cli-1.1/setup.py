import os
from setuptools import setup, find_packages

readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")

with open(readme_path, "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name='mp3-pcloud-cli',
    version='1.01',
    author='Sam Pomerantz',
    author_email='sam@sampomerantz.me',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mp3-pcloud-cli=module.main:main',
        ],
    },
    install_requires=[
        'requests',
        'yt-dlp',
    ],
)
