from setuptools import setup, find_packages

setup(
    name='algorithmetn',
    version='0.4.3',  # Updated version
    packages=find_packages(),
    description='A package for basic list operations and algorithms.',
    long_description=open('README.md').read(),  # Optional: read from README file
    long_description_content_type='text/markdown',  # Specify the format of long description
    author='Jaballah Karim',
    author_email='lhackerk233@gmail.com',
    license='MIT',  # Specify the license
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)