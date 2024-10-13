from setuptools import setup, find_packages

setup(
    name='vault-service',
    version='0.2.0',
    description='A reusable FastAPI vault utility service for other projects to use hashicorp vault',
    author='Ankush Bansal',
    author_email='ankush.bansal@asato.ai',
    packages=find_packages(include=['vault_service', 'vault_service.*']),
    install_requires=[
        'fastapi>=0.114.0',
        'uvicorn>=0.30.6',
        'gunicorn>=23.0.0',
        'hvac>=2.3.0',
        'python-dotenv>=1.0.1',
        'pydantic>=2.9.1',
    ],
    python_requires='>=3.11',  # Specify the required Python version
)