# /think - Sequential Thinking for Complex Problems

Use extended thinking for systematic problem-solving.

## Usage

```bash
/think "your complex question"
/think "problem statement" --depth detailed
/think --help
```

## What This Command Does

1. Accept complex question or problem
2. Engage sequential thinking process
3. Break problem into steps
4. Provide reasoned solution
5. Show step-by-step analysis

## Progressive Disclosure Levels

### Level 1: Quick Help
```bash
uv run sequential-thinking.py --help
```

### Level 2: See Function Details
```bash
uv run sequential-thinking.py list

uv run sequential-thinking.py info sequentialthinking
```

### Level 3: Working Examples
```bash
uv run sequential-thinking.py example sequentialthinking
```

### Level 4: Complete Reference
```bash
uv run sequential-thinking.py sequentialthinking --help
```

## When to Use Sequential Thinking

### Problem Solving
```bash
# Debug complex issue
/think "Why is my async code hanging?"

# Design decision
/think "Should I use Redis or in-memory cache?"

# Architecture planning
/think "How should I structure my monorepo?"
```

### Learning & Research
```bash
# Understand concept
/think "Explain database transactions and ACID properties"

# Compare approaches
/think "Pros and cons of REST vs GraphQL vs gRPC"

# Technical analysis
/think "How does OAuth2 authentication flow work?"
```

### Code Review & Optimization
```bash
# Performance analysis
/think "Why is my database query slow and how to optimize?"

# Refactoring strategy
/think "How to safely refactor this legacy module?"

# Security concerns
/think "What are the security implications of my API design?"
```

## Using Sequential Thinking

### Basic Usage
```bash
# Ask a complex question
uv run sequential-thinking.py sequentialthinking "your question here"

# The tool will:
# 1. Break down the problem
# 2. Reason through each part
# 3. Provide systematic analysis
# 4. Give reasoned conclusion
```

### Complex Problem Example
```bash
# System design question
uv run sequential-thinking.py sequentialthinking \
  "Design a real-time notification system that handles 1M concurrent users"

# The tool will think through:
# 1. Requirements analysis
# 2. Architecture options
# 3. Trade-offs
# 4. Implementation approach
# 5. Scalability considerations
```

### Multi-Part Questions
```bash
# Question with multiple aspects
uv run sequential-thinking.py sequentialthinking \
  "I have a Python web app that's slow. It uses:
   - Flask for routing
   - PostgreSQL for database
   - Redis for caching
   What should I optimize first?"

# The tool analyzes each component systematically
```

## Integration with Other Tools

### Combine with Repository Analysis
```bash
# Analyze repo
uv run repomix.py pack_codebase ~/my-project > project.txt

# Ask thinking about it
uv run sequential-thinking.py sequentialthinking \
  "Based on this project structure, suggest improvements: [paste content]"
```

### Code Review with Thinking
```bash
# Get code
uv run github.py get_file_contents --repo owner/repo --path "src/main.py" > main.py

# Ask for analysis
uv run sequential-thinking.py sequentialthinking \
  "Review this code for: 1) Performance 2) Security 3) Maintainability: [paste code]"
```

### Architecture Discussion
```bash
# Search for patterns
uv run semly.py outline ~/my-project > structure.txt

# Discuss systematically
uv run sequential-thinking.py sequentialthinking \
  "Given this architecture, how should we implement caching? [paste structure]"
```

## Output Formats

### Structured Thinking
```bash
# Get full analysis
uv run sequential-thinking.py sequentialthinking "your question"

# Returns:
# - Problem breakdown
# - Step-by-step reasoning
# - Considered alternatives
# - Recommended approach
# - Implementation notes
```

### JSON Output
```bash
# Machine-readable format
uv run sequential-thinking.py sequentialthinking "your question" --format json

# Parse results
uv run sequential-thinking.py sequentialthinking "query" --format json | jq '.reasoning'
```

### Text Format
```bash
# Human-readable analysis
uv run sequential-thinking.py sequentialthinking "your question" --format text
```

## Example Workflows

### Debugging Session
```bash
# Problem: Performance issue
QUESTION="My Django app loads users page in 5 seconds. It shows 100 users with their profiles. Database has 50K users. What should I optimize?"

uv run sequential-thinking.py sequentialthinking "$QUESTION"

# Thinking will consider:
# 1. Database query optimization (N+1 problem?)
# 2. Caching strategies
# 3. Frontend optimization
# 4. Pagination options
# 5. Index strategies
```

