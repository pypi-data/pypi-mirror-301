import json


def get_version() -> str:
    """Return the slicer command to get the printer version info.

    :return: The JSON-formatted string with the command the printer expects
    """
    command = json.loads(
        """
        {
            "info": {
                "sequence_id": "0",
                "command": "get_version"
            }
        }
        """
    )
    return json.dumps(command)
