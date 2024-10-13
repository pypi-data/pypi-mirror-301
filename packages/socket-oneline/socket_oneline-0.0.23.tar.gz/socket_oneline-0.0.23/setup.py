from pathlib import Path

from setuptools import find_packages
from setuptools import setup

print('     setup: version:  v0.0.23')
print('     setup: module :  socket_oneline')

# @formatter:off
setup(
    description='Client server base class over socket',
    keywords=['socket', 'client server', 'simple'],
    install_requires=[
        'medver-pytest',
        'pytest',
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],

    # common attributes from here on
    name='socket-oneline',
    packages=find_packages(include='./socket_oneline*', ),
    include_package_data=True,
    exclude_package_data={'./socket_oneline/lib': ['.gitignore']},
    version='0.0.23',
    license='MIT',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    author='J. Arrizza',
    author_email='cppgent0@gmail.com',
    url='https://bitbucket.org/arrizza-public/socket-oneline/src/master',
    download_url='https://bitbucket.org/arrizza-public/socket-oneline/get/master.zip',
)
# @formatter:on

print('     setup: done')
