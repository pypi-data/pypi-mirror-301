import json


def calibrate(
    *,
    bed_leveling: bool = False,
    motor_noise_calibration: bool = False,
    micro_lidar_calibration: bool = False,
    resonance_freq_id: bool = False,
) -> str:
    """Return a command string formatted to start calibration.

    :param bed_leveling:
    :param motor_noise_calibration:
    :param micro_lidar_calibration:
    :param resonance_freq_id:
    :return: The JSON-formatted string with the command the printer expects
    """
    options = _options_bitmask(
        bed_leveling,
        motor_noise_calibration,
        micro_lidar_calibration,
        resonance_freq_id,
    )
    command = json.loads(
        f"""
        {{
            "print": {{
                "sequence_id": "0",
                "command": "calibration",
                "option": {options}
            }}
        }}
        """
    )

    return json.dumps(command)


def _options_bitmask(
    bed_leveling: bool = False,
    motor_noise_calibration: bool = False,
    micro_lidar_calibration: bool = False,
    resonance_freq_id: bool = False,
) -> int:
    bitmask = 0
    # this is the proper order of bits
    options = [
        micro_lidar_calibration,  # 1
        bed_leveling,  # 2
        resonance_freq_id,  # 4
        motor_noise_calibration,  # 8
    ]

    for i, option in enumerate(options):
        if option:
            bitmask |= 1 << i

    return int(bitmask)
