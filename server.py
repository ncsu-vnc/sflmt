from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
import os, sys, getopt

import glob2, pickle
import numpy as np
from PIL import Image
from extractor import ImageFeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
import logging, threading, json, socket
from time import sleep
import netifaces as ni

ni.ifaddresses('eno1')
ip = ni.ifaddresses('eno1')[ni.AF_INET][0]['addr']

base_ip_address = '127.0.0.1' #ip
base_URL = 'http://' + base_ip_address
main_port = 8000
flask_port = 5000
sflmt_dir = "output"

search_results = 10

class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath

class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""
    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)

try:
   opts, args = getopt.getopt(sys.argv, 'p:d:')
   print (opts)
except getopt.GetoptError:
   print ('sflmt-server.py -d <directory> -m <mainport> -f <flaskport>')
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
	   print ('sflmt-server.py -d <directory> -m <mainport> -f <flaskport>')
	   sys.exit()
   elif opt in ("-d"):
	   sflmt_dir = arg
   elif opt in ("-m"):
	   main_port = arg
   elif opt in ("-f"):
	   flask_port = arg

#turn off general log messages to the console, only print errors
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def mainServer():

    web_dir = os.path.join(os.path.dirname(__file__), sflmt_dir)
    httpd = HTTPServer(web_dir, ("", main_port))
    httpd.serve_forever()

def flaskServer():

    # Read image features
    fe = ImageFeatureExtractor()
    features = []
    img_paths = []
    for feature_path in glob2.glob(sflmt_dir + '/data/feature/*'):
        features.append(pickle.load(open(feature_path, 'rb')))
        img_paths.append(base_URL + ':' + str(main_port) + '/data/originals/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')
    #print (img_paths)

    #app = Flask(__name__, template_folder= './' + path + '/templates' )
    app = Flask(__name__, template_folder= sflmt_dir + '/templates/' )

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        if request.method == 'POST':
            file = request.files['query_img']
            query_size = request.form['query_size']
            if file != None and query_size != None:
                if int(query_size) > 0 and int(query_size) < len(img_paths):
                    search_results = int(query_size)
                img = Image.open(file.stream)  # PIL image
                base_img_path = '/assets/uploaded/' + datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + "_" + file.filename
                uploaded_img_path = './' + sflmt_dir + base_img_path
                img.save(uploaded_img_path)
                query = fe.extract(img)
                dists = np.linalg.norm(features - query, axis=1)  # Do search
                ids = np.argsort(dists)[:search_results] # Top 30 results
                scores = [(dists[id], img_paths[id], os.path.basename(img_paths[id])) for id in ids]
                data = [os.path.basename(img_paths[id]) for id in ids]
                return render_template('search.html',
                                       sflmt_dir_path=(base_URL + ':' + str(main_port) + '/' + sflmt_dir + '/'),
                                       query_path=(base_URL + ':' + str(main_port) + base_img_path),
                                       scores=scores,
                                       data=json.dumps(data),
                                       querysize = search_results)
        else:
            return render_template('search.html', querysize = 15)

    app.run(base_ip_address, port = flask_port)

def announce():
    sleep(5)
    os.system('clear')
    print('----------------------------------')
    print('SFLMT server')
    print('to access - '  + base_URL + ':8000')
    print('----------------------------------')

if __name__ == "__main__":

    sendAnnounce = threading.Thread(target=announce)
    sendAnnounce.start()
    main_server = threading.Thread(target=mainServer)
    main_server.start()
    flaskServer()
