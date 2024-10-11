import pycurl, httpx
import logging


def make_request(url, headers, method='GET', data=None):
    try:
        # Make the request based on the method
        if method.upper() == 'GET':
            response = httpx.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = httpx.post(url, headers=headers, json=data)
        elif method.upper() == 'PUT':
            response = httpx.put(url, headers=headers, json=data)
        elif method.upper() == 'DELETE':
            response = httpx.delete(url, headers=headers)
        else:
            logging.error(f"Unsupported HTTP method: {method}")
            return None

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Return the JSON response
        return response.json()

    except httpx.RequestError as e:
        # Handle network-related errors
        logging.error(f"Request error occurred: {e}")
    except httpx.HTTPStatusError as e:
        # Handle HTTP status errors (e.g., 4xx, 5xx responses)
        logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        # Catch-all for any other exceptions
        logging.error(f"An unexpected error occurred: {e}")

    # Return None if an error occurs
    return None