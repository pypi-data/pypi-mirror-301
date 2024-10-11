from setuptools import setup, find_packages

setup(
    name="hostasphere_profiler",
    version="v1.0-rc3",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "psutil>=6.0.0",
        "grpcio>=1.66.2",
        "grpcio-tools>=1.66.2",
        "OpenHosta>=1.1.0rc3"
    ],
    author="William Jolivet",
    description="Hostasphere Profiler API",
    author_email="william.jolivet@epitech.eu",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/hand-e-fr/hostasphere",
    python_requires='>=3.6',
)