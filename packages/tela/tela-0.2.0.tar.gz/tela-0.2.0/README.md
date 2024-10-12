# Tela SDK for Python

The Tela SDK for Python provides a simple and powerful way to interact with the Tela API. This SDK allows you to create chat completions, handle file uploads, and manage various resources with ease.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
  - [Simple Completion](#simple-completion)
  - [Chat Completion](#chat-completion)
  - [Webhook Completion](#webhook-completion)
  - [Streaming Completion](#streaming-completion)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install the Tela SDK via npm, yarn, or pnpm:

```bash
pip install tela
```

## Usage

First, you need to import the SDK and initialize it with your API key:

```python
from tela import create_tela_client

tela = create_tela_client(api_key='your-api-key')
```

## Examples

### Simple Completion

This example demonstrates how to create a simple completion using a PDF document:

```python
from tela import create_tela_client, create_tela_file

tela = create_tela_client(
    api_key='your-api-key',
)

completion = tela.completions.create({
    canvas_id='your-canvas-id',
    variables={
        "document": create_tela_file("https://www.wmaccess.com/downloads/sample-invoice.pdf"),
    },
})
print(completion)
```

### Chat Completion

This example shows how to create a chat completion with a simple message:

```python
from tela import create_tela_client

tela = create_tela_client(
    api_key='your-api-key',
)
completion = tela.completions.create({
    canvas_id='your-canvas-id',
    messages=[{'role': 'user', 'content': 'Hello!'}],
})
print(completion)
```

### Webhook Completion

This example demonstrates how to create a completion that sends the result to a webhook URL:

```python
from tela import create_tela_client, create_tela_file

tela = create_tela_client(
    api_key='your-api-key',
)

webhook = tela.completions.create({
    canvas_id='your-canvas-id',
    variables={
        document: create_tela_file("https://www.wmaccess.com/downloads/sample-invoice.pdf"),
    },
    webhook_url='https://webhook.site/4294967295',
    stream=False,
})
print(webhook)
```

### Streaming Completion

This example shows how to handle streaming responses:

```python
from tela import create_tela_client, create_tela_file

tela = create_tela_client(
    api_key='your-api-key',
)

with open('sample-invoice.pdf', 'rb') as file:
    completion = tela.completions.create({
        canvas_id='your-canvas-id',
        variables={
            'document': create_tela_file(file),
        },
        stream=True,
    })
    for chunk in completion:
        print(chunk)
```

## Contributing

We welcome contributions to the Tela SDK! Please see our [contributing guide](CONTRIBUTING.md) for more information.
