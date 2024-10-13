from setuptools import setup, find_packages

setup(
    name='VoidHangman',
    version='0.1.1',
    author='Void',
    author_email='voidfy948@gmail.com',
    description='A simple Hangman game module for Discord bots',
    long_description=open('Readme.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/voidfy69/Hangman-Module.git',
    packages=find_packages(),  # Automatically find packages in your project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
