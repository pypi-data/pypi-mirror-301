from setuptools import setup, find_packages

setup(
    name= 'capote_ai',
    version='0.1',
    packages=find_packages(),
    install_requirements=[
        # Add dependencies here
        'openai',
        'python-dotenv',
        'PyMuPDF',
        'pdfplumber',
        'pandas',
    ],
)