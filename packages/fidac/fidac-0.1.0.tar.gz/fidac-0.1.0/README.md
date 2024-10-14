# FIDAC - A tool to capture facial location and distance

## Description


## Manual Faces Tutorial (Mac)


### Python Set-up
If you don't already have Python, install Python from their website: https://www.python.org/downloads/
Next, we need to install pip which is neccesary for importing all libraries. Open Terminal, an already installed application and then input these lines of code:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
```
python3 get-pip.py
```

Pip should now be successfully installed. For this program, we only need pandas and opencv which you can install by running this line in terminal.
```
pip install opencv-python pandas
```

Now your coding environment is all set up!

### Environment Set-Up
After determining what faces need to be manual, you should have a folder somewhere on your device named 'IPD_manual'. Determine the path to this folder which can be found by doing: Choose View > Show Path Bar, or press the Option key to show the path bar momentarily.
Here is a sample path: "/Users/keshav_rastogi/Documents/IPD_Manual". 

Now, plug in the path to the IPD_manual folder to the variable 'path' which is the first line in the process_file method, found near the end of manual_calculate.py. 
It should look something like this: path = "/Users/keshav_rastogi/Documents/IPD_Manual".

