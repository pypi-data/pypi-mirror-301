from setuptools import setup, find_packages

setup(
    name="capstoneproject2024_common",
    version="0.1.0",
    description="Reuse code for FastAPI",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["python-jose", "python-dotenv", "fastapi"],
    python_requires='>=3.6',
)
