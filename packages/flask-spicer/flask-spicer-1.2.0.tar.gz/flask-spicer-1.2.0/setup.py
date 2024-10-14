from setuptools import setup, find_packages

setup(
    name="flask-spicer",
    version="1.2.0",
    description="Improve your flask experience using elements",
    author="ItsTato",
    author_email="thatpogcomputer@gmail.com",
    url="https://github.com/ItsTato/Spicer",
    packages=find_packages(),
    install_requires=[
		"flask",
		"colorama>=0.4.6"
	],
	entry_points={
		"console_scripts": [
			"spicer=flask_spicer.cli:run"
		]
	},
    classifiers=[
        "Programming Language :: Python :: 3",
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)