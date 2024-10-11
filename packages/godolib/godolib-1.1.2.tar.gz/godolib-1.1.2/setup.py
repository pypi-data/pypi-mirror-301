from setuptools import setup, find_packages

setup(
    name='godolib',
    version='1.1.2',
    packages=find_packages(),
    install_requires=['statsmodels', 'numpy', 'scikit-learn', 'pandas', 'boto3', 'chardet', 'psutil', 'plotly', 'matplotlib'],
    description='Machine/Deep learning and preprocessing oriented library',
    author='Sergio Montes',
    author_email='ss.montes.jimenez@gmail.com',
    url='',
)
