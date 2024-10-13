from setuptools import setup, find_packages

setup(
    name='uistyle',
    version='0.8.9',
    description='A beautiful console UI system For discord',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ravan',
    author_email='ravanxl@example.com',
    url='https://github.com/vivekxd669/myconsoleui',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'loguru',
        'pyfiglet',
        'rich'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
