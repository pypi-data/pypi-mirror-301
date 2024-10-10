from setuptools import setup, find_packages

setup(
    name='vlm-ocr',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open('requirements.txt')
    ],
    author='Ethan Bailie',
    author_email='eabailie@uwaterloo.ca',
    description='Allows you to easily use a VLM for OCR purposes. Currently only OpenAI, working on adding more VLM compatibility',
    url='https://github.com/ethanbailie/vlm-ocr',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
