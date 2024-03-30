#!/bin/bash

# Compile multiple C files into a shared library
cd keyFeature
python3 setup.py build_ext --inplace
cd ..

# Optional: Move the shared library to a specific directory
# mkdir -p /path/to/your/directory
# mv your_library.so /path/to/your/directory/
