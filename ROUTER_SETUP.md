# HAL Query Router - Intelligent Request Routing

## 🎯 Overview

The Query Router intelligently routes requests to appropriate handlers:

- **Home Assistant** - Smart home control (lights, temperature, scenes)
- **Database** - QM database queries (patients, appointments, records)
- **LLM** - General queries via Ollama/OpenAI/Claude

## 📋 Architecture

```
User Query
    ↓
Voice Gateway
    ↓
Query Router (intent detection)
    ↓
    ├─→ Home Assistant Handler (smart home)
    ├─→ Database Handler (QM queries)
    └─→ LLM Handler (general AI)
```

## 🔧 Configuration

### 1. Edit Configuration File

Edit: `config/router_config.json`

```json
{
  "llm": {
    "provider": "ollama",
    "ollama": {
      "url": "http://10.1.10.20:11434",
      "model": "llama3.2:latest"
    },
    "openai": {
      "api_key": "sk-...",
      "model": "gpt-4"
    },
    "claude": {
      "api_key": "sk-ant-...",
      "model": "claude-3-sonnet-20240229"
    }
  },
  "home_assistant": {
    "url": "http://homeassistant.local:8123",
    "token": "YOUR_HA_TOKEN",
    "enabled": true
  },
  "database": {
    "enabled": true,
    "default_account": "HAL"
  }
}
```

### 2. Set Environment Variables (Optional)

```powershell
# For OpenAI
$env:OPENAI_API_KEY = "sk-..."

# For Claude
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# For Home Assistant
$env:HA_URL = "http://homeassistant.local:8123"
$env:HA_TOKEN = "your_long_lived_access_token"
```

### 3. Choose LLM Provider

In `router_config.json`, set:
```json
"provider": "ollama"    # or "openai" or "claude"
```

## 🎤 Example Queries

### Home Assistant Commands
```
"turn on the living room lights"
"set temperature to 72 degrees"
"turn off all lights"
"activate movie scene"
"dim the bedroom lights"
```

### Database Queries
```
"find patient named John Smith"
"how many appointments do we have"
"list all patients"
"show appointments for today"
"count medications"
```

### General LLM Queries
```
"tell me a joke"
"what is the capital of France"
"explain quantum computing"
"write a haiku about coffee"
"what's the weather like" (if no weather API configured)
```

### Built-in Queries (No LLM needed)
```
"what time is it"
"what's the date"
"hello"
```

## 🧪 Testing

### Test the Router

```powershell
cd C:\qmsys\hal
python test_router.py
```

This tests all query types and shows routing decisions.

### Test Individual Handlers

```powershell
# Test LLM Handler
python -c "import sys; sys.path.insert(0,'PY'); from llm_handler import *; print(query_ollama('tell me a joke', {'url':'http://10.1.10.20:11434','model':'llama3.2:latest'}, None))"

# Test Home Assistant
python -c "import sys; sys.path.insert(0,'PY'); from home_assistant_handler import *; print(parse_ha_intent('turn on living room lights'))"

# Test Database Handler
python -c "import sys; sys.path.insert(0,'PY'); from database_handler import *; print(parse_database_query('find patient named John'))"
```

## 🔄 Restart Services

After configuration changes, restart Voice Gateway:

```powershell
# Stop Voice Gateway
Stop-Process -Name python -Force

# Start Voice Gateway
Start-Process -FilePath "python" -ArgumentList "C:\qmsys\hal\PY\voice_gateway.py" -WindowStyle Hidden
```

## 📊 Intent Detection Patterns

### Home Assistant Patterns
- `turn on|turn off|switch|toggle|dim|brighten|set`
- `light|lights|lamp|switch|plug`
- `door|window|garage|blinds|curtain`
- `temperature|thermostat|climate|heat|cool`
- `play|pause|stop|volume|music|media|tv`
- `scene|automation`

### Database Patterns
- `find|search|lookup|get|show|list|retrieve`
- `patient|customer|record|person|appointment`
- `medication|allergy|vital|diagnosis`
- `how many|count|total`
- `query|database|system|records`

### LLM (Default)
- Everything else routes to LLM
- Questions, creative requests, general knowledge
- Maintains conversation context

## 🛠️ Extending the Router

### Add New Handler

1. Create handler file in `PY/`:
   ```python
   def handle_my_service(query: str, config: Dict, session_id: str) -> Dict:
       return {'text': 'response', 'status': 'success'}
   ```

2. Add patterns to `query_router.py`:
   ```python
   self.my_service_patterns = [
       r'\bmy pattern\b',
   ]
   ```

3. Update `detect_intent()` method
4. Update `route_query()` method
5. Add config to `router_config.json`

## 🔐 Security Notes

- **Never commit API keys** to git
- Use environment variables for sensitive data
- Store `router_config.json` outside git if it contains secrets
- Add to `.gitignore`: `config/router_config.json`

## 📝 Current Status

**Implemented:**
- ✅ Query router with intent detection
- ✅ LLM handler (Ollama/OpenAI/Claude)
- ✅ Home Assistant handler
- ✅ Database handler
- ✅ Voice Gateway integration
- ✅ Configuration system
- ✅ Test suite

**To Configure:**
1. Set LLM provider (Ollama ready at 10.1.10.20:11434)
2. Add Home Assistant token (if using HA)
3. Configure OpenAI/Claude keys (if using those)
4. Restart Voice Gateway

## 🚀 Quick Start

**Minimal setup (Ollama only):**
```powershell
# Ollama should be running at 10.1.10.20:11434
# No other configuration needed!

# Restart Voice Gateway
Stop-Process -Name python -Force
Start-Process -FilePath "python" -ArgumentList "C:\qmsys\hal\PY\voice_gateway.py" -WindowStyle Hidden

# Test from client
python simple_gui.py
# Type: "tell me a joke"
```

**The router is ready to use!** 🎉

---

**Updated:** 2025-12-03  
**Status:** Ready for testing  
**Default LLM:** Ollama (llama3.2:latest)
