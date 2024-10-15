from setuptools import setup, find_packages

setup(
    name='roborregos-metrics-client',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'roborregos-metrics-worker = src.worker.worker:main',
        ]
    }
)
