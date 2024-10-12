from setuptools import setup, find_packages

setup(
    name='datatoolcute',
    version='0.1.1',
    author='Yves Augusto',
    author_email='yvesromero1998@gmail.com',
    description='A short description of your library',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/my_library',
    packages=find_packages(),
    install_requires=[
        # List your library's dependencies here
        'python-Levenshtein>=0.25.1',
        'pandas>=2.2.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)