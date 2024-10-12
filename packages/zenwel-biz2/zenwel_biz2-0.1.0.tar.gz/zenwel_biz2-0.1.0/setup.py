from setuptools import setup, find_packages

setup(
    name='zenwel-biz2',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Daftar dependensi
    ],
    entry_points={
        'console_scripts': [
            # 'command-name = zenwel-biz2.module:function',
        ],
    },
    author='Adit',
    author_email='aditbekerja@gmail.com',
    description='Deskripsi singkat paket Anda',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/olseraqa/zenwel-biz.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    #python_requires='>=3.12.5',
)