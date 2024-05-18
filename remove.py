import shutil

try:
    shutil.rmtree("./build")
except Exception as e:
    print(e)
try:
    shutil.rmtree("./dist")
except Exception as e:
    print(e)
