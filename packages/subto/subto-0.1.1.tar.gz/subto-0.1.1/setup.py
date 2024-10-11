import setuptools

long_description = '''
`subto` is a package to make life easier when submitting jobs to schedulers\n\n

Please see the `subto` documentation for more details.
'''

# DO NOT EDIT THIS NUMBER!
# IT IS AUTOMATICALLY CHANGED BY python-semantic-release
__version__ = '0.1.1'

setuptools.setup(
    name='subto',
    version=__version__,
    author='Jon Kragskow',
    author_email='jgck20@bath.ac.uk',
    description='A package to make life easier when submitting jobs to schedulers', # noqa
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/kragskow-group/subto',
    project_urls={
        'Bug Tracker': 'https://gitlab.com/kragskow-group/subto/issues',
        'Documentation': 'https://www.kragskow.dev/subto/index.html'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    package_dir={'': '.'},
    packages=setuptools.find_packages(),
    python_requires='>=3.12',
    install_requires=[
        'xyz_py>=5.13.0'
    ],
    entry_points={
        'console_scripts': [
            'subto = subto.cli:interface',
        ]
    }
)
