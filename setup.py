import os
from setuptools import setup, find_packages


def read(*rnames):
    """Read in file content."""
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name='gocept.remoteleds',
    version='1.4.dev0',
    url='https://github.com/gocept/gocept.remoteleds',
    license='MIT',
    description='Can speak to an Arduino and set color of connected LEDs.',
    author='Daniel Havlik, Florian Pilz and Oliver Zscheyge',
    author_email='dh@gocept.com',
    long_description=(read('README.rst')
                      + '\n\n' +
                      'Detailed Documentation\n'
                      '**********************'
                      + '\n\n' +
                      read('CHANGES.rst')
                      ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: C',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
    ],
    keywords='arduino led adafruit neopixel',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['gocept'],
    include_package_data=True,
    install_requires=[
        'pyserial',
        'requests',
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'pytest',
        ]
    },
    entry_points={
        'console_scripts': [
            'remoteleds = gocept.remoteleds.discovery:entry',
        ]
    },
    zip_safe=False,
)
