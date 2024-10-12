from setuptools import setup, find_packages

setup(
    name='tureng_api',
    version='0.0.1',
    description='A simple wrapper for the Tureng dictionary API',
    author='ramazan',
    author_email='mramazantrn28@gmail.com',
    url='https://github.com/MRamazan/turengAPI',
    packages=find_packages(),
    long_description=open('README.md').read(),  # Add your README here
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
