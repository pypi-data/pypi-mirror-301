from setuptools import setup, find_packages

setup(
    name='vault-service',
    version='0.2.4',
    description='A reusable FastAPI vault utility service for other projects to use hashicorp vault',
    author='Ankush Bansal',
    author_email='ankush.bansal@asato.ai',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.114.0',
        'hvac>=2.3.0',
        'python-dotenv>=1.0.1',
        'pydantic>=2.9.1',
    ],
    python_requires='>=3.11',  # Specify the required Python version
)