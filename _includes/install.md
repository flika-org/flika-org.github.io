
# Flika Installation

## Python
Flika works with Python 2 and 3, but several of its dependencies may not.  Download [Python](https://www.python.org/downloads/) or install [Anaconda](https://www.continuum.io/downloads) to get several plugins pre-installed.
     
## Download Flika
Download the [zipped folder](https://github.com/kyleellefsen/Flika/archive/master.zip) and extract it to a location on your computer (like C:/Program Files/Flika), or visit the [github page](https://github.com/kyleellefsen/Flika/) to fork it yourself. Flika uses the same folder for every OS, but the installation steps are different.

### Windows
Navigate to the Flika directory and run the Flika.bat file. This will open a command prompt and begin installing any dependencies needed to start Flika.
### Linux
Open a terminal and run the following commands:


```python
sudo apt-get install python-pip python-numpy python-scipy build-essential cython python-matplotlib
sudo pip install scikit-image
sudo pip install future
```


      File "<ipython-input-3-c95f2af57c94>", line 1
        sudo apt-get install python-pip python-numpy python-scipy build-essential cython python-matplotlib
               ^
    SyntaxError: invalid syntax
    


Navigate to the Flika directory and run


```python
python FLIKA.py
```


      File "<ipython-input-4-9ef3ed642c06>", line 1
        python FLIKA.py
                   ^
    SyntaxError: invalid syntax
    


### Mac OS X
Install Anaconda by Continuum. This will install Python along with most of Flika's dependencies.
Any libraries not included in Anaconda will be installed the first time Flika is run.
Download the FLIKA zipped folder and extract the folder to a location on your computer. Navigate to the Flika directoryand run


```python
python FLIKA.py
```


      File "<ipython-input-5-9ef3ed642c06>", line 1
        python FLIKA.py
                   ^
    SyntaxError: invalid syntax
    

