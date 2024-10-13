from setuptools import setup, find_packages

setup(
    name="retriever_elsa",  # The name of your package
    version="0.2",  # The initial release version
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[  # List any dependencies your package has
        "requests",
        "pydantic",
    ],
    entry_points={  # Optional: If you want to create a command-line tool
        'console_scripts': [
            'retriever=retriever.retriever:main',  # Optional, change 'main' to the function you want as entry
        ],
    },
    author="abubakar",  # Your name as the author
    author_email="abubakarilyas624@gmail.com",  # Your contact email
    description="A package for interacting with Qdrant for memory retrieval and upsert operations",
    classifiers=[  # Classifiers to help users find your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
