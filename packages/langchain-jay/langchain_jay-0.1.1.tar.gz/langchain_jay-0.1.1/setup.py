from setuptools import setup, find_packages

setup(
    name='langchain_jay',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        # 필요한 패키지 목록
    ],
    author='Jae Yeob Kim',
    author_email='codejay2023@gmail.com',
    description='langchain util',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jaycando/langchain',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
