from setuptools import setup, find_packages

# Read the contents of your README file for the long description
def read_long_description():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(
    name='GammaJ',
    version='3',
    author='elemenom',
    author_email='pixilreal@gmail.com',
    description='A small lightweight language that combines Python and HTML.',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/elemenom/gammaj',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    entry_points={
        'console_scripts': [
            'gammaj=gammaj.run:run'
        ]
    },
)