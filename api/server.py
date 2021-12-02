import argparse
from os import pardir
import flask
import requests
import threading
from flask import Flask, request

from utils import config_parser

class Server:
    
    def __init__ (self, host, port):
        self.host = host
        self.port = port
        
        self.app = Flask(__name__)
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/', view_func=self.get_home)
        
    def run_server(self):
        self.server = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port})
        self.server.start()
        return self.server
        
    def shutdown_server(self):
        request.get(f'http://{self.host}:{self.port}/shutdown')
        
    def shutdown(self):
        terminate_function = request.environ.get('werkzeug.server.shutdown')
        if terminate_function:
            terminate_function()
                
    def get_home(self):
        return 'bip-bup-bop...testing'
        
if __name__== '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, dest='config')
    
    args = parser.parse_args()
    
    config = config_parser(args.config)
    
    server_host = config['SERVER_HOST']
    server_port = config['SERVER_PORT']
    
    server =  Server(
        host= server_host,
        port= server_port
    )
    server.run_server()
    