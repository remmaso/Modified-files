# 🔧 WebSocket Connection Troubleshooting Guide

## 🚨 Problem: "Disconnected" Status in Frontend

If you're seeing "Disconnected" in the chat interface, here's how to fix it:

## 🔍 Quick Diagnosis

### Step 1: Check Server Status
```bash
# Check if servers are running
curl http://localhost:8081/
# Should show: {"status": "running", "websocket_port": 8765, "connected_users": 0, "users": []}
```

### Step 2: Check Ports
```bash
# Check if ports are in use
lsof -i :8765  # WebSocket port
lsof -i :8081  # HTTP port
```

### Step 3: Check Server Logs
```bash
# View server logs
cat simple_server.log
```

## 🎯 Common Issues & Solutions

### Issue 1: WebSocket URL Problems
**Symptoms:** 
- Frontend loads but shows "Disconnected"
- Browser console shows WebSocket connection failed

**Solutions:**

#### Option A: Use Local Connection (Recommended for Testing)
1. **Access via localhost:** http://localhost:8081
2. **The WebSocket will connect to:** ws://localhost:8765
3. **This bypasses proxy issues**

#### Option B: Fix WebSocket Proxy Issues
The proxy service might not properly forward WebSocket connections. Use local access instead.

### Issue 2: Server Not Running
**Symptoms:**
- Cannot access http://localhost:8081
- Connection refused errors

**Solution:**
```bash
# Kill any existing servers
kill $(cat simple_server_pid.txt) 2>/dev/null || true

# Start the server
python3 chat_server_simple.py > simple_server.log 2>&1 &
echo $! > simple_server_pid.txt

# Check logs
tail -f simple_server.log
```

### Issue 3: Port Conflicts
**Symptoms:**
- "Address already in use" errors
- Server fails to start

**Solution:**
```bash
# Find processes using ports
lsof -i :8765
lsof -i :8081

# Kill conflicting processes
kill <PID>
```

## 🚀 Working Configuration

### Local Access (Most Reliable)
1. **Start Server:**
```bash
python3 chat_server_simple.py
```

2. **Access Frontend:**
```
http://localhost:8081
```

3. **WebSocket Connection:**
```
ws://localhost:8765
```

### Server Status Check
```bash
# Test HTTP endpoint
curl http://localhost:8081/

# Test WebSocket (advanced)
wscat -c ws://localhost:8765
```

## 📋 Step-by-Step Fix

### For Local Development:
1. **Ensure server is running:**
```bash
python3 chat_server_simple.py
```

2. **Access locally:**
```
http://localhost:8081
```

3. **Test connection:**
- Open browser console (F12)
- Check for WebSocket connection messages
- Look for "WebSocket connected successfully!"

### For Remote/Proxy Access:
1. **Verify proxy supports WebSocket:**
   - Many proxy services don't support WebSocket forwarding
   - Use local access for testing instead

2. **Check CORS settings:**
   - The server includes proper CORS headers
   - Should work with most proxy configurations

## 🔧 Advanced Debugging

### Browser Console Debugging
```javascript
// In browser console
const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => console.log('✅ Connected!');
ws.onerror = (e) => console.error('❌ Error:', e);
ws.onclose = () => console.log('🔌 Disconnected');
```

### Test WebSocket Directly
Create a simple test file:

```html
<!DOCTYPE html>
<html>
<body>
<script>
const ws = new WebSocket('ws://localhost:8765');
ws.onopen = () => {
    console.log('Connected!');
    ws.send(JSON.stringify({type: 'join', nickname: 'TestUser'}));
};
ws.onmessage = (e) => console.log('Message:', e.data);
</script>
</body>
</html>
```

## ✅ Verification Steps

1. **Server responds to HTTP:**
```bash
curl http://localhost:8081/
```

2. **WebSocket accepts connections:**
   - Use the test HTML file above
   - Or use browser console

3. **Frontend loads properly:**
   - Access http://localhost:8081
   - Check browser console for errors

4. **Full functionality works:**
   - Join with nickname
   - Send messages
   - See other users

## 🎯 Recommended Approach

### For Immediate Use:
1. **Use local access:** http://localhost:8081
2. **This avoids all proxy issues**
3. **Perfect for testing and development**

### For Production:
1. **Set up proper WebSocket proxying**
2. **Use nginx or similar for WebSocket support**
3. **Ensure SSL/TLS certificates for wss://**

## 🚨 Current Status

**The servers are running:**
- ✅ HTTP Server: http://localhost:8081
- ✅ WebSocket Server: ws://localhost:8765
- ✅ Both responding to requests

**Recommended access method:**
```
http://localhost:8081
```

## 💡 Pro Tips

1. **Always check server logs first**
2. **Use local access for reliable testing**
3. **Browser console is your friend (F12)**
4. **WebSocket issues are usually proxy-related**
5. **Localhost bypasses most network issues**

---

**The chat application is working! Use http://localhost:8081 for the most reliable experience.**