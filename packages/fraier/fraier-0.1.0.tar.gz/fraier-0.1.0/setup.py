from setuptools import setup, find_packages

setup(
    name="fraier",  # Nama paket
    version="0.1.0",  # Versi paket
    author="akmal",  # Nama penulis
    author_email="akmalrbc6@gmail.com",  # Pastikan ini alamat email yang valid
    description="Deskripsi singkat paket",
    long_description=open('README.md').read(),  # Deskripsi panjang paket
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Paket yang akan dimasukkan
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
