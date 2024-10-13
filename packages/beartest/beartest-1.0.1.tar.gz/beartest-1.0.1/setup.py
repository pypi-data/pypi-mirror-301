import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='beartest',
    version='1.0.1',
    author='bear',
    author_email='bear@qq.com',
    description='oh bear!',
    long_description=long_description,
    url='https://github.com/Qiyana-bear/bear_pip_test',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

