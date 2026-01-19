# Frontend Port Configuration

## Default Configuration

The frontend is configured to run on **port 3000** by default.

## If Port 3000 is Busy

You have multiple options:

### Option 1: Let React Prompt You
When you run `npm start` and port 3000 is busy, React will automatically ask:
```
? Something is already running on port 3000. Would you like to run the app on another port instead? (Y/n)
```
Type `Y` to use port 3001 automatically.

### Option 2: Use Alternative Port Scripts
Run the frontend on a specific port:

```bash
# Run on port 3001
cd frontend
npm run start:3001

# Run on port 3002
cd frontend
npm run start:3002
```

From root folder:
```bash
# Run backend + frontend on port 3001
npm run frontend:3001

# Run backend + frontend on port 3002
npm run frontend:3002
```

### Option 3: Set Custom Port in .env
Edit `frontend/.env` and change:
```
PORT=3000
```
to any port you want:
```
PORT=3005
```

### Option 4: One-Time Port Change
**Windows (PowerShell):**
```powershell
cd frontend
$env:PORT=3005; npm start
```

**Windows (CMD):**
```cmd
cd frontend
set PORT=3005 && npm start
```

**Linux/Mac:**
```bash
cd frontend
PORT=3005 npm start
```

## Browser Auto-Open Disabled

The frontend won't automatically open your browser. To access it:
- **Port 3000**: http://localhost:3000
- **Port 3001**: http://localhost:3001
- **Port 3002**: http://localhost:3002

You can manually open the URL shown in the terminal after the frontend starts.

## Install Required Package

First time setup:
```bash
cd frontend
npm install
```

This will install `cross-env` which allows the port settings to work on all platforms (Windows/Mac/Linux).
