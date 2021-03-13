#!/bin/bash

rm ./source/textplainer.rst
rm ./source/modules.rst

make clean
sphinx-apidoc -o ./source ../textplainer
make html

