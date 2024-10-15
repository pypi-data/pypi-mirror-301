from setuptools import setup, find_packages

setup(
    name='dspeech',
    version='0.0.2',
    description='A Speech-to-Text toolkit with VAD, punctuation, and emotion classification',
    author='Zhao Sheng',
    author_email='zhaosheng@nuaa.edu.cn',
    packages=find_packages(),
    install_requires=[
        'torch>=2.1.0',
        'numpy',
        'soundfile',
        'funasr>=1.1.12',
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
