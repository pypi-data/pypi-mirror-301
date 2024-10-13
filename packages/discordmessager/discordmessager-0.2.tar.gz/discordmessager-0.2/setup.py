from setuptools import setup, find_packages

setup(
    name='discordmessager',  
    version='0.2',  
    packages=find_packages(),  
    install_requires=[
        'requests',  
        'pycryptodome',
    ],
    entry_points={
        'console_scripts': [
            'discordmessager=discordmessager.discordmessager:main',  
        ],
    },
    description='DiscordMessager 1.0.0',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    author='John',  
    classifiers=[
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],
    python_requires='>=3.6',  
)
