from setuptools import find_packages, setup

setup(
    name="jqgpt",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "jqgpt=jqgpt.main:main",
        ],
    },
    author="Ankush Agarwal",
    description="jqgpt is a gpt powered tool that helps you write jq queries. It takes a human user query and a json file as input and outputs a jq query that answers the user query. It requires an OPENAI_API_KEY to work.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ankushagarwal/jqgpt",
    license="MIT",
    python_requires=">=3.6",
)
