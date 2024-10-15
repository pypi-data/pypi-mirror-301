# CDM Python frontend

Python frontend to communicate with the CDM. This library implements the 0mq API

## Build & install

To build the project run: `python3 setup.py build` which will also build the cdmpy module.

To install it: `python3 setup.py install --user`

### Manual build

To compile the tiny cdmpy module manually run: `bash -c "cd common-cdm && g++ -O3 -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes) cdmpy.cpp -o ../cdmpy$(python3-config --extension-suffix)"`
Note that the module depends on pybind11.

In mac:
```
bash -c "cd common-cdm && g++ -O3 -shared -std=c++17 -fPIC -Wl,-undefined,dynamic_lookup $(python3 -m pybind11 --includes) $(python3-config --ldflags) cdmpy.cpp -o ../cdmpy$(python3-config --extension-suffix)"
```

## GUI

Once the project is installed the GUI can be executed running "cdm_gui" command. 

To run the gui without installing the project `python3 -m cdm_gui.widget` can be used. 
