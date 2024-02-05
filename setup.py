from setuptools import setup, find_packages

setup(
    name='small_tools',
    version='0.1',
    author='Jiaxin Li',
    author_email='jil4025@med.cornell.edu',
    description='Some practical tools',
    packages=find_packages(),
    install_requires=['numpy',
                      'requests',
                      'pygenometracks',
                      'mygene==3.2.2'
                     ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8'
)