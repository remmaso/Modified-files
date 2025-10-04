import asyncio
import websockets
import json
from datetime import datetime
from aiohttp import web
import aiohttp_cors

class SimpleChatServer:
    def __init__(self, host='0.0.0.0', ws_port=8765, http_port=8081):
        self.host = host
        self.ws_port = ws_port
        self.http_port = http_port
        self.clients = set()
        self.client_nicknames = {}
        self.messages = []  # Store recent messages for new users
        
    async def register(self, websocket):
        """Register a new client"""
        self.clients.add(websocket)
        print(f"[SERVER] New client connected. Total clients: {len(self.clients)}")
        
    async def unregister(self, websocket):
        """Unregister a client"""
        if websocket in self.clients:
            self.clients.remove(websocket)
            if websocket in self.client_nicknames:
                nickname = self.client_nicknames[websocket]
                del self.client_nicknames[websocket]
                await self.broadcast_system_message(f"{nickname} left the chat")
                print(f"[SERVER] {nickname} disconnected. Total clients: {len(self.clients)}")
    
    async def broadcast_message(self, message, sender=None):
        """Broadcast message to all clients except sender"""
        if self.clients:
            tasks = []
            for client in self.clients:
                if client != sender:
                    tasks.append(client.send(json.dumps(message)))
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def broadcast_system_message(self, text):
        """Broadcast a system message to all clients"""
        message = {
            'type': 'system',
            'text': text,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        await self.broadcast_message(message)
    
    async def send_user_list(self):
        """Send updated user list to all clients"""
        users = list(self.client_nicknames.values())
        message = {
            'type': 'user_list',
            'users': users
        }
        await self.broadcast_message(message)
    
    async def handle_websocket(self, websocket):
        """Handle WebSocket client connection"""
        await self.register(websocket)
        
        try:
            async for message_str in websocket:
                try:
                    data = json.loads(message_str)
                    message_type = data.get('type')
                    
                    if message_type == 'join':
                        # Handle user joining
                        nickname = data.get('nickname', 'Anonymous')
                        self.client_nicknames[websocket] = nickname
                        
                        # Send welcome message to the user
                        welcome_msg = {
                            'type': 'system',
                            'text': f'Welcome to the chat, {nickname}!',
                            'timestamp': datetime.now().strftime('%H:%M:%S')
                        }
                        await websocket.send(json.dumps(welcome_msg))
                        
                        # Send recent messages to new user
                        for msg in self.messages[-10:]:  # Last 10 messages
                            await websocket.send(json.dumps(msg))
                        
                        # Broadcast join notification
                        await self.broadcast_system_message(f"{nickname} joined the chat")
                        
                        # Send updated user list
                        await self.send_user_list()
                        
                    elif message_type == 'message':
                        # Handle chat message
                        nickname = self.client_nicknames.get(websocket, 'Anonymous')
                        text = data.get('text', '')
                        
                        if text.strip():
                            message = {
                                'type': 'message',
                                'nickname': nickname,
                                'text': text,
                                'timestamp': datetime.now().strftime('%H:%M:%S')
                            }
                            
                            # Store message in history
                            self.messages.append(message)
                            if len(self.messages) > 100:  # Keep last 100 messages
                                self.messages = self.messages[-100:]
                            
                            # Broadcast to all clients including sender
                            await self.broadcast_message(message)
                            await websocket.send(json.dumps(message))
                            
                    elif message_type == 'typing':
                        # Handle typing indicator
                        nickname = self.client_nicknames.get(websocket, 'Anonymous')
                        typing_msg = {
                            'type': 'typing',
                            'nickname': nickname,
                            'is_typing': data.get('is_typing', False)
                        }
                        await self.broadcast_message(typing_msg, sender=websocket)
                        
                except json.JSONDecodeError:
                    print(f"[ERROR] Invalid JSON received")
                except Exception as e:
                    print(f"[ERROR] Error handling message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
            await self.send_user_list()
    
    async def handle_http(self, request):
        """Handle HTTP requests for health check and basic info"""
        return web.json_response({
            'status': 'running',
            'websocket_port': self.ws_port,
            'connected_users': len(self.clients),
            'users': list(self.client_nicknames.values())
        })
    
    async def start_websocket_server(self):
        """Start the WebSocket server"""
        print(f"[SERVER] WebSocket server starting on {self.host}:{self.ws_port}")
        async with websockets.serve(self.handle_websocket, self.host, self.ws_port):
            print(f"[SERVER] WebSocket server is running and waiting for connections...")
            await asyncio.Future()  # Run forever
    
    async def start_http_server(self):
        """Start the HTTP server for health checks"""
        app = web.Application()
        
        # Configure CORS
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })
        
        # Add routes
        resource = cors.add(app.router.add_resource("/"))
        cors.add(resource.add_route("GET", self.handle_http))
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.http_port)
        
        print(f"[SERVER] HTTP server starting on {self.host}:{self.http_port}")
        await site.start()
        print(f"[SERVER] HTTP server is running")
    
    async def start(self):
        """Start both servers"""
        print(f"[SERVER] Starting chat servers...")
        
        # Start both servers concurrently
        await asyncio.gather(
            self.start_websocket_server(),
            self.start_http_server()
        )

if __name__ == "__main__":
    server = SimpleChatServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n[SERVER] Server stopped.")