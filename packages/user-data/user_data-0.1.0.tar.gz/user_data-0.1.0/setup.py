from setuptools import setup, find_packages

setup(
    name='user_data',
    version='0.1.0',
    author='Aiden Metcalfe',
    author_email='avaartshop@outlook.com',
    description='A package for managing user information and settings on Windows systems.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aidmet/user_data',
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[
        'Programming Language :: Python :: 3',  # Specify the programming language
        'License :: OSI Approved :: MIT License',  # Specify the license
        'Operating System :: OS Independent',  # Specify the operating system
    ],
    python_requires='>=3.11'
)