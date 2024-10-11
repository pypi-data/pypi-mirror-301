from setuptools import setup, find_packages

setup(
    name="humanscript",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests==2.31.0",
        "transformers==4.31.0",
        "tensorflow>=2.11.0",
        "scikit-learn==1.2.2",
        "torch==2.0.1",
        "SQLAlchemy==2.0.15",
        "pymongo==4.5.0",
        "websockets==11.0.3",
        "Flask==2.3.3",
        "jsonschema==4.17.3",
        "jinja2==3.1.2",
        "joblib==1.3.2",
    ],
    entry_points={
        "console_scripts": [
            "humanscript=parser:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A human-readable programming language for web and mobile app generation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/humanscript",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
