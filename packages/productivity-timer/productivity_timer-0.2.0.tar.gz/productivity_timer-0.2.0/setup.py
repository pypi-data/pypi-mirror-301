from setuptools import setup, find_packages

setup(
    name="productivity-timer",
    version="0.2.0",
    description="A timer library for managing multiple timers for multiple individuals.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Abhishek",
    author_email="abhishekshivtiwari@gmail.com",
    url='https://github.com/Abhi-shekes/productivity_timer', 
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)


