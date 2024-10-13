# CodePilot CLI

[![CI](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ci.yml)
[![CD](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/cd.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/cd.yml)
[![Code Format](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/black.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/black.yml)
[![Linter](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ruff.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ruff.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/code-pilot-cli?logo=pypi&logoColor=white)](https://pypi.org/project/code-pilot-cli/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/code-pilot-cli?logo=python&logoColor=white)](https://pypi.org/project/code-pilot-cli/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/code-pilot-cli?logo=pypi&logoColor=white)](https://pypi.org/project/code-pilot-cli/)
[![PyPI - Format](https://img.shields.io/pypi/format/code-pilot-cli?logo=pypi&logoColor=white)](https://pypi.org/project/code-pilot-cli/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/code-pilot-cli?logo=pypi&logoColor=white)](https://pypi.org/project/code-pilot-cli/)
[![PyPI - License](https://img.shields.io/pypi/l/code-pilot-cli?logo=pypi&logoColor=white)](https://pypi.org/project/code-pilot-cli/)

A powerful and customizable code assistant designed for the command line interface (CLI) to help developers automate various coding tasks.

## Interactive Demonstration

We have created a [short interactive demonstration](https://youtu.be/XdwqzXIJ_qc) on how to use the CodePilot CLI, showcasing its features.

[![Interactive Demonstration of CodePilot CLI](https://img.youtube.com/vi/XdwqzXIJ_qc/maxresdefault.jpg)]([https://](https://www.youtube.com/watch?v=XdwqzXIJ_qc))

## Getting Started

To use the CodePilot CLI, you'll need to first install the package using pip:

```bash
pip install code-pilot-cli
```

Next, make sure to export your Hugging Face `HF_TOKEN` as an environment variable. You can obtain your token from [Hugging Face's website](https://huggingface.co/settings/tokens).

For Bash:

```bash
export HF_TOKEN=hf_**********************************
```

For PowerShell:

```powershell
$env:HF_TOKEN = "hf_**********************************"
```

Now you are all set to start using the CodePilot CLI!

## Usage

### Access Help Options

To view available help options, run:

```bash
code-pilot --help
```

### Interact with CodePilot

Engage with CodePilot by providing prompts:

```bash
code-pilot ai 'list all files in the current directory'
```

### Chat with CodePilot

Initiate a conversation with CodePilot and export or import the chat history for future reference:

```bash
code-pilot chat --
```

### Generate Code Completions

Obtain code completions from CodePilot based on the user's input:

```bash
code-pilot completions 'fn add(x: i32, y: i32) -> i32 {'
```

### Generate Documentation

Generate code documentation directly from source files:

```bash
code-pilot document src/main.rs
```

### Enhance Code Quality and Best Practices

Get suggestions on how to improve your code according to best practices:

```bash
code-pilot enhance App.tsx
```

### Perform Code Review

Perform a code review using CodePilot model and receive valuable feedback:

```bash
code-pilot review app/models.py
```

### Perform Code Scanning

Scan your code for potential security vulnerabilities:

```bash
code-pilot scan src/main.rs
```

### Generate Tests

Automatically generate tests based on your source code:

```bash
code-pilot test src/lib.rs
```

### Use Custom Large Language Models (LLMs)

Leverage custom LLMs for enhanced code assistants:

```bash
code-pilot chat -m'mistralai/Mistral-Nemo-Instruct-2407'
```

## License

The CodePilot CLI project is released under the MIT License.
