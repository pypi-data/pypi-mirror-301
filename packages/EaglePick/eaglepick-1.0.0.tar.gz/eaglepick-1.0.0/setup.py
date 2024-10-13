from setuptools import setup, find_packages

setup(
    name='EaglePick',
    version='1.0.0',
    description='Human-readable programming language for web, mobile, and backend applications',
    author='Qudus Nafiu Olarenwaju',
    author_email='qudus@amatip.co.uk',
    Company='Amatip IT',
    url='https://github.com/QudusApp/EaglePick',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
        'spacy',
        'react-native',
        'Jinja2'
    ],
    entry_points={
        'console_scripts': [
            'eaglepick = eaglepick_cli:main',  # This allows users to run EaglePick from the terminal
        ],
    },
)
