from setuptools import setup, find_packages

setup(
    name='mqManager',  # Name of your library
    version='0.1.13',         # Version of your library
    author='WireDevTeam',
    author_email='sunnepazzy123@gmail.com',
    description='A library for managing RabbitMQ connections and messaging.',
    long_description=open('README.md').read(),  # Read the long description from README.md
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mqManager',  # URL to your project
    packages=find_packages(),  # Automatically find packages
    install_requires=[
        'pika>=1.0.0',  # List your dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
    