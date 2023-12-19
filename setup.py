from setuptools import find_packages, setup

setup(
    name="PyRedis",
    version="0.0.1",
    description="Python implementation of Redis server",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyredis = pyredis.main:start_server'
        ]
    },
)
