# Python Chat Application

A simple real-time chat application built with Python using socket programming. This application allows multiple users to connect to a central server and chat with each other in real-time.

## Features

- **Multi-user support**: Multiple clients can connect simultaneously
- **Real-time messaging**: Messages are broadcast instantly to all connected users
- **User nicknames**: Each user can set their own nickname
- **Connection notifications**: Users are notified when someone joins or leaves
- **Simple commands**: Built-in commands for help and quitting
- **Thread-based**: Uses threading for handling multiple connections

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

1. Clone or download this repository
2. No additional installation required - uses Python standard library only

## Usage

### Starting the Server

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run the server:

```bash
python chat_server.py
```

The server will start listening on `127.0.0.1:5555` by default.

You should see:
```
[SERVER] Server is listening on 127.0.0.1:5555
[SERVER] Waiting for connections...
```

### Connecting Clients

1. Open a new terminal/command prompt (keep the server running)
2. Navigate to the project directory
3. Run the client:

```bash
python chat_client.py
```

4. Enter your nickname when prompted
5. Start chatting!

You can open multiple terminals to simulate multiple users chatting.

### Custom Host and Port

To connect to a different host or port:

```bash
python chat_client.py <host> <port>
```

Example:
```bash
python chat_client.py 192.168.1.100 8888
```

## Commands

While in the chat, you can use these commands:

- `/help` - Display available commands
- `/quit` - Exit the chat application

## How It Works

### Server (`chat_server.py`)

- Creates a socket server that listens for incoming connections
- Accepts multiple client connections using threading
- Broadcasts messages from one client to all other connected clients
- Manages client nicknames and connection status
- Handles client disconnections gracefully

### Client (`chat_client.py`)

- Connects to the server using socket
- Uses two threads:
  - One for receiving messages from the server
  - One for sending messages to the server
- Formats messages with the user's nickname
- Handles server disconnections

## Example Session

**Server Terminal:**
```
[SERVER] Server is listening on 127.0.0.1:5555
[SERVER] Waiting for connections...
[SERVER] Connected with ('127.0.0.1', 54321)
[SERVER] Nickname of client is Alice
[SERVER] Connected with ('127.0.0.1', 54322)
[SERVER] Nickname of client is Bob
```

**Client 1 (Alice):**
```
Enter your nickname: Alice
[CLIENT] Connecting to 127.0.0.1:5555...
[CLIENT] Connected successfully!

=== Welcome to the Chat Room ===
Type your messages and press Enter to send
Type /help for available commands
Type /quit to exit
================================

[SERVER] Connected to the server!
[SERVER] Bob joined the chat!
Hello everyone!
Bob: Hi Alice!
```

**Client 2 (Bob):**
```
Enter your nickname: Bob
[CLIENT] Connecting to 127.0.0.1:5555...
[CLIENT] Connected successfully!

=== Welcome to the Chat Room ===
Type your messages and press Enter to send
Type /help for available commands
Type /quit to exit
================================

[SERVER] Connected to the server!
Alice: Hello everyone!
Hi Alice!
```

## Architecture

```
┌─────────────┐
│   Server    │
│  (Port 5555)│
└──────┬──────┘
       │
       ├──────────┬──────────┬──────────┐
       │          │          │          │
   ┌───▼───┐  ┌──▼────┐  ┌──▼────┐  ┌──▼────┐
   │Client1│  │Client2│  │Client3│  │Client4│
   │(Alice)│  │ (Bob) │  │(Carol)│  │(Dave) │
   └───────┘  └───────┘  └───────┘  └───────┘
```

## Troubleshooting

### "Connection refused" error
- Make sure the server is running before starting clients
- Check that you're using the correct host and port
- Verify no firewall is blocking the connection

### Messages not appearing
- Check your network connection
- Ensure the server is still running
- Try restarting both server and client

### Port already in use
- Another application might be using port 5555
- Modify the port in both server and client code
- Or specify a different port when running

## Limitations

- Currently supports text messages only
- No message history (messages are not saved)
- No private messaging between users
- No authentication or security features
- Designed for local network use

## Future Enhancements

Possible improvements for this chat application:

- Add encryption for secure communication
- Implement private messaging
- Add message history/logging
- Create a GUI interface
- Add file sharing capabilities
- Implement user authentication
- Add chat rooms/channels
- Support emojis and rich text

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork this project and submit pull requests for any improvements!