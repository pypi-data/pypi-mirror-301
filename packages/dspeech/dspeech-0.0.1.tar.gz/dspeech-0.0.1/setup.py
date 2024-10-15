from setuptools import setup, find_packages

setup(
    name='dspeech',
    version='0.0.1',
    description='A Speech-to-Text toolkit with VAD, punctuation, and emotion classification',
    author='Zhao Sheng',
    author_email='zhaosheng@nuaa.edu.cn',
    packages=find_packages(),
    install_requires=[
        'torch',
        'numpy',
        'soundfile',
        'funasr',
        'rich',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'dspeech=dspeech.cli:main',  # 将 CLI 绑定到 dspeech 命令
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
