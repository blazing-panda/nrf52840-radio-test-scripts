# This script can be used to configure a nrf52840dk that is flashed with the radio_test program
# to receive rssi packets with the provided configuration and save the result
# of all performed runs into "radio_test.csv".
# This script is supposed to be used in tandem with the tx.py


import os
import serial
import pandas as pd
import nrf52840 as nrf

file_name = "radio_test.csv"


def main():
    port = nrf.prompt_for_serial_port()
    with serial.Serial() as ser:  # ensures that ports will be closed when leaving scope
        ser.baudrate = nrf.baudrate
        ser.port = port

        # timeout ensures that ser.readline() will eventually timeout and the next run can be performed
        # also means that we have  seconds to start receiving
        ser.timeout = 5

        ser.open()

        # configure options that will not change
        nrf.configure_start_channel(ser)
        nrf.configure_transmit_pattern(ser)
        ser.flush()
        for i in range(0, 4):
            print(ser.readline().decode())

        runs = {}  # this dict will contain all performed runs
        # load available data => useful if a run needs to be redone
        if os.path.exists(file_name) and input(f"{file_name} found, reuse? (y, n) ") == "y":
            runs = pd.read_csv(file_name).to_dict(orient="list")

        while True:  # loop until no more runs are to be performed
            # configure options that need to be adjusted for every run
            output_power = nrf.prompt_for_output_power()
            data_rate = nrf.prompt_for_data_rate()
            distance = nrf.prompt_for_distance()
            run_name = f"{data_rate}-{output_power}-{distance}m"

            nrf.set_data_rate(ser, data_rate)
            ser.flush()
            for i in range(0, 2):
                print(ser.readline().decode())

            _ = input("start receiving on enter:")
            nrf.start_rx(ser)
            ser.flush()

            print(ser.readline().decode())  # fetch the start call
            line = ser.readline()
            received_values = []
            while line:
                substr = line.decode().split("=")
                if len(substr) > 1:
                    received_values.append(int(substr[1]))
                line = ser.readline()
            runs[run_name] = received_values  # inserts run or overwrites previous run with same config

            # save all runs to csv => canceling will not cause data loss
            df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in runs.items()]))
            df.to_csv(file_name, index=False)

            if input("configure next run? (y, n)") != "y":
                break

        print(df.describe())


if __name__ == "__main__":
    main()
