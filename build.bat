@echo off
cd C:\Users\msi-z\OneDrive\�h�L�������g\GitHub\PayNexus
pipreqs ./PayNexus
python remove.py
python setup.py sdist
python setup.py bdist_wheel
pause