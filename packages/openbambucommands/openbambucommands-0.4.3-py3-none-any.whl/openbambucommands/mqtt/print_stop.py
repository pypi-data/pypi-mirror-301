import json


def stop_print() -> str:
    """Return a command string formatted to stop the current print.

    Send with QoS of 1 for higher priority.

    :return: The JSON-formatted string with the command the printer expects
    """
    command = json.loads(
        """
        {
            "print": {
                "sequence_id": "0",
                "command": "stop",
                "param": ""
            }
        }
        """
    )
    return json.dumps(command)
