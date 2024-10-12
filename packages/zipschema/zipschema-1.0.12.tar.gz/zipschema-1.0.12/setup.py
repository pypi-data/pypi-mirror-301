from setuptools import setup, find_packages

setup(
    name="zipschema",
    version="1.0.12",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "jsonschema",
        "jinja2",
        "python-docx"
    ],
    entry_points={
        'console_scripts': [
            'zipschema=zipschema.zipschema:main',
            'zs=zipschema.zipschema:main'
        ],
    },
    author="Sean Hummel",
    description="CLI tool for validating zipschema files and generating documentation.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mrmessagewriter/zipschema",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
