from setuptools import setup, find_packages

setup(
        packages=find_packages(),
        install_requires=[
            'click',
            ],
        entry_points={
            'console_scripts': [
                'rsyncer = rsyncer.rsyncer:rsyncer',
                ]
            }
        )


