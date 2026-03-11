# /analyze - Structured Code and Architecture Analysis

Use sequential-thinking-cli for systematic code/architecture analysis.

## Instructions

1. Take the target from $ARGUMENTS (file path, directory, or description)
2. Use the `sequential-thinking` skill in **Analyze** mode
3. First, read the relevant code using Read tool or `uv run repomix.py pack_codebase`
4. Then orchestrate a 5-8 step analysis chain via `uv run sequential-thinking-cli/cli.py sequentialthinking`
5. Cover: structure, quality, performance, security, maintainability
6. Present prioritized recommendations and action plan

If $ARGUMENTS is empty, ask the user what they want to analyze.

## Target

$ARGUMENTS
