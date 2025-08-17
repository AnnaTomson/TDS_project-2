from setuptools import setup, find_packages

setup(
    name="data_analyst_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'flask>=2.3.3',
        'openai>=1.0.0',
        'pandas>=2.0.0',
        'matplotlib>=3.7.0',
        'numpy>=1.24.0',
        'openpyxl>=3.1.0',
        'python-dotenv>=1.0.0',
        'python-multipart>=0.0.6',
        'python-dateutil>=2.8.2',
        'requests>=2.31.0'
    ],
    python_requires='>=3.8',
)
