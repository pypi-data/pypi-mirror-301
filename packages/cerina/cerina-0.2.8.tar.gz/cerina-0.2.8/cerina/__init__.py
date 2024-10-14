from .gpt import Completion
from .search_text import search_text
from .search import IntegratedSearchGPT
from .search_img import search_images
from .Agents.superagents import *
from .agents import *
from .Scrapping.selenium_scrapper import *
from .prompt_template import *
from .optimiser import *

__all__ = [
    "Completion",
    "search_text",
    "search_text_async",
    "search_images",
    "search_images_async",
    "Agent",
    "ResearchAgent",
    "ScriptWriterAgent",
    "Tool",
    "CustomTool",
    "SeleniumScraper",
    "PromptOptimizer",
]

def print_search_results(query, search_func):
    """
    Print search results from a given search function.

    Args:
        query (str): The search query.
        search_func (function): The search function to use (either search_text or search_images).
    """
    results = search_func(query)
    for index, result in enumerate(results, start=1):
        print(f"Result {index}:")
        for key, value in result.items():
            print(f"  {key.capitalize()}: {value}")
        print()