# Quick Start Guide

## Test the Chat Application in 3 Easy Steps

### Step 1: Start the Server

Open a terminal and run:
```bash
python3 chat_server.py
```

You should see:
```
[SERVER] Server is listening on 127.0.0.1:5555
[SERVER] Waiting for connections...
```

### Step 2: Start First Client

Open a **new terminal** and run:
```bash
python3 chat_client.py
```

Enter a nickname (e.g., "Alice") when prompted.

### Step 3: Start Second Client (Optional)

Open **another new terminal** and run:
```bash
python3 chat_client.py
```

Enter a different nickname (e.g., "Bob") when prompted.

Now you can chat between the clients!

## Quick Test

If you just want to verify the application works, run:
```bash
python3 test_chat.py
```

This will automatically test the connection and messaging.

## Example Chat Session

**Terminal 1 (Server):**
```
python3 chat_server.py
[SERVER] Server is listening on 127.0.0.1:5555
[SERVER] Waiting for connections...
```

**Terminal 2 (Client 1):**
```
python3 chat_client.py
Enter your nickname: Alice
[CLIENT] Connected successfully!
Hello everyone!
```

**Terminal 3 (Client 2):**
```
python3 chat_client.py
Enter your nickname: Bob
[CLIENT] Connected successfully!
Alice: Hello everyone!
Hi Alice!
```

## Stopping the Application

- **Clients**: Type `/quit` or press `Ctrl+C`
- **Server**: Press `Ctrl+C`

## Troubleshooting

If you get "Connection refused":
1. Make sure the server is running first
2. Check that port 5555 is not blocked
3. Verify you're using the correct host/port

If port 5555 is already in use:
```bash
# Find the process using port 5555
lsof -i :5555

# Kill it (replace PID with actual process ID)
kill <PID>
```

## Have Fun Chatting! 🎉