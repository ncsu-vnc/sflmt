import http.server
import socketserver
import os, sys, getopt

def main(argv):
   path = "./"
   port = 5000
   try:
	   opts, args = getopt.getopt(argv, 'p:d:')
	   print (opts)
   except getopt.GetoptError:
	   print ('sflmt-server.py -d <directory> -p <port>')
	   sys.exit(2)
   for opt, arg in opts:
	   if opt == '-h':
		   print ('sflmt-server.py -d <directory> -p <port>')
		   sys.exit()
	   elif opt in ("-d"):
		   path = arg
	   elif opt in ("-p"):
		   port = arg

   web_dir = os.path.join(os.path.dirname(__file__), str(path))
   os.chdir(web_dir)

   Handler = http.server.SimpleHTTPRequestHandler

   with socketserver.TCPServer(("", int(port)), Handler) as httpd:
       print("serving " + str (path) + " at port", str(port))
       httpd.serve_forever()

if __name__ == "__main__":
   main(sys.argv[1:])
