#!/usr/bin/env python3
"""
Test script for the chat application
"""
import socket
import time

def test_connection():
    """Test basic connection to server"""
    print("Testing connection to chat server...")
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5555))
        
        # Wait for NICKNAME request
        message = client.recv(1024).decode('utf-8')
        if message == 'NICKNAME':
            print("✓ Server requested nickname")
            client.send('TestUser'.encode('utf-8'))
            
            # Wait for welcome message
            welcome = client.recv(1024).decode('utf-8')
            print(f"✓ Received: {welcome}")
            
            # Send a test message
            client.send('TestUser: Hello from test script!'.encode('utf-8'))
            print("✓ Sent test message")
            
            time.sleep(1)
            client.close()
            print("✓ Connection test passed!")
            return True
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Chat Application Test Suite")
    print("=" * 50)
    test_connection()
    print("=" * 50)
    print("Test completed!")