from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    ext_modules=cythonize([
        Extension(
            name="lib.PAEKS.paeks",
            sources=["lib/PAEKS/paeks.pyx"],
            libraries=["pbc", "gmp", "ssl", "crypto"],
            include_dirs=["/mnt/c/Users/leo/leoliu91/pbc", "/usr/include/openssl", "/usr/include/x86_64-linux-gnu"],
        ),
        Extension(
            name="lib.PKE.pke",
            sources=["lib/PKE/pke.pyx"],
            libraries=["pbc", "gmp", "ssl", "crypto"],
            include_dirs=["/mnt/c/Users/leo/leoliu91/pbc", "/usr/include/openssl", "/usr/include/x86_64-linux-gnu", "/usr/include"],
        ),
        Extension(
            name="lib.SCF.scf",
            sources=["lib/SCF/scf.pyx"],
            libraries=["pbc", "gmp", "ssl", "crypto"],
            include_dirs=["/mnt/c/Users/leo/leoliu91/pbc", "/usr/include/openssl", "/usr/include/x86_64-linux-gnu"],
        ),
    ]),
)
