# Personal AI Assistant

An advanced AI assistant with persistent memory, voice interaction, and expandable skills. Built on OpenQM for robust data storage and various LLM models for cognitive functions.

## Core Features

- **Persistent Memory**: Stores conversations, learned behaviors, and personal preferences in OpenQM
- **Voice Interaction**: Natural voice input and output
- **Email Integration**: Access and process email content
- **Task Management**: Interface with task lists and calendars
- **Expandable Skills**: Learn and develop new capabilities over time
- **Adaptive Personality**: Personality traits that evolve through interaction
- **Multi-Model Intelligence**: Uses different LLM models optimized for specific tasks

## System Architecture

### Core Components

1. **Memory System (OpenQM-based)**
   - Personal knowledge base
   - Conversation history
   - User preferences
   - Learned behaviors
   - Task history
   - Email integration data
   - Voice interaction logs

2. **Model Selection System**
   - Task classifier
   - Model router
   - Performance tracker
   - Model configuration store

3. **Interface Layer**
   - Voice input/output system
   - Email integration
   - Task list integration
   - Web interface

### Data Structure

OpenQM files:
- MEMORY.STORE: For persistent memory
- USER.PROFILE: Personal information and preferences
- CONVERSATION.HISTORY: Chat logs
- TASK.TRACKER: Task management
- EMAIL.STORE: Email integration
- SKILL.REGISTRY: Learned capabilities
- MODEL.CONFIG: LLM configurations

## Setup

### 1. Configure Environment Variables

The system now uses environment variables for configuration. Run the setup script:

**Option A: PowerShell (Recommended)**

```powershell
cd C:\QMSYS\HAL
.\setup_environment.ps1
```

**Option B: Batch File**

```cmd
cd C:\QMSYS\HAL
setup_environment.bat
```

**Option C: Manual Configuration**

See [CONFIGURATION.md](CONFIGURATION.md) for detailed instructions on setting environment variables manually.

Required variables:

- `HAL_PYTHON_PATH` - Path to Python executable (default: `C:\Python312\python.exe`)
- `HAL_SCRIPT_PATH` - Path to AI handler script (default: `C:\QMSYS\HAL\PY\ai_handler.py`)
- `OLLAMA_HOST` - Ollama server hostname (default: `ubuai.q.lcs.ai`)
- `OLLAMA_PORT` - Ollama server port (default: `11434`)

### 2. Install Python dependencies

```powershell
cd C:\QMSYS\HAL\PY
pip install -r requirements.txt
```

### 3. Configure API Keys in OpenQM

```qm
LOGTO HAL
ED API.KEYS OPENAI
```

Add your OpenAI API key, then:

```qm
ED API.KEYS ANTHROPIC
```

Add your Anthropic API key.

### 4. Set up AI Model System

```qm
BASIC HAL.BP SETUP.MODEL.SYSTEM
CATALOG HAL.BP SETUP.MODEL.SYSTEM
SETUP.MODEL.SYSTEM

BASIC HAL.BP POPULATE.MODELS
CATALOG HAL.BP POPULATE.MODELS
POPULATE.MODELS
```

### 5. Compile and catalog the AI integration

```qm
BASIC HAL.BP ask.b
CATALOG HAL.BP ask.b
BASIC HAL.BP ask.ai.b
CATALOG HAL.BP ask.ai.b
```

## Usage

### 1. Ask AI questions from OpenQM:
```
ask.b what is 2+2
ask.b gpt-4o explain quantum physics
ask.b claude-3.5-sonnet write a poem
ask.b deepseek-r1:32b solve this math problem
```

### 2. Query model information:
```
LIST MODELS
LIST MODEL.NAMES
SELECT MODELS WITH PROVIDER = "openai"
```

### 3. Add custom model aliases:
```
EDIT MODEL.NAMES my-custom-gpt
```
Set FRIENDLY_NAME, MODEL_ID, TEMPERATURE, etc.

### 4. Add system prompts:
```
BASIC HAL.BP ADD.PROMPT
CATALOG HAL.BP ADD.PROMPT
ADD.PROMPT
```

## Extending the System

The assistant is designed to be modular and extensible. New capabilities can be added by:

1. Creating new skill modules in the `skills/` directory
2. Registering them with the skill registry
3. Training or fine-tuning models for specific tasks
4. Adding new OpenQM files for specialized data storage

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.
