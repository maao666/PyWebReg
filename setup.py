from distutils.core import setup
setup(
  name = 'webreg',
  packages = ['WebReg'],
  version = '0.2',
  license='Apache License',
  description = 'Python API for UCI WebReg',
  author = 'Mason',
  author_email = 'maao666@icloud.com',
  url = 'https://github.com/maao666/UCI_WebReg_API',
  download_url = 'https://github.com/maao666/UCI_WebReg_API/archive/v0.2.tar.gz',
  keywords = ['UCI', 'UC Irvine', 'WebReg', 'API', 'bot', 'enrollment'],
  install_requires=[
          'selenium',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
