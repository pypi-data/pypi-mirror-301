from setuptools import setup, find_packages

setup(
    name="BR-Logs",  # Replace with your module name
    version="0.5.0",  # Initial version
    packages=find_packages(),
    install_requires=[
    'aiohappyeyeballs==2.4.2',
    'aiohttp==3.9.0',
    'aiosignal==1.3.1',
    'attrs==24.2.0',
    'frozenlist==1.4.1',
    'idna==3.10',
    'multidict==6.1.0',
    'yarl==1.13.0',
    'pytz==2024.2'
    
],
    author="Amir Sakov",
    author_email="volturisalts@gmail.com",
    description="A wrapper for the BR-Logs API.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sak0v/BR-Logs",  # GitHub repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # Specify the supported Python versions
)
