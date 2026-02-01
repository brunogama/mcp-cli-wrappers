# /test-wrapper - Validate CLI Wrapper

Test a CLI wrapper through all 4 progressive disclosure levels.

## Usage

```bash
/test-wrapper crawl4ai
/test-wrapper github
/test-wrapper WRAPPER_NAME
```

## What This Command Does

1. Verify wrapper exists
2. Test Level 1: `--help`
3. Test Level 2: `list` and `info` for first function
4. Test Level 3: `example` for first function
5. Test Level 4: `FUNCTION --help`
6. Optionally test `--discover` (MCP introspection)
7. Report results

## Test Sequence

### Step 1: Verify Wrapper Exists
```bash
ls -la ~/cli-wrappers/$ARGUMENTS.py
```

### Step 2: Test Level 1 (Quick Help)
```bash
cd ~/cli-wrappers
timeout 10 uv run $ARGUMENTS.py --help
```
Expected: Quick overview, function list, ~10-15 lines

### Step 3: Test Level 2a (List Functions)
```bash
timeout 10 uv run $ARGUMENTS.py list
```
Expected: All functions listed with descriptions

### Step 4: Test Level 2b (Function Info)
```bash
# Get first function name from list, then:
timeout 10 uv run $ARGUMENTS.py info FIRST_FUNCTION
```
Expected: Full signature, parameters, returns

### Step 5: Test Level 3 (Examples)
```bash
timeout 10 uv run $ARGUMENTS.py example FIRST_FUNCTION
```
Expected: 2-3 working examples

### Step 6: Test Level 4 (Full Reference)
```bash
timeout 10 uv run $ARGUMENTS.py FIRST_FUNCTION --help
```
Expected: Complete argparse reference

### Step 7: Test MCP Discovery (Optional)
```bash
timeout 30 uv run $ARGUMENTS.py --discover
```
Expected: Live tool list from MCP server (may fail if server not running)

## Success Criteria

- [ ] Level 1: Returns without error, shows functions
- [ ] Level 2a: Lists all functions
- [ ] Level 2b: Shows detailed info for a function
- [ ] Level 3: Shows working examples
- [ ] Level 4: Shows argparse help
- [ ] JSON output is valid: `uv run $ARGUMENTS.py list --format json | jq .`

## Batch Testing All Wrappers

```bash
cd ~/cli-wrappers
for wrapper in crawl4ai firecrawl ref repomix deepwiki github semly gitmcp sequential-thinking claude-flow flow-nexus; do
  echo "=== Testing $wrapper ==="
  timeout 10 uv run "$wrapper.py" --help >/dev/null 2>&1 && echo "OK: $wrapper" || echo "FAIL: $wrapper"
done
```

## Troubleshooting

### Wrapper Not Found
```bash
ls ~/cli-wrappers/*.py
```

### Timeout
```bash
# Increase timeout
timeout 30 uv run $ARGUMENTS.py --help
```

### MCP Server Not Running
```bash
# Check MCP configuration
claude mcp list

# Test without --discover
uv run $ARGUMENTS.py list
```
