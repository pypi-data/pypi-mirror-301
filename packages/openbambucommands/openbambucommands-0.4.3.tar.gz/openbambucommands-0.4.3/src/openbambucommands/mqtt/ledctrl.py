import json


def set_light(led_on: bool) -> str:
    """Return a command string formatted to set the printer light on or off.

    :param led_on: The state the light will be set to
    :return: The JSON-formatted string with the command the printer expects
    """
    command = json.loads(
        f"""
    {{
        "system": {{
            "sequence_id": "0",
            "command": "ledctrl",
            "led_node": "chamber_light",
            "led_mode": "{"on" if led_on is True else "off"}",
            "led_on_time": 0,
            "led_off_time": 0,
            "loop_times":  0,
            "interval_time": 0
        }}
    }}
    """
    )
    return json.dumps(command)
