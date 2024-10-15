# setup.py

from setuptools import setup, find_packages

setup(
    name='TickBox',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'todo-manager=todo_manager.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    author='Abhinav',
    author_email='upstage.barrier_0x@icloud.com',
    description='A terminal-based TO-DO list manager with rich functionality.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/abhinavhooda/todo-manager',
    license='MIT',
)
