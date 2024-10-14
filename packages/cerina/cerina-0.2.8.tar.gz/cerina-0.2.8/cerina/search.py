import asyncio
from .gpt import Completion
from .search_text import search_text

class IntegratedSearchGPT:
    def __init__(self):
        self.completion = Completion()
    
    def generate_with_search_sync(self, query, max_results=5):
        """
        Generate a GPT completion using search results as context in a synchronous manner.

        Args:
            query (str): The user's query to search and generate a completion for.
            max_results (int): The maximum number of search results to fetch.

        Returns:
            str: The generated text as a response from the GPT API.
        """
        # Perform the search
        search_results = search_text(query, max_results=max_results)
        
        # Format the search results as context
        context = "\n".join([f"Title: {result.get('title')}\nBody: {result.get('body')}" for result in search_results])

        # Create the prompt with the search results as context
        prompt = f"Using the following information:\n{context}\n\nAnswer the following question:\n{query}"

        # Generate the GPT completion
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.completion.create(prompt))
        return response

    async def generate_with_search(self, query, max_results=5):
        """
        Generate a GPT completion using search results as context.

        Args:
            query (str): The user's query to search and generate a completion for.
            max_results (int): The maximum number of search results to fetch.

        Returns:
            str: The generated text as a response from the GPT API.
        """
        # Perform the search
        search_results = search_text(query, max_results=max_results)
        
        # Format the search results as context
        context = "\n".join([f"Title: {result.get('title')}\nBody: {result.get('body')}" for result in search_results])

        # Create the prompt with the search results as context
        prompt = f"Using the following information:\n{context}\n\nAnswer the following question:\n{query}"

        # Generate the GPT completion
        response = await self.completion.create_async(prompt)
        return response