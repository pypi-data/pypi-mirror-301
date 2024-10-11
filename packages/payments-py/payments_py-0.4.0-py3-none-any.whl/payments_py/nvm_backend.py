import asyncio
import json
import re
import requests
import socketio
import jwt
from typing import Optional, Dict, List, Any

from payments_py.environments import Environment

sio = socketio.AsyncClient(logger=False, engineio_logger=False)


class BackendApiOptions:
    def __init__(self,
                 environment: Environment,
                 api_key: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None,
                 web_socket_options: Optional[Dict[str, Any]] = None):
        self.api_key = api_key
        self.backend_host = environment.value['backend']
        self.web_socket_host = environment.value['websocket']
        self.proxy_host = environment.value['proxy']
        self.headers = headers or {}
        self.web_socket_options = web_socket_options or {}


class NVMBackendApi:
    def __init__(self, opts: BackendApiOptions):
        self.opts = opts
        self.socket_client = sio
        self.room_id = None
        self.has_key = False

        default_headers = {
            'Accept': 'application/json',
            **(opts.headers or {}),
            **({'Authorization': f'Bearer {opts.api_key}'} if opts.api_key else {})
        }

        if opts.web_socket_options and opts.web_socket_options.get('bearer_token'):
            opts.web_socket_options['transport_options'] = {
                'websocket': {
                    'extraHeaders': {'Authorization': f'Bearer {opts.web_socket_options["bearer_token"]}'}
                }
            }

        self.opts.headers = default_headers
        self.opts.web_socket_options = {
            **(opts.web_socket_options or {})
        }

        try:
            if self.opts.api_key and len(self.opts.api_key) > 0:
                decoded_jwt = jwt.decode(self.opts.api_key, options={"verify_signature": False})
                client_id = decoded_jwt.get('sub')
                
                # Check if the client_id exists and does not match the specified pattern
                if client_id:# and not re.match(r'^0x[a-fA-F0-9]{40}$', client_id):
                    self.room_id = f"room:{client_id}"
                    self.has_key = True
        except Exception:
            self.has_key = False
            self.room_id = None 

        try:
            backend_url = self.opts.backend_host.rstrip('/')
            self.opts.backend_host = backend_url
        except Exception as error:
            raise ValueError(f"Invalid URL: {self.opts.backend_host} - {str(error)}")
    
    async def connect_socket(self):
        if not self.has_key:
            raise ValueError('Unable to subscribe to the server because a key was not provided')

        if self.socket_client and self.socket_client.connected:
            return
        
        try:
            print(f"nvm-backend:: Connecting to websocket server: {self.opts.web_socket_host}")
            # self.socket_client = socketio.AsyncClient(logger=True, engineio_logger=True)
            await self.socket_client.connect(self.opts.web_socket_host, headers=self.opts.headers, transports=["websocket"])
            print(f"nvm-backend:: Connected: {self.socket_client.connected}")
        except Exception as error:
            raise ConnectionError(f"Unable to initialize websocket client: {self.opts.web_socket_host} - {str(error)}")

    async def disconnect_socket(self):
        if self.socket_client and self.socket_client.connected:
            self.socket_client.disconnect()


    # @sio.on('connect')
    # async def on_connect(self):
    #     print('nvm-backend:: Connected XXXXXX')
    

    async def _subscribe(self, callback, events: Optional[str]=None):
        await self.connect_socket()
        if not self.socket_client.connected:
            raise ConnectionError('Failed to connect to the WebSocket server.')
        
        async def event_handler(data):
            parsed_data = json.loads(data)    
            print(f"nvm-backend:: Received event: {parsed_data}")
            received_event_type = parsed_data.get('event')
            if isinstance(events, list):
                if received_event_type in events:
                    print(f"Received {received_event_type} event from list: {parsed_data}")
                    await callback(parsed_data['data'])
                else:
                    print(f"Ignoring event {received_event_type} (expecting one of {events})")
            else:
                print(f"Ignoring event {received_event_type} (expecting {events})")

        
        # Register event listener for the room
        self.socket_client.on(self.room_id, event_handler)
        
        # self.socket_client.on(self.room_id, callback)
        print(f"nvm-backend:: Joining room: {self.room_id}")
        
        # Join the room
        await self.join_room(self.room_id)
        print(f"nvm-backend:: Joined room: {self.room_id}")


    async def _emit_events(self, data: Any):
        print(f"nvm-backend:: Emitting events to room: {self.room_id}")
        # print(f"nvm-backend:: Emitting data: {data}")
        await self.connect_socket()
        # await self.socket_client.emit('room_message', {"room": self.room_id, "data": data})

        await self.socket_client.emit(event=self.room_id, data=data)


    async def join_room(self, room_id):
        print(f"event:: Joining room: {room_id}")
        await self.socket_client.emit('join_room', { "room": room_id })


    async def disconnect(self):
        await self.disconnect_socket()
        print("nvm-backend:: Disconnected from the server")

    def parse_url_to_proxy(self, uri: str) -> str:
        # print(f"nvm-backend:: Parsing URL: {uri}")
        return f"{self.opts.proxy_host}{uri}"
    
    def parse_url_to_backend(self, uri: str) -> str:
        # print(f"nvm-backend:: Parsing URL: {uri}")
        return f"{self.opts.backend_host}{uri}"

    def set_bearer_token(self, token: str):
        self.opts.headers['Authorization'] = f'Bearer {token}'

    def get(self, url: str):
        try:
            response = requests.get(url, headers=self.opts.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            return {"data": err.response.json(), "status": err.response.status_code, "headers": err.response.headers}

    def post(self, url: str, data: Any):
        try:
            response = requests.post(url, json=data, headers=self.opts.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            return {"data": err.response.json(), "status": err.response.status_code, "headers": err.response.headers}

    def put(self, url: str, data: Any):
        try:
            response = requests.put(url, json=data, headers=self.opts.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            return {"data": err.response.json(), "status": err.response.status_code, "headers": err.response.headers}

    def delete(self, url: str, data: Any):
        try:
            response = requests.delete(url, json=data, headers=self.opts.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            return {"data": err.response.json(), "status": err.response.status_code, "headers": err.response.headers}
