from setuptools import setup

setup(
    name='lyrics',
    version='0.0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
    entry_points={
        'console_scripts': [
            'lyrics = lyrics.cli:main',
        ]
    }
)
