from setuptools import setup, find_packages
from preptools.version import __version__

with open("requirements.txt") as requirements:
    requires = list(requirements)

extras_requires = {
    'tests': ['pytest~=6.2.5']
}

setup_options = {
    'name': 'preptools',
    'version': __version__,
    'description': 'P-Rep management command line interface',
    'author': 'ICON Foundation',
    'author_email': 'foo@icon.foundation',
    'packages': find_packages(exclude=['tests*', 'docs']),
    'url': 'https://github.com/icon-project/preptools',
    'long_description_content_type': 'text/markdown',
    'long_description': open('README.md').read(),
    'include_package_data': True,
    'py_modules': ['preptools'],
    'python_requires': '>=3.7',
    'license': "Apache License 2.0",
    'install_requires': requires,
    'extras_require': extras_requires,
    'test_suite': 'tests',
    'entry_points': {
        'console_scripts': [
            'preptools=preptools:main'
        ],
    },
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
}

setup(**setup_options)
