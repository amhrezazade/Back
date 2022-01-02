

print("\r\n")
PORT = 4848

import json 
import socket
import http.server
import socketserver
import app




class Handler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        resp = {}
        if self.path.startswith("/p2"):
            try:
                Data = (self.rfile.read(int(self.headers['content-length']))).decode('utf-8')
                jsondata = json.loads(Data)
                Name = jsondata['Query']
            except:
                print("error parsing json data")
                resp = {"status":0}
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(resp).encode())
                return
            res = app.GetDocList(Name)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return
        if self.path.startswith("/su"):
            Data = (self.rfile.read(int(self.headers['content-length']))).decode('utf-8')
            res = app.GetSuggestion(Data)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return        
        resp = {'Error':'404'}
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode())

    def do_GET(self):

        if self.path == "/test":
            print("Request : Test")
            print("Test Api : Application is running")
            resp = {"status":1}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
            return

        if self.path.startswith("/GetDoc/") :
            id = self.path[8:]
            resp = app.GetDoc(id)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
            return
        resp = {'Error':'404'}
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode())







myserver =  socketserver.TCPServer(("", PORT), Handler)
print("\r\nServer Started")
myserver.serve_forever()