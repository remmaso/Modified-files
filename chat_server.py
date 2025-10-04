import socket
import threading
import sys

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []
        
    def broadcast(self, message, sender_socket=None):
        """Send message to all connected clients except sender"""
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    # Remove client if sending fails
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    nickname = self.nicknames[index]
                    self.nicknames.remove(nickname)
                    self.broadcast(f'[SERVER] {nickname} left the chat!'.encode('utf-8'))
    
    def handle_client(self, client):
        """Handle individual client connection"""
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcast(message, client)
                else:
                    # Client disconnected
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    nickname = self.nicknames[index]
                    self.broadcast(f'[SERVER] {nickname} left the chat!'.encode('utf-8'))
                    self.nicknames.remove(nickname)
                    break
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'[SERVER] {nickname} left the chat!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break
    
    def receive_connections(self):
        """Accept new client connections"""
        while True:
            try:
                client, address = self.server.accept()
                print(f"[SERVER] Connected with {str(address)}")
                
                # Request and store nickname
                client.send('NICKNAME'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
                
                self.nicknames.append(nickname)
                self.clients.append(client)
                
                print(f"[SERVER] Nickname of client is {nickname}")
                self.broadcast(f'[SERVER] {nickname} joined the chat!'.encode('utf-8'))
                client.send('[SERVER] Connected to the server!'.encode('utf-8'))
                
                # Start thread to handle this client
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()
            except:
                break
    
    def start(self):
        """Start the chat server"""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            print(f"[SERVER] Server is listening on {self.host}:{self.port}")
            print("[SERVER] Waiting for connections...")
            self.receive_connections()
        except Exception as e:
            print(f"[ERROR] Failed to start server: {e}")
            sys.exit(1)
    
    def stop(self):
        """Stop the chat server"""
        print("\n[SERVER] Shutting down server...")
        for client in self.clients:
            client.close()
        self.server.close()

if __name__ == "__main__":
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print("[SERVER] Server stopped.")