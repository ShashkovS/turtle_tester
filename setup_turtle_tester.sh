#!/bin/bash
git clone https://github.com/ShashkovS/turtle_tester
cd turtle_tester/
git pull origin master
python3 setup.py install --user
cd ..
