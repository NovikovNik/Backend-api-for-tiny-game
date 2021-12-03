import argparse
from os import pardir
import flask
import requests
import threading
from flask import Flask, request, jsonify
from werkzeug.exceptions import abort

from db.bd_api.exceptions import UserNotFoundException
from db.bd_api.interaction import DbInteraction
from utils import config_parser

class Server:
    
    def __init__ (self, host, port, db_host, db_user, password, db_name):
        self.host = host
        self.port = port

        self.db_interaction = DbInteraction(
            host = db_host,
            user = db_user,
            password = password,
            db_name = db_name,
            rebuild_db=False
        )

        self.app = Flask(__name__)
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/add_user', view_func=self.add_user_info, methods=['POST'])
        self.app.add_url_rule('/get_user/<username>', view_func=self.get_user_info)
        self.app.add_url_rule('/edit_user', view_func=self.edit_user_info, methods=['PUT'])

        self.app.register_error_handler(404, self.page_not_found)

    def page_not_found(self, err_description):
        return  jsonify(error=str(err_description)), 404

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

    def add_user_info(self):
        request_body = dict(request.json)
        username = request_body['username']
        password = request_body['password']
        email = request_body['email']

        self.db_interaction.add_user_info(
            username=username,
            password=password,
            email=email
        )
        return f'Succes added {username}',201

    def get_user_info(self, username):
        try:
            user_info = self.db_interaction.get_user_info(username)
            return user_info, 200
        except UserNotFoundException:
            abort(404, description='User not found')

    def edit_user_info(self):
        try:
            request_body = dict(request.json)
            new_username = request_body['username']
            new_password = request_body['new_password']
            new_email = request_body['new_email']

            self.db_interaction.edit_user_info(
                username=new_username,
                new_username=new_username,
                new_password=new_password,
                new_email=new_email
            )
            return 'succes', 200

        except UserNotFoundException:
            abort(404, description='User not found')
        
if __name__== '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, dest='config')
    
    args = parser.parse_args()
    
    config = config_parser(args.config)
    
    server_host = config['SERVER_HOST']
    server_port = config['SERVER_PORT']

    db_host = config['DB_HOST']
    db_user = config['DB_USER']
    db_password = config['DB_PASSWORD']
    db_name = config['DB_NAME']

    server =  Server(
        host= server_host,
        port= server_port,
        password= db_password,
        db_name= db_name,
        db_host= db_host,
        db_user = db_user
    )
    server.run_server()
    