# Street Feature-Location Mapping Tool (SFLMT)



## Dependencies

Uses Python version >= 3.6

To install the Python dependencies, you can run (ideally in a virtual environment):

```bash
pip install -r requirements.txt
```

## Process a folder of images for visualization

```bash
python sflmt.py --images "path/to/images/*.jpg"

#python sflmt.py --images "path/to/images/*.jpg" --metadata "path/to/metadata/*.json"
```

## start SFLMT server

```bash
python sflmt-server.py
# usage: sflmt-server.py -d <directory> -p <port>
# default directory "./" port 5000
```

## Acknowledgements
The WebGL image viewer within this tool is largely repurposed from the Yale DH Pixplot project (https://github.com/YaleDHLab/pix-plot), authored by Yale Digital Humanities Lab Developer Douglas Duhaim.
