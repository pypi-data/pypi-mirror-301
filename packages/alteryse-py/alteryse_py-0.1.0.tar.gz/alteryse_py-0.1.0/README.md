# Alteryse Py

Alteryse Py is a Python library that provides an easy-to-use interface for interacting with the Alteryse Instances.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
  - [TextGeneration Class](#textgeneration-class)
    - [Constructor](#constructor)
    - [generate](#generate)
    - [chat](#chat)
- [Error Handling](#error-handling)
- [License](#license)

## Installation

You can install the package using pip:

```bash
pip install alteryse-py
```

## Usage

### Basic Example

To use the Alteryse library, create an instance of the `TextGeneration` class with your instance ID and API key:

```python
from alteryse import TextGeneration

# Initialize the TextGeneration instance
text_gen = TextGeneration(
    instance_id='your-instance-id',
    api_key='your-api-key'
)

# Generate text based on a prompt
async def generate_text():
    try:
        response = await text_gen.generate('What is the capital of France?')
        print(response.content)  # Logs the generated text
    except Exception as error:
        print('Error generating text:', error)

import asyncio
asyncio.run(generate_text())
```

### Chat Example

You can also use the library to send chat messages:

```python
# Send a chat message
async def send_chat_message():
    try:
        messages = [
            {'role': 'user', 'content': 'Hello, how are you?'},
            {'role': 'assistant', 'content': 'I am fine, thank you!'}
        ]
        response = await text_gen.chat(messages)
        print(response.content)  # Logs the chat response
    except Exception as error:
        print('Error in chat:', error)

asyncio.run(send_chat_message());
```

### Generating Text with Options

You can customize the text generation with additional options like `temperature` and `top_p`:

```python
options = {
    'temperature': 0.7,  # Controls the randomness of the output. Lower values make the output more deterministic.
    'top_p': 0.9  # Controls the diversity of the output. Values between 0 and 1 limit the set of possible outputs.
}

# Generate text with options
async def generate_text_with_options():
    try:
        response = await text_gen.generate('Tell me a joke.', options)
        print(response.content)  # Logs the generated joke
    except Exception as error:
        print('Error generating text with options:', error)

asyncio.run(generate_text_with_options());
```

## API Reference

### TextGeneration Class

The `TextGeneration` class provides methods to interact with the Alteryse API.

#### Constructor

```python
def __init__(self, instance_id: str, api_key: str):
```

- **instance_id**: The ID of the instance to connect to.
- **api_key**: The API key for authorization.

#### generate

```python
async def generate(self, prompt: str, images: Optional[List[str]] = None, options: Optional[Options] = None) -> GenerateResponse:
```

- **prompt**: The text prompt to generate text from.
- **images**: Optional images to be included in the generation process.
- **options**: Optional settings for the generation process.
- **Returns**: A promise that resolves to a `GenerateResponse` object.
- **Throws**: Error if the request fails or returns a 503 status.

#### chat

```python
async def chat(self, messages: List[ChatRequest], options: Optional[Options] = None) -> ChatResponse:
```

- **messages**: An array of chat messages to be sent, each with the following structure:

```python
{
    'role': 'system' | 'user' | 'assistant',
    'content': str,
    'images': Optional[List[str]]  # Optional images to include with the message
}
```

- **options**: Optional settings for the chat process.
- **Returns**: A promise that resolves to a `ChatResponse` object.
- **Throws**: Error if the request fails or returns a 503 status.

## Error Handling

The library handles errors internally and throws them when the API responds with an error status (e.g., 503). You can catch these errors in your implementation to manage user feedback or retries accordingly.

```python
try:
    response = await text_gen.generate('Your prompt here')
except Exception as error:
    print('Error:', error.message)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
