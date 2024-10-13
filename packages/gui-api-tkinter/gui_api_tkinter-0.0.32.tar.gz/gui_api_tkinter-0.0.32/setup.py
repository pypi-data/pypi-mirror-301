from pathlib import Path

from setuptools import find_packages
from setuptools import setup

print('     setup: version:  v0.0.32')
print('     setup: module :  gui_api_tkinter')

# @formatter:off
setup(
    description='GUI API for interfacing and testing with tkinter',
    keywords=['gui', 'tkinter', 'test', 'verification'],
    install_requires=[
        'medver-pytest',
        'pytest',
        'socket-oneline',
    ],
    classifiers=[
        # TODO update as needed
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],

    # common attributes from here on
    name='gui-api-tkinter',
    packages=find_packages(include='./gui_api_tkinter*', ),
    include_package_data=True,
    exclude_package_data={'./gui_api_tkinter/lib': ['.gitignore']},
    version='0.0.32',
    license='MIT',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    author='J. Arrizza',
    author_email='cppgent0@gmail.com',
    url='https://bitbucket.org/arrizza-public/gui-api-tkinter/src/master',
    download_url='https://bitbucket.org/arrizza-public/gui-api-tkinter/get/master.zip',
)
# @formatter:on

print('     setup: done')
