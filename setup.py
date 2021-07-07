from setuptools import setup

requires = [
    'aiohttp>=3.7.4',
    'beautifulsoup4>=4.9.3'
]

test_requirements = [
    'pytest-mock>=3.5.1',
    'pytest>=6.2.2',
    'pytest-asyncio>=0.14.0'
]

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
   name='urchintai-client',
   version='1.0.0',
   description='Client to call UR Chintai API (UR都市機構)',
   author='Nguyen Thai Duong',
   author_email='duongnt.bk@gmail.com',
   long_description=long_description,
   long_description_content_type='text/markdown',
   url='https://github.com/duongntbk/urchintai-client',
   packages=['urchintai_client'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
   install_requires=requires,
   tests_require=test_requirements,
)
