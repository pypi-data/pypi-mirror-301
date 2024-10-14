from pathlib import Path
import setuptools


setuptools.setup(
    name="streamlit-quill2",
    version="0.0.4",
    author="bkdevinci",
    author_email="",
    description="Quill component for Streamlit",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/bkdevinci/streamlit-quill",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
