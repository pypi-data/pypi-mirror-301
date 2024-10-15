from setuptools import setup, find_packages

setup(
    name="GenCareAIUtils",
    version="0.1.4", 
    author_email="info@doktereva.nl",
    description="Helper functions for the GenCareAI project",
    long_description="Helper functions for the GenCareAI project",
    long_description_content_type="text/markdown",
    url="https://github.com/ekrombouts/GenCareAIUtils",
    packages=find_packages(),
    install_requires=[
        "os",
    ],
)