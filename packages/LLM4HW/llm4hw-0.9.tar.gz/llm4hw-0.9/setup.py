from setuptools import setup, find_packages

setup(
    name='LLM4HW',
    version='0.9',
    packages=find_packages(),
    include_package_data=True,  # Ensures MANIFEST.in is used to include files
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
    package_data={
        '': ['*.env', '*.tcl', '*.md'],
    },
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
