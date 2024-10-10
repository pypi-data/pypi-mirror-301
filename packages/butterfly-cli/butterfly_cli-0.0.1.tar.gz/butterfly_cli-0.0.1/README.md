# Butterfly

Butterfly is a powerful security analysis tool that uses AI agents to analyze your codebase for potential security issues, architectural flaws, performance bottlenecks, and more.

## Installation

You can install Butterfly using pip:

```
pip install butterfly-cli
```

## Configuration

1. Create a `.env` file in the root directory of your project.
2. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

Run Butterfly inside your codebase:

```
butterfly run
```

This command will initiate the analysis using various AI agents, each focusing on different aspects of your codebase.

## Features

- Architecture analysis
- Performance optimization suggestions
- Static code analysis
- Code quality assessment
- Dependency analysis
- And more!

## Disclaimer

This tool uses AI to analyze code and provide suggestions. While it can be a valuable aid in identifying potential issues, it should not be solely relied upon for security audits. Always combine this tool's output with manual review and testing.