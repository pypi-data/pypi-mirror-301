import requests


def init():
    try:
        response = requests.get(url="https://dev-api.miralabs.ai/lon/")

        # Check if the response status code indicates a failure
        if not response.ok:
            raise PermissionError("ACCESS DENIED")

        # Return the JSON content if successful
        return response.json()

    except requests.exceptions.RequestException as e:
        # Handle general request exceptions
        raise PermissionError("ACCESS DENIED") from e
