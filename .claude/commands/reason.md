# /reason - Deep Multi-Step Reasoning

Use sequential-thinking-cli for deep reasoning with branching and revision support.

## Instructions

1. Take the problem from $ARGUMENTS
2. Use the `sequential-thinking` skill in **Reason** mode
3. Orchestrate a 5-10 step reasoning chain via `uv run sequential-thinking-cli/cli.py sequentialthinking`
4. Use branching (`--branchFromThought`, `--branchId`) to explore competing alternatives
5. Use revision (`--isRevision`, `--revisesThought`) when later analysis contradicts earlier conclusions
6. Present comparison table, recommendation with confidence level, and implementation notes

If $ARGUMENTS is empty, ask the user what they need to reason about.

## Problem

$ARGUMENTS