### Architecture Review
```bash
# Design decision
QUESTION="We're adding real-time notifications. Should we use:
1. WebSockets with message queue
2. Server-Sent Events (SSE)
3. Polling
4. GraphQL subscriptions

Our app handles 10K concurrent users, needs <1s latency."

uv run sequential-thinking.py sequentialthinking "$QUESTION"

# Thinking will analyze each option's:
# - Scalability
# - Latency characteristics
# - Server resource usage
# - Client-side complexity
# - Fallback options
```

### Migration Planning
```bash
# Complex task planning
QUESTION="We need to migrate from PostgreSQL to MongoDB. We have:
- 2TB of relational data
- 50+ tables with relationships
- Production system (no downtime allowed)
- Team of 5 developers
- 2-month deadline

What's the strategy?"

uv run sequential-thinking.py sequentialthinking "$QUESTION"

# Thinking will consider:
# - Data migration approach
# - Schema redesign
# - Compatibility layer options
# - Testing strategy
# - Rollback planning
```

## Advanced Usage

### Step-by-Step Problem Solving
```bash
# Initial problem statement
PROBLEM="I have deadlocks in my multi-threaded Python application"

# First analysis
uv run sequential-thinking.py sequentialthinking "$PROBLEM"

# Then deeper dive based on results
FOLLOW_UP="I'm using locks on these resources: A, B, C. What's the safest way to prevent deadlocks?"

uv run sequential-thinking.py sequentialthinking "$FOLLOW_UP"
```

### Decision Making Framework
```bash
# Use thinking for important decisions
DECISION="Should we build our own message queue or use RabbitMQ? We need:
- High throughput (1M msg/sec)
- Low latency (<100ms)
- Must be fault-tolerant
- Team knows Python/Rust"

uv run sequential-thinking.py sequentialthinking "$DECISION"
```

### Learning Structured Topics
```bash
# Deep dive into concepts
TOPIC="Explain distributed systems consensus algorithms (Raft, Paxos, etc). When should each be used?"

uv run sequential-thinking.py sequentialthinking "$TOPIC"

# Returns comprehensive explanation with trade-offs
```

## Combining with Research

### Research Then Think
```bash
# Search for information
uv run exa.py search "Kubernetes cluster autoscaling"

# Then think about it
uv run sequential-thinking.py sequentialthinking \
  "Based on the search results, how should we implement autoscaling for our Kubernetes cluster?"
```

### Documentation Search + Thinking
```bash
# Find docs
uv run ref.py search "Python async patterns"

# Deep analysis
uv run sequential-thinking.py sequentialthinking \
  "Explain Python async/await patterns and when to use each approach"
```

## Tips for Better Results

### Be Specific
```bash
# ❌ Vague
/think "My code is slow"

# ✅ Specific
/think "Loading 1000 users with their posts takes 30 seconds. Database query takes 25s, rest is processing. How to optimize?"
```

### Include Context
```bash
# ❌ No context
/think "Should we cache this?"

# ✅ With context
/think "Our API endpoint returns user profiles (name, avatar, stats). Called 10K times/day. Response size 5KB. How should we cache?"
```

### Ask About Trade-offs
```bash
# ✅ Explore alternatives
/think "What are the trade-offs between: 1) Caching in Redis, 2) Database query optimization, 3) Pagination? Which should we do first?"
```

### Multi-Stage Analysis
```bash
# Stage 1: Understand problem
uv run sequential-thinking.py sequentialthinking "What are the root causes of N+1 query problems?"

# Stage 2: Apply to your case
uv run sequential-thinking.py sequentialthinking "I have this query pattern: [show code]. Is it causing N+1?"

# Stage 3: Solution approach
uv run sequential-thinking.py sequentialthinking "For this N+1 issue, what's the best fix for Django ORM?"
```

## Troubleshooting

### Thinking Takes Too Long
```bash
# Simplify question
# Instead of: "Design entire system"
# Ask: "What database should we use?"

uv run sequential-thinking.py sequentialthinking "Should we use PostgreSQL or MongoDB for user data?"
```

### Results Too Long
```bash
# Request summary
uv run sequential-thinking.py sequentialthinking "your question" --format summary

# Or save to file
uv run sequential-thinking.py sequentialthinking "your question" > analysis.txt
```

### Need More Detail
```bash
# Ask follow-up questions
FIRST="Is caching the bottleneck?"
uv run sequential-thinking.py sequentialthinking "$FIRST"

# Then follow up
SECOND="You suggested Redis. How specifically to implement it?"
uv run sequential-thinking.py sequentialthinking "$SECOND"
```

## See Also

- Sequential thinking: `uv run sequential-thinking.py --help`
- Function details: `uv run sequential-thinking.py info sequentialthinking`
- Examples: `uv run sequential-thinking.py example sequentialthinking`
- Full reference: `uv run sequential-thinking.py sequentialthinking --help`
