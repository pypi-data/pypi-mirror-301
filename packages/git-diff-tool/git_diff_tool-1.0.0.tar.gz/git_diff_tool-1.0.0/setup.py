from setuptools import setup, find_packages

setup(
    name="git_diff_tool",
    version="1.0.0",
    author="Abenezer Tesfaye",
    author_email="aben.ezer443@gmail.com",
    description="A tool for comparing Git branches",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/kecheste/diff_tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'diff_tool=diff_tool.diff_tool:main',
        ],
    }
)
