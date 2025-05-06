from setuptools import setup, find_packages

setup(
    name="inkbook-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "supabase",
        "pytest",
        "httpx",
    ],
    python_requires=">=3.11",
) 