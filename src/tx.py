# This script can be used to configure a nrf52840dk that is flashed with the radio_test program
# to send rssi packets with the provided configuration.
# This script is supposed to be used in tandem with the rx.py

import serial
import nrf52840 as nrf

packages = 1000  # nr of packages to be sent per transmission


def main():
    port = nrf.prompt_for_serial_port()
    with serial.Serial() as ser:  # ensures opened port will be closed when leaving scope
        ser.baudrate = nrf.baudrate
        ser.port = port
        ser.open()

        # configure options that will not change
        nrf.configure_start_channel(ser)
        nrf.configure_transmit_pattern(ser)
        ser.flush()  # flush the data buffer over to the serial port
        for i in range(0, 4):
            print(ser.readline().decode())

        while True:  # loop until no more transmission shall be performed
            # configure options that need to be adjusted for every run
            nrf.configure_output_power(ser)
            nrf.configure_data_rate(ser)
            ser.flush()
            for i in range(0, 4):
                print(ser.readline().decode())

            while input("start transmission? (y, n) ") == "y":  # start transmission with current configuration
                nrf.start_tx(ser, packages)
                ser.flush()

                line = ser.readline().decode()
                while line.find("TX has finished") == -1:  # wait till transmission has finished
                    print(line)
                    line = ser.readline().decode()
                print(line)

            if input("configure next transmission? (y, n) ") != "y":
                break


if __name__ == "__main__":
    main()
