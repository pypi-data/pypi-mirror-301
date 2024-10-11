"""
LunarDB Client Module

This module provides a Python client for interacting with a LunarDB instance.
"""

import requests
from typing import Any, Dict, List, Optional, Tuple
from .exceptions import LunarDBException, ConnectionError, AuthenticationError, KeyError, ServerError

class LunarDBClient:
    """
    A client for interacting with LunarDB.

    This client provides methods for various LunarDB operations including
    key-value operations, list operations, and database management.
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize a new LunarDBClient.

        Args:
            base_url (str): The base URL of the LunarDB API.
            api_key (Optional[str]): An optional API key for authentication.
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Send a request to the LunarDB API.

        Args:
            method (str): The HTTP method to use.
            endpoint (str): The API endpoint to call.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            Dict[str, Any]: The JSON response from the API.

        Raises:
            ConnectionError: If there's an issue connecting to the server.
            AuthenticationError: If there's an authentication problem.
            ServerError: If the server returns an unexpected error.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to LunarDB: {e}")
        except requests.HTTPError as e:
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed")
            elif response.status_code >= 500:
                raise ServerError(f"Server error: {response.text}")
            else:
                raise LunarDBException(f"HTTP error occurred: {e}")

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> Dict[str, Any]:
        """
        Set a key-value pair in LunarDB.

        Args:
            key (str): The key to set.
            value (Any): The value to set.
            ttl (Optional[int]): Time to live in seconds.

        Returns:
            Dict[str, Any]: The response from the server.

        Raises:
            KeyError: If there's an issue with the key operation.
        """
        try:
            data = {"key": key, "value": value}
            if ttl is not None:
                data["ttl"] = ttl
            return self._request("POST", "/set", json=data)
        except LunarDBException as e:
            raise KeyError(f"Error setting key '{key}': {e}")

    def get(self, key: str) -> Any:
        """
        Get the value for a key from LunarDB.

        Args:
            key (str): The key to retrieve.

        Returns:
            Any: The value associated with the key.

        Raises:
            KeyError: If the key is not found or there's an issue with the key operation.
        """
        try:
            response = self._request("GET", f"/get/{key}")
            return response.get("value")
        except LunarDBException as e:
            raise KeyError(f"Error getting key '{key}': {e}")

    def delete(self, key: str) -> Dict[str, Any]:
        """
        Delete a key-value pair from LunarDB.

        Args:
            key (str): The key to delete.

        Returns:
            Dict[str, Any]: The response from the server.

        Raises:
            KeyError: If there's an issue with the key operation.
        """
        try:
            return self._request("DELETE", f"/delete/{key}")
        except LunarDBException as e:
            raise KeyError(f"Error deleting key '{key}': {e}")

    def mset(self, kvs: List[Tuple[str, Any]]) -> Dict[str, Any]:
        """
        Set multiple key-value pairs in LunarDB.

        Args:
            kvs (List[Tuple[str, Any]]): A list of key-value tuples to set.

        Returns:
            Dict[str, Any]: The response from the server.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            return self._request("POST", "/mset", json={"kvs": dict(kvs)})
        except LunarDBException as e:
            raise LunarDBException(f"Error in MSET operation: {e}")

    def mget(self, keys: List[str]) -> List[Any]:
        """
        Get multiple values from LunarDB.

        Args:
            keys (List[str]): A list of keys to retrieve.

        Returns:
            List[Any]: A list of values corresponding to the keys.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            response = self._request("POST", "/mget", json={"keys": keys})
            return response.get("values", [])
        except LunarDBException as e:
            raise LunarDBException(f"Error in MGET operation: {e}")

    def keys(self) -> List[str]:
        """
        Get all keys in LunarDB.

        Returns:
            List[str]: A list of all keys in the database.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            response = self._request("GET", "/keys")
            return response.get("keys", [])
        except LunarDBException as e:
            raise LunarDBException(f"Error getting keys: {e}")

    def clear(self) -> Dict[str, Any]:
        """
        Clear all key-value pairs from LunarDB.

        Returns:
            Dict[str, Any]: The response from the server.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            return self._request("POST", "/clear")
        except LunarDBException as e:
            raise LunarDBException(f"Error clearing database: {e}")

    def size(self) -> int:
        """
        Get the number of key-value pairs in LunarDB.

        Returns:
            int: The number of key-value pairs.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            response = self._request("GET", "/size")
            return response.get("size", 0)
        except LunarDBException as e:
            raise LunarDBException(f"Error getting size: {e}")

    def cleanup_expired(self) -> Dict[str, Any]:
        """
        Remove expired entries from LunarDB.

        Returns:
            Dict[str, Any]: The response from the server.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            return self._request("POST", "/cleanup")
        except LunarDBException as e:
            raise LunarDBException(f"Error cleaning up expired entries: {e}")

    def save(self, filename: str) -> Dict[str, Any]:
        """
        Save the cache to a file.

        Args:
            filename (str): The name of the file to save to.

        Returns:
            Dict[str, Any]: The response from the server.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            return self._request("POST", "/save", json={"filename": filename})
        except LunarDBException as e:
            raise LunarDBException(f"Error saving to file: {e}")

    def load(self, filename: str) -> Dict[str, Any]:
        """
        Load the cache from a file.

        Args:
            filename (str): The name of the file to load from.

        Returns:
            Dict[str, Any]: The response from the server.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            return self._request("POST", "/load", json={"filename": filename})
        except LunarDBException as e:
            raise LunarDBException(f"Error loading from file: {e}")

    def lpush(self, key: str, value: Any) -> Dict[str, Any]:
        """
        Push an element to the head of the list.

        Args:
            key (str): The key of the list.
            value (Any): The value to push.

        Returns:
            Dict[str, Any]: The response from the server.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            return self._request("POST", "/lpush", json={"key": key, "value": value})
        except LunarDBException as e:
            raise LunarDBException(f"Error in LPUSH operation: {e}")

    def lpop(self, key: str) -> Any:
        """
        Remove and return an element from the head of the list.

        Args:
            key (str): The key of the list.

        Returns:
            Any: The popped value.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            response = self._request("POST", "/lpop", json={"key": key})
            return response.get("value")
        except LunarDBException as e:
            raise LunarDBException(f"Error in LPOP operation: {e}")

    def rpush(self, key: str, value: Any) -> Dict[str, Any]:
        """
        Push an element to the tail of the list.

        Args:
            key (str): The key of the list.
            value (Any): The value to push.

        Returns:
            Dict[str, Any]: The response from the server.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            return self._request("POST", "/rpush", json={"key": key, "value": value})
        except LunarDBException as e:
            raise LunarDBException(f"Error in RPUSH operation: {e}")

    def rpop(self, key: str) -> Any:
        """
        Remove and return an element from the tail of the list.

        Args:
            key (str): The key of the list.

        Returns:
            Any: The popped value.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            response = self._request("POST", "/rpop", json={"key": key})
            return response.get("value")
        except LunarDBException as e:
            raise LunarDBException(f"Error in RPOP operation: {e}")

    def lrange(self, key: str, start: int, stop: int) -> List[Any]:
        """
        Get a range of elements from the list.

        Args:
            key (str): The key of the list.
            start (int): The starting index.
            stop (int): The stopping index.

        Returns:
            List[Any]: The range of elements.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            response = self._request("GET", f"/lrange/{key}/{start}/{stop}")
            return response.get("values", [])
        except LunarDBException as e:
            raise LunarDBException(f"Error in LRANGE operation: {e}")

    def llen(self, key: str) -> int:
        """
        Get the length of the list.

        Args:
            key (str): The key of the list.

        Returns:
            int: The length of the list.

        Raises:
            LunarDBException: If there's an issue with the operation.
        """
        try:
            response = self._request("GET", f"/llen/{key}")
            return response.get("length", 0)
        except LunarDBException as e:
            raise LunarDBException(f"Error in LLEN operation: {e}")
        