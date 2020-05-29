# Street Feature-Location Mapping Tool (SFLMT)
version (0.0)

## Dependencies

Uses Python version >= 3.6

To install the Python dependencies, you can run (ideally in a virtual environment):

```bash
pip install -r requirements.txt
```

## Process a folder of images for visualization

```bash

python sflmt.py --images "./sample-images/files/*.jpg" --latlong "./sample-images/sample-images-metadata.json"

#python sflmt.py --images "path/to/images/*.jpg" --latlong "path/to/metadata/*.json"
```

## Start SFLMT server

```bash
python server.py

# usage: sflmt-server.py -d <directory> -m <main http server port> -f <flask server port>
# default directory -> "output", main http server port -> 8000 , flask server port -> 5000
```

## Access SFLMT

http://127.0.0.1:8000

## Acknowledgements
The WebGL image viewer within this tool is largely repurposed from the Yale DH Pixplot project (https://github.com/YaleDHLab/pix-plot), authored by Yale Digital Humanities Lab Developer Douglas Duhaim.
