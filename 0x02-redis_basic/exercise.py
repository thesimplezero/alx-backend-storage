#!/usr/bin/env python3
"""
Module to interact with Redis
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


class Cache:
    """
    Cache class for storing and retrieving data in Redis
    """
    def __init__(self):
        """
        Initialize the Cache instance with a Redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count the number of calls
        to a method and store in Redis

        Args:
            method: The method to be decorated

        Returns:
            Callable: The decorated method
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """
        Decorator to store the history of inputs and
        outputs for a particular function in Redis

        Args:
            method: The method to be decorated

        Returns:
            Callable: The decorated method
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            inputs_key = f"{method.__qualname__}:inputs"
            outputs_key = f"{method.__qualname__}:outputs"

            # Append input arguments to the inputs list
            self._redis.rpush(inputs_key, str(args))

            # Execute the wrapped function to retrieve the output
            output = method(self, *args, **kwargs)

            # Store the output in the outputs list
            self._redis.rpush(outputs_key, str(output))

            return output

        return wrapper

    @staticmethod
    def replay(func: Callable) -> None:
        """
        Display the history of calls for a particular function

        Args:
            func: The function to display the history for

        Returns:
            None
        """
        key = func.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"

        inputs = cache._redis.lrange(inputs_key, 0, -1)
        outputs = cache._redis.lrange(outputs_key, 0, -1)

        print(f"{key} was called {len(inputs)} times:")

        for inp, out in zip(inputs, outputs):
            print(f"{func.__name__}{inp.decode()} -> {out.decode()}")


# Test cases
if __name__ == "__main__":
    cache = Cache()

    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    Cache.replay(cache.store)
