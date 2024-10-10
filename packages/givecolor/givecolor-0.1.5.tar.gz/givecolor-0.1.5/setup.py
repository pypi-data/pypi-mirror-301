from setuptools import setup, find_packages

setup(
    name='givecolor',
    version='0.1.5',
    author='JC-Xander',
    author_email='j.xanderoficial@gmail.com',
    description='Un paquete para imprimir texto de colores en la terminal de Windows',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JC-Xander/GiveColor',

    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
