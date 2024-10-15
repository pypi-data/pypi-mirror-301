from setuptools import setup

setup(
    name="printf-package", 
    version="0.2.0", 
    py_modules=["printf"], 
    install_requires=[],  
    description="A package for experiment printf function",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/uchihamadara6969/printf-package",  
    author="Darked Nuke",  
    author_email="darkednuke@gmail.com", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
