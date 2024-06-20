#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    """ Decorator for caching and tracking get_page function calls """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper function that:
            - Increments the call count for the given URL
            - Checks if the URL's response is cached in Redis
            - Retrieves cached data if available, otherwise makes an HTTP request
            - Caches the response in Redis with a timeout of 10 seconds
        """
        client = redis.Redis()
        client.incr(f'count:{url}')  # Increment call count for this URL
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')  # Return cached response if available
        response = fn(url)  # Call original function to fetch data
        client.set(f'{url}', response, 10)  # Cache response in Redis for 10 seconds
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """ Makes an HTTP GET request to the specified URL and returns the response text """
    response = requests.get(url)
    return response.text

