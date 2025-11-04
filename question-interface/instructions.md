# Question Interface - Development Instructions

## Overview

This project provides a web interface for viewing questions and to-do lists with a 3D concept cloud visualization. It consists of a FastAPI backend and a React frontend with Three.js.

## Project Structure

```
question-interface/
├── backend/              # FastAPI server
│   ├── main.py          # API endpoints
│   ├── requirements.txt # Python dependencies
│   └── tests/           # Backend unit tests
├── frontend/            # React application
│   ├── src/
│   │   ├── App.jsx      # Main application component
│   │   ├── ConceptCloud.jsx  # 3D visualization
│   │   └── QuestionList.jsx  # Question display
│   └── package.json     # Node dependencies
├── test_integration.py  # Integration tests
└── docker-compose.yml   # Container setup
```

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- VS Code with debugging extensions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd question-interface/backend
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests:
   ```bash
   python -m pytest tests/
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd question-interface/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run tests:
   ```bash
   npm test
   ```

## Running the Application

### Development Mode

1. Start the backend:
   ```bash
   cd question-interface/backend
   source venv/bin/activate
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the frontend (in another terminal):
   ```bash
   cd question-interface/frontend
   npm run dev
   ```

3. Open `http://localhost:5173` in your browser

### Debug Mode

Use VS Code's Run and Debug panel (F5) and select from:
- **"Debug Full Stack - HTTP"** - Standard HTTP development (port 8000)
- **"Debug Full Stack - HTTPS"** - HTTPS with SSL certificates (port 8443)

## HTTPS Support

### Why HTTP vs HTTPS?

**Development (HTTP):**
- ✅ Faster setup and startup
- ✅ No certificate management
- ✅ Browser allows localhost HTTP without warnings
- ✅ Simpler for local development

**Production (HTTPS):**
- 🔒 Encrypted communication
- ✅ Required for modern web security
- ✅ Browser security features enabled

### Using HTTPS Locally

If you want HTTPS in development:

1. **SSL certificates are pre-generated** in the backend directory (`cert.pem`, `key.pem`)

2. **Start with HTTPS debug config:**
   - Use "Debug Full Stack - HTTPS" in VS Code
   - Backend runs on `https://localhost:8443`
   - Frontend runs on `http://localhost:5173`

3. **Browser warnings:** You'll see a "Not Secure" warning since it's self-signed. Click "Advanced" → "Proceed to localhost (unsafe)" to continue.

4. **Manual HTTPS startup:**
   ```bash
   cd question-interface/backend
   source venv/bin/activate
   uvicorn main:app --ssl-keyfile key.pem --ssl-certfile cert.pem --host 0.0.0.0 --port 8443
   ```

### Production HTTPS

For production deployment, use a reverse proxy (nginx) or cloud platform that provides SSL certificates automatically.

## Testing

### Unit Tests

- **Backend**: `cd question-interface/backend && python -m pytest tests/`
- **Frontend**: `cd question-interface/frontend && npm test`

### Integration Tests

Run the integration test script to verify the full system works:

```bash
cd question-interface
python test_integration.py
```

This script:
- Starts the backend server
- Tests all API endpoints
- Verifies data loading from CSV
- Cleans up the server process

### SSL Certificate Tests

Test SSL certificate configuration for HTTPS development:

```bash
cd question-interface
python test_ssl.py
```

This script validates that SSL certificates are properly configured and can be loaded by the server.

## Script Execution Guidelines

### ABSOLUTE RULE: NEVER Use Direct Terminal Commands for Complex Operations

**🚫 STRICTLY FORBIDDEN: Never execute commands with pipes (|), redirection (>, >>), complex shell operations, or multi-step processes directly in the terminal.**

**REASONING:** Direct terminal commands with pipes/redirection are:**
- Not reproducible or version controllable
- Difficult to debug and maintain
- Platform-dependent and error-prone
- Leave no audit trail of what was executed

**EXAMPLES OF COMPLETELY FORBIDDEN COMMANDS:**
```bash
# ❌ ABSOLUTELY NEVER DO THESE:
curl http://localhost:8000 | head -20
npm run dev > /dev/null 2>&1 &
command1 && command2 || command3
ps aux | grep python | grep -v grep
cat file.txt | grep "pattern" | wc -l
```

**✅ ONLY DO THIS INSTEAD:**
```bash
# ✅ Create a script file and execute it
python my_test_script.py
```

### When to Create Scripts (MANDATORY)

**You MUST create a script file for ANY operation that involves:**
- Multiple commands or steps
- Pipes, redirection, or shell operators
- Process management (starting/stopping servers)
- Error handling and cleanup
- Data processing or filtering
- Network requests with output processing
- Any non-trivial operation

### Script Requirements (MANDATORY)

**ALL scripts MUST include:**
1. **Descriptive filename**: `test_api_endpoints.py`, `start_services.py`
2. **Shebang line**: `#!/usr/bin/env python3`
3. **Comprehensive docstring**: Explain purpose, usage, and behavior
4. **Error handling**: Try/except blocks with proper cleanup
5. **Resource cleanup**: Always terminate processes, close connections
6. **Return codes**: `sys.exit(0)` for success, `sys.exit(1)` for failure
7. **Absolute paths**: Use absolute paths to avoid directory issues

### Terminal Command Restrictions (MANDATORY)

**The ONLY terminal commands allowed are:**
- `cd` - Change directory
- `ls` - List files
- `python script.py` - Execute a Python script
- `npm test` - Run npm scripts (single command only)
- `pip install -r requirements.txt` - Install dependencies
- Simple commands without pipes/redirection

**ANYTHING ELSE must be written as a script first.**

### Consequences of Violation

If you execute forbidden terminal commands:
- The operation will fail or behave unpredictably
- Debugging becomes extremely difficult
- The codebase becomes less maintainable
- Future developers will struggle to understand what was done

**ALWAYS create a script instead. This is not optional - it is mandatory.**

## API Endpoints

- `GET /questions` - Get all questions
- `GET /questions/{id}` - Get specific question
- `GET /categories` - Get question categories with counts

## Data Source

Questions are loaded from `../../metaproject-life/data/questions.csv` relative to the backend directory.

## Docker Support

Use Docker Compose for containerized deployment:

```bash
docker-compose up
```

## Troubleshooting

### Backend Issues
- Ensure virtual environment is activated
- Check that CSV file exists at expected path
- Verify all dependencies are installed

### Frontend Issues
- Ensure backend is running on port 8000
- Check CORS settings if API calls fail
- Verify Node.js version compatibility

### Testing Issues
- Run tests from correct directory
- Ensure all dependencies are installed
- Check that ports 8000/5173 are available