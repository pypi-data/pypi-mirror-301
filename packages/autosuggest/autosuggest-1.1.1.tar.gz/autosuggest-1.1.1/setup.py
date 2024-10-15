from setuptools import setup, find_packages


# Read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='autosuggest',
    version='1.1.1',
    packages=find_packages(),
    description='A cross-platform auto-suggest input package with enhanced features',
    author='Ishan OShada',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='ic31908@gmail.com',
    url='https://github.com/ishanoshada/autosuggest',  # Update with your actual GitHub repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
