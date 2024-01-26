#!/usr/bin/env python3
"""
Module to fetch HTML content of a URL,
track access count, and cache results
"""
import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


def track_access_count(func: Callable) -> Callable:
    """
    Decorator to track the number of times a URL is accessed

    Args:
        func: The function to be decorated

    Returns:
        Callable: The decorated function
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"

        # Increment access count
        redis_conn.incr(count_key)

        # Call the original function
        result = func(url)

        return result

    return wrapper


def cache_result(expiration: int = 10) -> Callable:
    """
    Decorator to cache the result of a function with an expiration time

    Args:
        expiration: Expiration time in seconds

    Returns:
        Callable: The decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            result_key = f"result:{url}"

            # Check if result is already in cache
            cached_result = redis_conn.get(result_key)
            if cached_result:
                return cached_result.decode()

            # Call the original function
            result = func(url)

            # Cache the result with expiration time
            redis_conn.setex(result_key, expiration, result)

            return result

        return wrapper

    return decorator


@track_access_count
@cache_result(expiration=10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL

    Args:
        url: The URL to fetch

    Returns:
        str: The HTML content
    """
    response = requests.get(url)
    return response.text


# Example usage
if __name__ == "__main__":
    base_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/"
    specific_path = "http://www.google.com"
    slow_url = base_url + specific_path
    # Access slow URL multiple times
    for _ in range(5):
        content = get_page(slow_url)
        print(content)

    # Print access count
    access_count = redis_conn.get(f"count:{slow_url}")
    print(f"Access count for {slow_url}: {access_count.decode()}")
