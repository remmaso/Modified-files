#!/usr/bin/env python3
import websocket
import json
import time

def test_websocket():
    print("🧪 Testing WebSocket connection...")
    
    try:
        # Create WebSocket connection
        ws = websocket.create_connection("ws://localhost:8765")
        print("✅ WebSocket connected successfully!")
        
        # Send join message
        join_msg = {"type": "join", "nickname": "TestUser"}
        ws.send(json.dumps(join_msg))
        print("📤 Sent join message")
        
        # Listen for response
        response = ws.recv()
        print(f"📨 Received: {response}")
        
        # Send test message
        test_msg = {"type": "message", "text": "Hello from test!"}
        ws.send(json.dumps(test_msg))
        print("📤 Sent test message")
        
        # Get response
        response = ws.recv()
        print(f"📨 Received: {response}")
        
        # Close connection
        ws.close()
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_websocket()