from setuptools import setup, find_packages

setup(
    name='roundr',
    version='1.2',
    packages=find_packages(),
    py_modules=['roundr'],
    description='Round Number',
    author='Reza Abbaszadeh',
    author_email='rezaabbaszadehlinkedin@gmail.com',
    url='https://github.com/RezaAbbaszadeh80/roundr',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
