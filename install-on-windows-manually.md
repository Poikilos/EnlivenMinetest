# Chunkymap Installation
### OPTIONALLY manual install
(install-chunkymap-on-windows.py does all of required steps in this file automatically)
        * put these files anywhere
        * python 2.7.x such as from python.org
        * run get_python_architecture.py to make sure you know whether to download the following in 32-bit or 64-bit  
        Administrator Command Prompt (to find it in Win 10, right-click windows menu)
        * update python package system:
```
C:\python27\python -m pip install --upgrade pip wheel setuptools
```
        * numpy such as can be installed via the easy unofficial installer wheel at  
        http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy  
        then:
```
#cd to the folder where you downloaded the whl file
C:\python27\python -m pip install "numpy-1.10.4+mkl-cp27-cp27m-win32.whl"  
```
        (but put your specific downloaded whl file instead)  
        * Pillow (instead of PIL (Python Imaging Library) which is a pain on Windows): there is a PIL installer wheel for Python such as 2.7 here:  
        http://www.lfd.uci.edu/~gohlke/pythonlibs/  
        as suggested on http://stackoverflow.com/questions/2088304/installing-pil-python-imaging-library-in-win7-64-bits-python-2-6-4  
        then:
```
C:\python27\python -m pip install "Pillow-3.1.1-cp27-none-win32.whl"
```
        (but put your specific downloaded whl file instead, such as Pillow-3.1.1-cp27-none-win_amd64.whl)
        * run (or if your python executable does not reside in C:\Python27\ then first edit the file):
```
chunkymap-generator.bat
```
        (all the batch does is run C:\Python27\python generator.py)
        (generator.py will ask for configuration options on first run and ask for your www root)