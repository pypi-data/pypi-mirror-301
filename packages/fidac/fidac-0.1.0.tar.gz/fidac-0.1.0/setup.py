from setuptools import setup, find_packages

setup(
    name='fidac',
    version='0.1.0',
    author='Keshav Rastogi',
    author_email='keshavrast21@gmail.com',
    description='insert description', # modify later
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_library', # modify later
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.9',
    install_requires=[
        'pandas',
        'opencv-python',  # for cv2
        'tqdm',
        'numpy',
        'matplotlib',
        'seaborn',
    ]
)