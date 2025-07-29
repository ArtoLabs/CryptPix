from setuptools import setup, find_packages

setup(
    name='cryptpix',
    version='0.1.0',
    description='A minimal image obfuscation tool that splits images into layered components for CSS-based reconstruction.',
    author='Your Name',
    author_email='you@example.com',
    packages=find_packages(),
    install_requires=[
        'Pillow'
    ],
    python_requires='>=3.7',
)
