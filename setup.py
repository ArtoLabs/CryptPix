from setuptools import setup, find_packages

setup(
    name='cryptpix',
    version='0.2.0',
    description='A minimal image obfuscation tool that splits images into layered components for CSS-based reconstruction.',
    author='Your Name',
    author_email='you@example.com',
    packages=find_packages(),
    include_package_data=True,  # <-- Add this line
    install_requires=[
        'Pillow'
    ],
    python_requires='>=3.7',
)
