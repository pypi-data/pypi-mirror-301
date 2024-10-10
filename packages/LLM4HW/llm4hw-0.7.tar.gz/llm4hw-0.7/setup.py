from setuptools import setup, find_packages

setup(
    name='LLM4HW',
    version='0.7',
    packages=find_packages(),
    install_requires=[
        # List dependencies
        # pip install openai
        # pip install Flask
        # sudo apt-get install python3-tk
        'numpy',
        'openai',
        'Flask',
        # 'python3-tk',
        'requests',
        # python-dotenv
        'python-dotenv',

    ],
    author='Siyu Qiu',
    author_email='siyu.qiu1@unsw.edu.au',
    description='Everything you need to install for the LLM4HW tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/annnnie-qiu/annie_install.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
