import aiohttp
from aiohttp import ClientSession, ClientError
import nest_asyncio
import asyncio

nest_asyncio.apply()

class Completion:
    """
    This class provides methods for generating completions based on prompts using an asynchronous HTTP request.
    """

    async def create_async(self, prompt):
        """
        Create a completion for the given prompt using an AI text generation API.

        Args:
            prompt (str): The input prompt for generating the text.

        Returns:
            str: The generated text as a response from the API.

        Raises:
            ClientError: If there is an issue with sending the request or fetching the response.
        """
        async with ClientSession() as session:
            try:
                async with session.post(
                    url="https://api.binjie.fun/api/generateStream",
                    headers={
                        "origin": "https://chat18.aichatos96.com",
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
                    },
                    json={
                        "prompt": prompt,
                        "system": "Always talk in English.",
                        "withoutContext": True,
                        "stream": False,
                    },
                ) as resp:
                    return await resp.text()
            except ClientError as exc:
                raise ClientError("Unable to fetch the response.") from exc
            except Exception:
                return "Sorry, your request can't be processed now!, Try again later."

    def create(self, prompt):
        """
        Create a completion for the given prompt using an AI text generation API in a synchronous manner.

        Args:
            prompt (str): The input prompt for generating the text.

        Returns:
            str: The generated text as a response from the API.
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.create_async(prompt))
