# XcodeMCP CLI Wrapper

Control Xcode through the Model Context Protocol with a progressive-disclosure CLI.

## Overview

- **MCP Server**: [lapfelix/XcodeMCP](https://github.com/lapfelix/XcodeMCP)
- **Functions**: 26 tools across 4 categories
- **Stack**: Python 3.10+ with `uv` (PEP 723)

## Quick Start

```bash
cd ~/cli-wrappers/xcode-cli

# Level 1: Quick overview
uv run cli.py --help

# Level 2: List all functions
uv run cli.py list

# Level 2: Detailed function docs
uv run cli.py info xcode_build

# Level 3: Working examples
uv run cli.py example xcode_test
```

## Prerequisites

1. **Xcode** installed on macOS
2. **XcodeMCP server** configured in Claude Desktop:

```json
{
  "mcpServers": {
    "xcode-mcp": {
      "command": "npx",
      "args": ["-y", "@anthropic/xcode-mcp"]
    }
  }
}
```

## Categories

### Project Management
| Function | Description |
|----------|-------------|
| `xcode_open_project` | Open an Xcode project or workspace |
| `xcode_close_project` | Close the active project |
| `xcode_get_workspace_info` | Get workspace status and details |
| `xcode_get_projects` | List projects within a workspace |
| `xcode_open_file` | Open a file at a specific line |
| `xcode_refresh_project` | Close and reopen to refresh |

### Build Operations
| Function | Description |
|----------|-------------|
| `xcode_build` | Build a scheme |
| `xcode_clean` | Clean build directory |
| `xcode_test` | Run tests with options |
| `xcode_build_and_run` | Build and run scheme |
| `xcode_debug` | Start debugging session |
| `xcode_stop` | Stop current operation |
| `find_xcresults` | Find XCResult files |

### Configuration
| Function | Description |
|----------|-------------|
| `xcode_get_schemes` | List available schemes |
| `xcode_set_active_scheme` | Switch active scheme |
| `xcode_get_run_destinations` | List simulators/devices |
| `xcode_get_test_targets` | Get test target info |

### XCResult Analysis
| Function | Description |
|----------|-------------|
| `xcresult_browse` | Browse test results |
| `xcresult_browser_get_console` | Get console output |
| `xcresult_summary` | Quick results overview |
| `xcresult_get_screenshot` | Extract screenshots |
| `xcresult_get_ui_hierarchy` | Get UI hierarchy JSON |
| `xcresult_get_ui_element` | Get UI element details |
| `xcresult_list_attachments` | List test attachments |
| `xcresult_export_attachment` | Export attachments |

## Usage Examples

### List Schemes
```bash
uv run cli.py xcode_get_schemes --xcodeproj /path/to/MyApp.xcodeproj
```

### Build a Project
```bash
uv run cli.py xcode_build \
  --xcodeproj /path/to/MyApp.xcodeproj \
  --scheme MyApp
```

### Build for Specific Destination
```bash
uv run cli.py xcode_build \
  --xcodeproj /path/to/MyApp.xcodeproj \
  --scheme MyApp \
  --destination "iPhone 15 Pro"
```

### Run All Tests
```bash
uv run cli.py xcode_test \
  --xcodeproj /path/to/MyApp.xcodeproj \
  --destination "iPhone 15 Pro"
```

### Run Specific Test Class
```bash
uv run cli.py xcode_test \
  --xcodeproj /path/to/MyApp.xcodeproj \
  --destination "iPhone 15" \
  --selected-test-classes "MyAppTests.LoginTests"
```

### Get Test Results Summary
```bash
uv run cli.py xcresult_summary \
  --xcresult-path /path/to/Test.xcresult
```

### Browse Failed Tests
```bash
uv run cli.py xcresult_browse \
  --xcresult-path /path/to/Test.xcresult \
  --include-console
```

### Get Console Output for Specific Test
```bash
uv run cli.py xcresult_browser_get_console \
  --xcresult-path /path/to/Test.xcresult \
  --test-id 0
```

### Find XCResult Files
```bash
uv run cli.py find_xcresults \
  --xcodeproj /path/to/MyApp.xcodeproj
```

## Output Formats

```bash
# JSON (default)
uv run cli.py xcode_get_schemes --xcodeproj /path/to/MyApp.xcodeproj

# Text
uv run cli.py xcode_get_schemes --xcodeproj /path/to/MyApp.xcodeproj --format text

# Table
uv run cli.py xcode_get_schemes --xcodeproj /path/to/MyApp.xcodeproj --format table
```

## 4-Level Progressive Disclosure

### Level 1: Quick Help (~30 tokens)
```bash
uv run cli.py --help
```
Overview with main functions and quick start examples.

### Level 2: Function List & Info (~150 tokens)
```bash
uv run cli.py list                    # All functions by category
uv run cli.py info xcode_build        # Detailed docs for one function
```

### Level 3: Examples (~200 tokens)
```bash
uv run cli.py example xcode_test
```
Copy-paste ready examples with expected output.

### Level 4: Full Reference (~500 tokens)
```bash
uv run cli.py xcode_test --help
```
Complete argparse documentation.

## Common Workflows

### Full Build Cycle
```bash
# Clean, build, test
uv run cli.py xcode_clean --xcodeproj /path/to/MyApp.xcodeproj
uv run cli.py xcode_build --xcodeproj /path/to/MyApp.xcodeproj --scheme MyApp
uv run cli.py xcode_test --xcodeproj /path/to/MyApp.xcodeproj --destination "iPhone 15"
```

### Analyze Test Failures
```bash
# Find results
uv run cli.py find_xcresults --xcodeproj /path/to/MyApp.xcodeproj

# Get summary
uv run cli.py xcresult_summary --xcresult-path /path/to/Test.xcresult

# Browse failures with console
uv run cli.py xcresult_browse --xcresult-path /path/to/Test.xcresult --include-console
```

### Debug Session
```bash
# Start debugging
uv run cli.py xcode_debug --xcodeproj /path/to/MyApp.xcodeproj --scheme MyApp

# Stop when done
uv run cli.py xcode_stop --xcodeproj /path/to/MyApp.xcodeproj
```

## Troubleshooting

### MCP Connection Failed
Ensure XcodeMCP is configured in Claude Desktop settings:
```json
{
  "mcpServers": {
    "xcode-mcp": {
      "command": "npx",
      "args": ["-y", "@anthropic/xcode-mcp"]
    }
  }
}
```

### Xcode Not Responding
```bash
# Refresh the project
uv run cli.py xcode_refresh_project --xcodeproj /path/to/MyApp.xcodeproj
```

### Build Timeout
Default timeout is 300 seconds. For large projects, operations may take longer.

### Permission Errors
Ensure Xcode has automation permissions in System Preferences > Privacy & Security.

## Contributing

See CLAUDE.md for development guidelines.

## License

MIT
