from setuptools import setup, find_packages

setup(
    name='mp3-pcloud-cli',
    version='1.0',
    author='Sam Pomerantz',
    author_email='sam@sampomerantz.me',
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
