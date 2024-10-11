from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="backtrack_sampler",
    version="0.0.4",
    description="An LLM sampler that allows rewinding and revising generated tokens",
    author="Mihai Chirculescu",
    author_email="apropodemine@gmail.com",
    url="https://github.com/Mihaiii/backtrack_sampler",
    packages=find_packages(),
    py_modules=['backtrack_sampler'],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
