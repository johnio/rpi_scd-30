# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
import adafruit_scd30

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

#unsure of units, seems to be neg deg C
#scd.temperature_offset = 2
#time.sleep(0.5)
print("Temperature offset:", scd.temperature_offset)

# scd.measurement_interval = 4
print("Measurement interval:", scd.measurement_interval)

#us forced calibration
#scd.self_calibration_enabled = False
print("Self-calibration enabled:", scd.self_calibration_enabled)

#does not seem to work, use altitude
#scd.ambient_pressure = 1002
#time.sleep(0.5)
print("Ambient Pressure:", scd.ambient_pressure)

#scd.altitude = 270
print("Altitude:", scd.altitude, "meters above sea level")

#only run one time when outside and settled
#scd.forced_recalibration_reference = 400
#time.sleep(0.5)
print("Forced recalibration reference:", scd.forced_recalibration_reference)
print("")


while True:
    # since the measurement interval is long (2+ seconds) we check for new data before reading
    # the values, to ensure current readings.
    if scd.data_available:
        print("Data Available!")
        print("CO2: %d PPM" % scd.CO2)
        print("Temperature: %0.2f degrees C" % scd.temperature)
        print("Humidity: %0.2f %% rH" % scd.relative_humidity)
        print("")
        print("Waiting for new data...")
        print("")

    time.sleep(0.5)
