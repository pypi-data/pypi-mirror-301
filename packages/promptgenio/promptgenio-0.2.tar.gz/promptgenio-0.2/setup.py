from setuptools import setup, find_packages

setup(
    name='promptgenio',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
        'groq',
    ],
    author='Christian Madsen',
    author_email='hej@echristiannmadsen.dk',
    description='A Python package for PromptGenio integration',
    url='https://github.com/christiannmadsen/promptgenio-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)