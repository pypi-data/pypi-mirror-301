from setuptools import setup, find_packages

setup(
        name="py-prompt-ai",
        version="0.0.1",
        author="Evan Straub",
        author_email="estraub@infrastructure-system.com",
        url="https://github.com/InfrastructureSystem/py-prompt-ai",
        description="An easy to use prompt manager for AI projects",
        packages=find_packages(),
        install_requires=[
            'jinja2>=3.0.0'
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
            "Operating System :: OS Independent",
        ]
)