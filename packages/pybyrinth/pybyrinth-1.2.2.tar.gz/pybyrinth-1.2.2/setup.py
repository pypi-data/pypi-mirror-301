# setup.py

from setuptools import setup

from setuptools import setup

setup(
    name='pybyrinth',  
    version='1.2.2',  
    description="A Python library for creating, solving, and visualizing mazes using Depth-First Search (DFS) and Breadth-First Search (BFS) algorithms.",
    long_description=open('README.md', encoding='utf-8').read(),  
    long_description_content_type='text/markdown',  
    author='Pablo Álvaro Hidalgo',  
    author_email='palvaroh2000@gmail.com',  
    license='MIT',  
    py_modules=['pybyrinth'], 
    install_requires=[
        'numpy==1.23.5',
        'matplotlib==3.6.2'
    ],  
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent', 
    ],
    python_requires='>=3.6',  
    keywords='maze, labyrinth, pathfinding, search, DFS, BFS', 
    url='https://github.com/pabblo2000/pybyrinth',  
)

# Para subir la librería a PyPI, ejecuta el siguiente comando en la terminal:
# python setup.py sdist 

# Luego, ejecuta el siguiente comando en la terminal:
# twine upload --repository pynacci dist/*