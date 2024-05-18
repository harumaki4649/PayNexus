@echo off
cd C:\Users\msi-z\OneDrive\ƒhƒLƒ…ƒƒ“ƒg\GitHub\PayNexus
pipreqs ./PayNexus
python remove.py
python setup.py sdist
python setup.py bdist_wheel