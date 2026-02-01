# /new-wrapper - Create New CLI Wrapper

Generate a new CLI wrapper for an MCP server.

## Usage

```bash
/new-wrapper MCP_NAME
/new-wrapper --name mytools --type stdio --command "npx @my/mcp-server"
```

## What This Command Does

1. Gather MCP server information
2. Add definition to `generate-all-wrappers.py`
3. Run generator to create wrapper
4. Test the new wrapper
5. Update documentation

## Step-by-Step Process

### Step 1: Gather MCP Information

Required information:
- **Name**: Short identifier (e.g., `mytools`)
- **Type**: `stdio`, `http`, or `npx`
- **Command**: How to run the MCP server
- **Functions**: List of tool names and descriptions

### Step 2: Add to MCP_DEFINITIONS

Edit `generate-all-wrappers.py`:

```python
MCP_DEFINITIONS["$ARGUMENTS"] = {
    "command": "npx @example/mcp-server",  # or path to server
    "type": "stdio",  # or "http"
    "functions": [
        {"name": "function1", "description": "What it does"},
        {"name": "function2", "description": "What it does"},
    ]
}
```

### Step 3: Generate Wrapper

```bash
cd ~/cli-wrappers
uv run generate-all-wrappers.py
```

### Step 4: Test New Wrapper

```bash
# Level 1: Quick help
uv run $ARGUMENTS.py --help

# Level 2: List functions
uv run $ARGUMENTS.py list

# Try MCP discovery (if server is running)
uv run $ARGUMENTS.py --discover
```

### Step 5: Enhance Wrapper (Optional)

Edit the generated `$ARGUMENTS.py` to add:

1. **Better FUNCTION_INFO** with detailed parameters:
```python
FUNCTION_INFO = {
    "my_function": {
        "description": "Detailed description",
        "parameters": [
            {
                "name": "url",
                "type": "str",
                "required": True,
                "description": "The URL to process"
            }
        ],
        "returns": "Dict with result data",
        "timeout": "30 seconds"
    }
}
```

2. **Working FUNCTION_EXAMPLES**:
```python
FUNCTION_EXAMPLES = {
    "my_function": [
        {
            "title": "Basic usage",
            "command": "uv run $ARGUMENTS.py my_function --url https://example.com",
            "output": '{"success": true, "data": "..."}'
        }
    ]
}
```

3. **Custom validation** if needed

### Step 6: Update Documentation

Update `INDEX.md` to include the new wrapper.

## MCP Types

### stdio (Most Common)
```python
{
    "command": "npx @package/mcp-server",
    "type": "stdio",
    ...
}
```

### HTTP
```python
{
    "command": "https://api.example.com/mcp",
    "type": "http",
    ...
}
```

### Python Module
```python
{
    "command": "uv --directory /path/to/server run main.py",
    "type": "stdio",
    ...
}
```

## Example: Adding a New MCP

```python
# In generate-all-wrappers.py
MCP_DEFINITIONS["weather"] = {
    "command": "npx @example/weather-mcp",
    "type": "stdio",
    "functions": [
        {"name": "get_forecast", "description": "Get weather forecast"},
        {"name": "get_current", "description": "Get current conditions"},
        {"name": "get_alerts", "description": "Get weather alerts"}
    ]
}
```

Then run:
```bash
uv run generate-all-wrappers.py
uv run weather.py --help
uv run weather.py list
```

## Checklist

- [ ] MCP_DEFINITIONS updated
- [ ] Generator ran successfully
- [ ] Level 1 help works
- [ ] Level 2 list works
- [ ] FUNCTION_INFO has detailed docs
- [ ] FUNCTION_EXAMPLES has working examples
- [ ] INDEX.md updated
