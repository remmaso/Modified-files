import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = ""
        self.running = True
        
    def receive_messages(self):
        """Receive messages from server"""
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICKNAME':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("\n[ERROR] Connection to server lost!")
                self.running = False
                self.client.close()
                break
    
    def send_messages(self):
        """Send messages to server"""
        while self.running:
            try:
                message = input('')
                if message.lower() == '/quit':
                    print("[CLIENT] Disconnecting from server...")
                    self.running = False
                    self.client.close()
                    break
                elif message.lower() == '/help':
                    print("\n=== Chat Commands ===")
                    print("/quit - Exit the chat")
                    print("/help - Show this help message")
                    print("=====================\n")
                else:
                    full_message = f'{self.nickname}: {message}'
                    self.client.send(full_message.encode('utf-8'))
            except:
                self.running = False
                self.client.close()
                break
    
    def connect(self):
        """Connect to the chat server"""
        try:
            # Get nickname from user
            self.nickname = input("Enter your nickname: ").strip()
            while not self.nickname:
                print("[ERROR] Nickname cannot be empty!")
                self.nickname = input("Enter your nickname: ").strip()
            
            # Connect to server
            print(f"[CLIENT] Connecting to {self.host}:{self.port}...")
            self.client.connect((self.host, self.port))
            print("[CLIENT] Connected successfully!")
            print("\n=== Welcome to the Chat Room ===")
            print("Type your messages and press Enter to send")
            print("Type /help for available commands")
            print("Type /quit to exit")
            print("================================\n")
            
            # Start threads for receiving and sending
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            
            send_thread = threading.Thread(target=self.send_messages)
            send_thread.start()
            
            # Wait for threads to complete
            send_thread.join()
            receive_thread.join()
            
        except ConnectionRefusedError:
            print(f"[ERROR] Could not connect to server at {self.host}:{self.port}")
            print("[ERROR] Make sure the server is running!")
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # Allow custom host and port via command line arguments
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5555
    
    client = ChatClient(host, port)
    try:
        client.connect()
    except KeyboardInterrupt:
        print("\n[CLIENT] Disconnected.")
        sys.exit(0)