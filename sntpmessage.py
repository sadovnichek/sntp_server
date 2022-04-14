import datetime
import struct
import time

diff = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 60 * 60


def format_time(timestamp):
    return int(timestamp * (2 ** 32))


class SNTPMessage:
    def __init__(self, data, offset=0, stratum=1):
        self.offset = offset
        self.format = ">3B b 5I 3Q"
        self.leap = 0  # no warnings
        self.version = 4
        self.mode = 4  # server
        self.flags = self.leap << 6 | self.version << 3 | self.mode
        self.stratum = stratum
        self.polling = 4  # 2**4=16 seconds
        self.precision = -6
        self.root_delay = 0
        self.root_dispersion = 0
        self.reference_id = 0
        self.ref_timestamp = 0
        self.origin_timestamp = int.from_bytes(data[40:48], 'big')
        self.receive_timestamp = time.time() + diff

    def __bytes__(self):
        return struct.pack(self.format,
                           self.flags,
                           self.stratum,
                           self.polling,
                           self.precision,
                           self.root_delay,
                           self.root_dispersion,
                           self.reference_id,
                           self.ref_timestamp,  # update time
                           self.ref_timestamp,
                           self.origin_timestamp,
                           format_time(self.receive_timestamp + self.offset),
                           format_time(time.time() + diff + self.offset))
