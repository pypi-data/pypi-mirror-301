from setuptools import setup, find_packages

setup(
    name='roborregos-metrics-client',
    version='0.0.4',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic'
    ],
    entry_points={
        'console_scripts': [
            'roborregos-metrics-worker = src.worker.worker:main',
        ]
    }
)
