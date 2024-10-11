from setuptools import setup, find_packages

setup(
    name='wxauto',
    version='3.9.11.17.5',
    author='Cluic',
    author_email='tikic@qq.com',
    description='A simple wechat automation tool',
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    # a.dll
    package_data={'wxauto': ['*.dll']},
    install_requires=[
        'pywin32',
        'pyperclip',
        'Pillow',
        'psutil',
        'typing_extensions',
        'comtypes',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
