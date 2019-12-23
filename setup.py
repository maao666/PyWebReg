import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

print('Found Package(s): ', setuptools.find_packages())

setuptools.setup(
    name='webreg',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    version='0.2',
    license='Apache License',
    description='Python API for UCI WebReg',
    author='Mason',
    author_email='maao666@icloud.com',
    url='https://github.com/maao666/UCI_WebReg_API',
    download_url='https://github.com/maao666/UCI_WebReg_API/archive/v0.2.tar.gz',
    keywords=['UCI', 'UC Irvine', 'WebReg', 'API', 'bot', 'enrollment'],
    install_requires=[
        'selenium',
        'beautifulsoup4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
