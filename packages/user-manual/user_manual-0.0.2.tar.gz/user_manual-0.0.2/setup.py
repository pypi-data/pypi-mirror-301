# setup.py
from setuptools import setup, find_packages

setup(
    name="user_manual",
    version="0.0.2",
    packages=find_packages(),
    install_requires=['wheel','opencv-python==4.10.0.84','opencv-contrib-python==4.10.0.84','opencv-python-headless==4.10.0.84','PyMuPDF==1.24.9','PyMuPDFb==1.24.9','numpy==1.24.2','matplotlib==3.6.3','matplotlib-inline==0.1.6','pypdf==4.3.1','PyPDF2==3.0.1','Pillow==9.5.0','python-docx==1.1.2','PyAutoGUI==0.9.54','pyperclip==1.8.2','paddleocr==2.8.1','paddlepaddle==2.6.2'],
    entry_points={
        'console_scripts': [
            'user_manual=user_manual.user_manual:main',
        ],
    },
    author="Aviral Srivastava",
    author_email="aviralsrivastava284@gmail.com",
    description="Generate the User Manual by ChatGPT",
    long_description_content_type='text/markdown',
    url="https://github.com/A284viral/protections_v1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)