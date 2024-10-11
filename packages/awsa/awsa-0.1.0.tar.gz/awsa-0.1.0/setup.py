from setuptools import setup, find_packages

setup(
    name='awsa',
    version='0.1.0',
    description='.',
    author='Mandela Logan',
    author_email='mandelakorilogan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'torch',                   
        'transformers',   
        'requests',                   
        'beautifulsoup4',             
        'edge-tts',
        'playsound',                   
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
