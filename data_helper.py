import json


def create_json(data, t="r"):
    # [t] is type of source file.
    #               - 'r' is recording file
    #               - 'd' is Data001.txt
    json_data = []
    if t == "r":
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
            json_data.append(s)

    elif t == "d":
        for row in data:
            s = {
                "t": row[0],
                "stillness": row[1],
                "gyro": [row[2], row[3], row[4]],
                "accel": [row[5], row[6], row[7]],
                "magne": [row[8], row[9], row[10]],
                "alpha": row[11],
                "mu": row[12]
            }
            json_data.append(s)

    return json_data
