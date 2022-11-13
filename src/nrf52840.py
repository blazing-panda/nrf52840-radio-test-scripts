# This script contains configuration option for a nrf52840dk that is flashed with the radio_test program.
# It provides prompts for specific settings and helpers to configure a connected board via the ser.Serial class

import serial.tools.list_ports
from serial import Serial

baudrate = 115200

data_rates = [
    ("ble_1Mbit", "1 Mbit/s Bluetooth Low Energy"),
    ("ble_2Mbit", "2 Mbit/s Bluetooth Low Energy"),
    ("ble_lr125Kbit", "Long range 125 kbit/s TX, 125 kbit/s and 500 kbit/s RX"),
    ("ble_lr500Kbit", "Long range 500 kbit/s TX, 125 kbit/s and 500 kbit/s RX"),
    ("nrf_1Mbit", "1 Mbit/s Nordic proprietary radio mode"),
    ("nrf_2Mbit", "2 Mbit/s Nordic proprietary radio mode"),
    ("ieee802154_250Kbit", "IEEE 802.15.4-2006 250 kbit/s"),
]

# uncomment the options you want to enable
output_powers = [
    "pos8dBm",
    # "pos7dBm",
    # "pos6dBm",
    # "pos5dBm",
    # "pos4dBm",
    # "pos3dBm",
    # "pos2dBm",
    "pos0dBm",
    # "neg4dBm",
    # "neg8dBm",
    # "neg12dBm",
    # "neg16dBm",
    # "neg20dBm",
    # "neg30dBm",
    "neg40dBm",
]
transmit_patterns = [
    "pattern_11110000",
    # "pattern_11001100",
    # "pattern_random",
]


def input_int_in_range(prompt: str, start: int, end: int):
    res = ""
    while True:
        res = input(prompt)
        try:
            res = int(res)
            if start <= res <= end:
                break
            else:
                print("input not in range, try again")
        except ValueError:
            print("not an integer, try again")
    return res


def prompt_for_data_rate() -> str:
    print("Available data rates:")
    for i, rate in enumerate(data_rates):
        print(f"[{i}] {rate[0]} ({rate[1]})")
    data_rate_index = input_int_in_range(f"select data rate [0 - {len(data_rates) - 1}]: ", 0, len(data_rates) - 1)
    return data_rates[data_rate_index][0]


def prompt_for_output_power() -> str:
    print("Available output powers:")
    for i, power in enumerate(output_powers):
        print(f"[{i}] {power}")
    output_power_index = input_int_in_range(f"select output power [0 - {len(output_powers) - 1}]: ", 0,
                                            len(output_powers) - 1)
    return output_powers[output_power_index]


def prompt_for_transmit_pattern() -> str:
    return transmit_patterns[0]


def prompt_for_distance() -> float:
    while True:
        val = input("set current distance (in meter): ")
        try:
            return float(val)
        except ValueError:
            print("not a float value, try again")


def prompt_for_serial_port() -> str:
    available_ports = [comport.device for comport in serial.tools.list_ports.comports()]
    for i, port in enumerate(available_ports):
        print(f"[{i}] {port}")
    selected_port = input_int_in_range(f"select port [0 - {len(available_ports) - 1}]: ", 0,
                                       len(output_powers) - 1)
    return available_ports[selected_port]


def set_data_rate(ser: Serial, rate: str):
    ser.write(f"data_rate {rate}\r\n".encode())


def configure_data_rate(ser: Serial):
    set_data_rate(ser, prompt_for_data_rate())


def configure_output_power(ser: Serial):
    ser.write(f"output_power {prompt_for_output_power()}\r\n".encode())


def configure_transmit_pattern(ser: Serial):
    ser.write(f"transmit_pattern {prompt_for_transmit_pattern()}\r\n".encode())


def configure_start_channel(ser: Serial):
    start_channel = 0
    while True:
        try:
            start_channel = int(input("set start channel: "))
            break
        except ValueError:
            print("input not an int, try again")
    ser.write(f"start_channel {start_channel}\r\n".encode())


def start_tx(ser: Serial, packages: int):
    ser.write(f'start_tx_modulated_carrier {packages}\r\n'.encode())


def start_rx(ser: Serial):
    ser.write(b'start_rx \r\n')

