import json
import os
import time
import redis

#redis_client = redis.StrictRedis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)
redis_client = redis.StrictRedis()


import datetime

#adafruit imports
import time
import board
import busio
import adafruit_scd30

class CO2Monitor():
    def __init__(self):
        # SCD-30 has tempremental I2C with clock stretching, datasheet recommends
        # starting at 50KHz
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
        self.scd = adafruit_scd30.SCD30(self.i2c)

    def get_measurement(self):
        t = datetime.datetime.now()
        print(t.isoformat())
        print("CO2: %d PPM" % self.scd.CO2)
        print("Temperature: %0.2f degrees C" % self.scd.temperature)
        print("Humidity: %0.2f %% rH" % self.scd.relative_humidity)

        return {
            'time': int(time.time()),
            'measurement': {
                'co2_ppm': self.scd.CO2,
                'temp_f': self.scd.temperature*9.0/5.0+32,
                'temp_c': self.scd.temperature,
                'humid_perc' : self.scd.relative_humidity,
                'timestamp': t.isoformat()
                },
        }

    def save_measurement_to_redis(self):
        """Saves measurement to redis db"""
        redis_client.lpush('measurements', json.dumps(self.get_measurement(), default=str))

    def get_last_n_measurements(self):
        """Returns the last n measurements in the list"""
        return [json.loads(x) for x in redis_client.lrange('measurements', 0, -1)]
