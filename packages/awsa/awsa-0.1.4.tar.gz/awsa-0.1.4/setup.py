from setuptools import setup, find_packages

setup(
    name='awsa',
    version='0.1.4',
    description='AISAK-O agent for information collection and summary.',
    author='Mandela Logan',
    author_email='mandelakorilogan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'torch',
        'transformers',
        'beautifulsoup4',
        'edge-tts',
        'nest_asyncio',
        'IPython',                   
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
