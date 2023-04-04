import json


class Helper:
    def create_json(self, data):
        self.data = []
        for row in data:
            s = {
                "t": row[0],
                "stillness": row[1],
                "gyro": [row[2], row[3], row[4]],
                "accel": [row[5], row[6], row[7]],
                "magne": [row[8], row[9], row[10]],
                "alpha": row[11],
                "mu": row[37]
            }
            self.data.append(s)

        return self.data