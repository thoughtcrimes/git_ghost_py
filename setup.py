from setuptools import setup

setup(
    name='git_ghost',
    version='0.1.0',    
    description='A example Python package',
    url='https://github.com/D6AD3C/git_ghost_py',
    author='',
    author_email='',
    license='MIT',
    packages=['git_ghost'],
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'git-ghost=git_ghost.__main__:cli',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)