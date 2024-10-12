from setuptools import setup, find_packages

setup(
    name='pipewizard',
    version='0.0.1',
    packages=find_packages(), 
    entry_points={
        'console_scripts': [
            'pipewizard=pipewizard.main:main',
        ],
    },
    description='A tool to help generate GitHub pipelines for Python projects',
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown', 
    author='atxpaul',
    author_email='',
    url='https://github.com/atxpaul/pipewizard', 
    classifiers=[ 
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10', 
    install_requires=[
        'questionary',
        'rich'
    ],
)
