from setuptools import setup, find_packages

setup(
    name='criteria_performance',  # Nom du package
    version='0.0.1',  # Version initiale
    description='A Python package for performance criteria visualization',  # Courte description
    long_description=open("README.md").read(),  # Description longue à partir du README.md
    long_description_content_type='text/markdown',  # Le format de description longue (ici, Markdown)
    url='https://github.com/teach-genius/aryad.git',  # Lien vers ton dépôt GitHub
    author="Olanda-Eyiba Chantry",
    author_email='chantryolanda85@gmail.com',
    license='MIT',  # Choix de la licence
    packages=find_packages(where="."),  # Trouve tous les packages à partir du répertoire courant
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib'
    ],  # Liste des dépendances
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Version minimale de Python
)
