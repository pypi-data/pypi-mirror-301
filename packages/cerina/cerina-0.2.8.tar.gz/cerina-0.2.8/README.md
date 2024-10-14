# Cerina Package

## Overview
Cerina is a package that provides functionalities for different llm completions, Advanced AI Agents and Agentic search at free of cost. Explore more below and give a star.

## Installation
To install the package, run:

```sh
pip install -U cerina
```
### Basic Chat Integration
Use our llm's into your applications at free of cost

- Synchronous

```bash
from cerina import Completion

completion = Completion()
prompt = "What are the benefits of using AI in education?"
response = completion.create(prompt)
print("Response from API:", response)
```
- Asynchronous Example

```bash
import asyncio
from cerina import Completion

completion = Completion()
async def main():
    query = "which is the most advanced version of gpt?"
    response = await completion.create_async(query)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

### Integrate Search Functions with GPT

```bash
import asyncio
from cerina import IntegratedSearchGPT

async def main():
    integrated_search_gpt = IntegratedSearchGPT()
    query = "what is the dollar price now in inr?"
    response = await integrated_search_gpt.generate_with_search(query)
    print("Response from API:", response)

if __name__ == "__main__":
    asyncio.run(main())
```

### Search Text

```bash
from cerina import print_search_results, search_text, search_images

def main():
    query_text = "Hetc"

    print("Text Search Results:")
    print_search_results(query_text, search_text)

if __name__ == "__main__":
    main()
```

### Search Image

```bash
from cerina import print_search_results, search_text, search_images

def main():
    query_image = "cats"


    print("Image Search Results:")
    print_search_results(query_image, search_images)

if __name__ == "__main__":
    main()
```



