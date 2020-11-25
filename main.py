from circleparse import parse_replay_file
import time
import cv2
import numpy as np


def main(filename):
    width = 1500
    height = 80
    image = np.ones((height, width)) * 255

    replay = parse_replay_file(filename)

    current_time = 0

    lines = [[]]

    r = 1
    r2 = 1
    lastData = [0,0,0]
    key_passed = 0

    for data in replay.play_data:
        c_data = [int(data.x), int(data.y), data.keys_pressed]

        if c_data[0] >= 180 and c_data[0] <= 200 and c_data[1] >= 200 and c_data[1] <= 240:

            if data.keys_pressed == 0:
                key_passed += 1

            if lastData != c_data:

                if key_passed >= 6 or r >= 7:
                    if len(lines[-1]) > 1:
                        lines.append([])
                elif r >= 4:
                    lines[-1].append(lastData)
                    lines[-1].append(c_data)

                r = 1
                lastData = c_data
            r += 1

        if data.keys_pressed != 0:
            key_passed = 0

    offset = 45

    print("LEN: {}".format(len(lines)))

    for word_i in range(len(lines)):
        for word_l in range(1, len(lines[word_i])):
            letter = lines[word_i][word_l]
            prev_letter = lines[word_i][word_l-1]

            p_x = prev_letter[0]
            p_y = prev_letter[1]
            c_x = letter[0]
            c_y = letter[1]

            p_x += word_i * offset - 160
            c_x += word_i * offset - 160

            p_y -= 190
            c_y -= 190

            cv2.line(image, (p_x, p_y), (c_x, c_y), (0, 0, 0), thickness=2)

    cv2.imwrite("test.png", image)


main("replay_c7fc37de03.osr")