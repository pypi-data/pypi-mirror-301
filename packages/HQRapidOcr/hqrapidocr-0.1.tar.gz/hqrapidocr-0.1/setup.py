from setuptools import setup, find_packages

setup(
    name='HQRapidOcr',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'numpy',
        'rapidocr-onnxruntime',
        'pillow'
    ],
    author='Fzz',
    author_email='1349168301@qq.com',
    description='A simple OCR SDK based on RapidOCR and Flask',
    long_description=open('README.md').read(),  # 从 README 文件中获取详细描述
    long_description_content_type='text/markdown',  # README 文件的格式
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # 支持的 Python 版本
)