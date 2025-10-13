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

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
QMHOME=/path/to/qm
EMAIL_SERVER=your_email_server
EMAIL_USER=your_email
EMAIL_PASSWORD=your_password
```

3. Initialize the OpenQM database structure:
```bash
python -m core.initialize_db
```

## Usage

1. Start the assistant:
```bash
python -m core.assistant
```

2. Interact through voice:
```python
assistant = AIAssistant(config)
response = await assistant.handle_voice_input()
await assistant.respond_with_voice(response)
```

3. Add new skills:
```python
skill_data = {
    "name": "weather_check",
    "api_endpoint": "weather_api_url",
    "parameters": ["location", "date"]
}
assistant.learn_new_skill("weather_check", skill_data)
```

## Extending the System

The assistant is designed to be modular and extensible. New capabilities can be added by:

1. Creating new skill modules in the `skills/` directory
2. Registering them with the skill registry
3. Training or fine-tuning models for specific tasks
4. Adding new OpenQM files for specialized data storage

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.
