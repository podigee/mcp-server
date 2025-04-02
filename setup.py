from setuptools import setup, find_packages

setup(
    name="podigee-mcp-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.2.0",
        "httpx>=0.24.0",
        "python-dotenv>=1.0.0",
    ],
    description="A Model Context Protocol server for the Podigee podcast platform",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/pod-mcp",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
) 