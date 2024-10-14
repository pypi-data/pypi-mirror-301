from setuptools import setup, find_packages

setup(
    name="web_inspector",
    version="1.0.0",
    description="Library for web inspection and locator generation",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pyperclip",
        "keyboard"
    ],
    entry_points={
        'console_scripts': [
            'run-inspector = web_inspector.run_inspector:main',
        ],
    },
)
