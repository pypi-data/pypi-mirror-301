from setuptools import setup, find_packages

setup(
    name='papatool',  # The name of your package
    version='0.1.0',
    description='A package tool for managing Python packages',
    author='Wasit Limprasert',
    author_email='wasit7@gmail.com',
    url='https://github.com/wasit7/package-tool',  # Your GitHub repository URL
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'papatool=papatool.papatool:main',  # CLI command to run the tool
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[  # Add any required dependencies here
        'setuptools',
        'wheel',
        'twine'
    ],
)
