from setuptools import setup, find_packages
# python setup.py sdist bdist_wheel
# twine upload dist/*
setup(
    name='ttlinks',
    version='0.2.1a',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt', '*.json', '*.csv']},
    license='MIT',
    description='TTLinks Network Service Packages',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yantao Tao',
    author_email='dorisjingjing531@gmail.com',
    url='https://github.com/tyt063144/TTLinks.git',
    install_requires=[
        'inflect'
    ],
    keywords=['network', 'ttlinks', 'networking', 'automation',
              'ip', 'mac', 'python', 'wildcard', 'subnet', 'network automation'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Telecommunications Industry",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Networking",
    ]
)