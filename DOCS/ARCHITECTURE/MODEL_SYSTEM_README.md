# AI Model Management System

A comprehensive system for managing AI models, friendly names, and system prompts in OpenQM.

## Files Created

### 1. MODELS
Master model data file containing technical specifications for each AI model.

**Fields:**
- `MODEL_ID` - Unique identifier (e.g., "gpt-4o", "claude-3-5-sonnet-20241022")
- `MODEL_NAME` - Display name
- `PROVIDER` - Provider name (openai, anthropic, ollama)
- `DATE_RELEASED` - Release date
- `CUTOFF_DATE` - Knowledge cutoff date
- `CONTEXT_WINDOW` - Maximum context window size
- `MAX_OUTPUT` - Maximum output tokens
- `COST_INPUT` - Cost per 1M input tokens
- `COST_OUTPUT` - Cost per 1M output tokens
- `SUPPORTS_VISION` - Y/N
- `SUPPORTS_TOOLS` - Y/N
- `SUPPORTS_STREAMING` - Y/N
- `IS_REASONING` - Y/N (for reasoning models like DeepSeek R1)
- `ENDPOINT` - API endpoint path
- `NOTES` - Additional notes
- `ACTIVE` - Y/N
- `CREATE_DATE` - Record creation date
- `UPDATE_DATE` - Last update date

### 2. MODEL.NAMES
Friendly name mappings and user preferences for models.

**Fields:**
- `FRIENDLY_NAME` - User-friendly name (e.g., "claude-3.5-sonnet")
- `MODEL_ID` - Links to MODELS file
- `SYSTEM_PROMPT_ID` - Links to PROMPTS file
- `BREVITY` - Response length preference (brief, normal, detailed)
- `HUMOR` - Humor level (none, light, normal, high)
- `VOICE_ID` - Voice ID for TTS
- `WAKE_WORDS` - Wake words for voice activation (multivalued)
- `LANGUAGE` - Language code (en, es, fr, etc.)
- `TEMPERATURE` - Temperature setting (0.0-2.0)
- `MAX_TOKENS` - Max tokens override
- `TOP_P` - Top P sampling
- `FREQUENCY_PENALTY` - Frequency penalty
- `PRESENCE_PENALTY` - Presence penalty
- `ACTIVE` - Y/N
- `CREATE_DATE` - Record creation date
- `UPDATE_DATE` - Last update date

### 3. PROMPTS
System prompts library.

**Fields:**
- `PROMPT_ID` - Unique identifier
- `PROMPT_TYPE` - Type (SYSTEM, USER, ASSISTANT)
- `PROMPT_NAME` - Display name
- `PROMPT_TEXT` - The actual prompt text
- `CATEGORY` - Category for organization
- `TAGS` - Tags for searching (multivalued)
- `ACTIVE` - Y/N
- `CREATE_DATE` - Record creation date
- `UPDATE_DATE` - Last update date

## Setup Instructions

### 1. Create the Files and Dictionaries

```
BASIC HAL.BP SETUP.MODEL.SYSTEM
CATALOG HAL.BP SETUP.MODEL.SYSTEM
SETUP.MODEL.SYSTEM
```

This creates:
- MODELS file with 18 fields
- MODEL.NAMES file with 16 fields
- PROMPTS file with 9 fields
- All dictionary definitions
- Indexes on key fields

### 2. Populate with Default Models

```
BASIC HAL.BP POPULATE.MODELS
CATALOG HAL.BP POPULATE.MODELS
POPULATE.MODELS
```

This adds:
- **OpenAI**: gpt-4o, gpt-4-turbo
- **Anthropic**: claude-3-5-sonnet-20241022, claude-3-opus-20240229
- **Ollama**: deepseek-r1:32b

And creates friendly name mappings:
- `gpt-4o` → `gpt-4o`
- `gpt-4` → `gpt-4-turbo`
- `claude-3.5-sonnet` → `claude-3-5-sonnet-20241022`
- `claude-3-opus` → `claude-3-opus-20240229`
- `deepseek-r1:32b` → `deepseek-r1:32b`

### 3. Update ask.ai.b (Optional)

To use the MODEL.NAMES file for automatic mapping:

```
COPY HAL.BP ask.ai.b ask.ai.b.backup
COPY HAL.BP ask.ai.b.new ask.ai.b
BASIC HAL.BP ask.ai.b
CATALOG HAL.BP ask.ai.b
```

## Usage Examples

### Query Models
```
LIST MODELS
LIST MODELS PROVIDER CONTEXT_WINDOW COST_INPUT COST_OUTPUT
SELECT MODELS WITH PROVIDER = "openai"
LIST MODELS
```

### Query Friendly Names
```
LIST MODEL.NAMES
LIST MODEL.NAMES FRIENDLY_NAME MODEL_ID TEMPERATURE
```

### Use Friendly Names
```
ask.b claude-3.5-sonnet write a poem
ask.b gpt-4 explain quantum physics
ask.b deepseek-r1:32b solve 2+2
```

The system automatically maps:
- `claude-3.5-sonnet` → `claude-3-5-sonnet-20241022`
- `gpt-4` → `gpt-4-turbo`

### Add New Prompts
```
BASIC HAL.BP ADD.PROMPT
CATALOG HAL.BP ADD.PROMPT
ADD.PROMPT
```

### Add New Model Names
```
EDIT MODEL.NAMES my-custom-gpt
```

Then set:
- FRIENDLY_NAME: my-custom-gpt
- MODEL_ID: gpt-4o
- TEMPERATURE: 0.9
- BREVITY: brief
- HUMOR: high
- etc.

## Integration with ask.ai.b

The updated `ask.ai.b` now:
1. Looks up the friendly name in MODEL.NAMES
2. Gets the actual MODEL_ID
3. Uses that for the API call
4. Falls back to hardcoded mapping if MODEL.NAMES is unavailable

This allows you to:
- Create custom aliases
- Override model parameters per alias
- Manage all model mappings in one place
- No code changes needed to add new models

## Adding New Models

### Add to MODELS file:
```
EDIT MODELS new-model-id
```

### Add friendly name:
```
EDIT MODEL.NAMES my-friendly-name
```
Set MODEL_ID to link to the MODELS record.

### Test:
```
ask.b my-friendly-name test prompt
```

## Benefits

1. **Centralized Management** - All model data in one place
2. **Flexible Aliases** - Create unlimited friendly names
3. **User Preferences** - Different settings per alias
4. **Easy Updates** - Update model specs without code changes
5. **Cost Tracking** - Track costs per model
6. **Extensible** - Add new fields as needed
7. **Searchable** - Use QM queries to find models
8. **Indexed** - Fast lookups on key fields

## Future Enhancements

- Link SYSTEM_PROMPT_ID to automatically inject system prompts
- Track usage statistics per model
- Cost calculation and reporting
- Model performance metrics
- A/B testing between models
- Automatic model selection based on task type
