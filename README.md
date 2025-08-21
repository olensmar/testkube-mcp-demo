# Testkube MCP Server Demo

A demonstration of AI-powered test failure analysis using Testkube MCP Server with GitHub Copilot.

## 🎯 What This Demo Shows

### Testkube MCP Server

- Natural language interaction with your Kubernetes testing infrastructure
- Direct test execution from VSCode via conversational AI
- Automatic collection of test results, logs, and failure details

### GitHub Copilot Agent mode

- Contextual analysis of test failures using your source code
- Intelligent correlation between test results and application logic
- Code-level root cause identification with precise line numbers
- Automated fix suggestions and PR creation assistance

### The Complete AI Workflow

1. **Execute**: Run TestWorkflows using natural language commands
2. **Analyze**: AI examines test failure patterns and error messages  
3. **Correlate**: AI scans your source code to find the exact bug
4. **Suggest**: AI recommends specific code changes needed
5. **Automate**: AI helps create PRs with the proposed fixes

## 🛠️ Tech Stack

- **Testkube MCP Server**: Test execution and analysis
- **GitHub Copilot Pro**: AI assistant in agent mode
- **VSCode**: Development environment
- **Kubernetes**: Container platform
- **Calculator Service**: Simple Flask app with an intentional bug

## 🐛 The Bug

The calculator's `/add` endpoint multiplies instead of adding:

```python
# Bug in app.py
def add(a, b):
    return a * b  # Should be: return a + b
```

## 🚀 Quick Start

### Deploy the buggy calculator

```bash
kubectl apply -f k8s/
```

### Configure Testkube MCP Server in VSCode

Run the demo with Copilot Agent:

"Can you run testworkflow calculator-addition-test?"

→ Test fails: expected 8, got 15

"Can you find the root cause in my code?"

→ Copilot finds the multiply vs add bug

In app.py, the `add()` function uses
`multiplication (*)` instead of `addition (+)`:

```python
def add(a, b):
            return a * b  # Should be: return a + b
```

"Can you fix this and create a PR?"

→ I'll fix the bug and create a pull request with the
corrected addition function.

## 🔗 Resources

- Blog Post: [Detailed walkthrough and screenshots] - Coming Soon
- Testkube MCP: [https://docs.testkube.io/articles/mcp-overview](https://docs.testkube.io/articles/mcp-overview)
- Calculator Service: fully functional with API endpoints. GitHub repo: [https://github.com/techmaharaj/calculator-service](https://github.com/techmaharaj/calculator-service)