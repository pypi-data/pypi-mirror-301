from pathlib import Path

from setuptools import find_packages
from setuptools import setup

print('     setup: version:  v1.0.4')
print('     setup: module :  on_the_fly_stats')

# @formatter:off
setup(
    description='On the fly statistics including standard deviation, average, min/max and counters',
    keywords=['statistics', 'utility'],
    install_requires=[
        'medver-pytest',
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],

    # common attributes from here on
    name='on-the-fly-stats',
    packages=find_packages(include='./on_the_fly_stats*', ),
    include_package_data=True,
    exclude_package_data={'./on_the_fly_stats/lib': ['.gitignore']},
    version='1.0.4',
    license='MIT',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    author='J. Arrizza',
    author_email='cppgent0@gmail.com',
    url='https://bitbucket.org/arrizza-public/on-the-fly-stats/src/master',
    download_url='https://bitbucket.org/arrizza-public/on-the-fly-stats/get/master.zip',
)
# @formatter:on

print('     setup: done')
