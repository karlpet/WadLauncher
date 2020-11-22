# WadLauncher
Simple wad launcher for doom games.

# How to setup environment
Make sure you are using python3, version >= 3.5  
Make sure you have pip installed  

Create a virtual environment in base folder:
```
> python3 -m venv venv
```

Source into virtual environment and install packages:  
```
> source venv/bin/activate
> pip install -r requirements_dev.txt
```

Run project:  
```
> fbs run
```

Build project:  
```
> fbs freeze
```

Start QtDesigner
```
> qtchooser -run-tool=designer -qt=5
```
