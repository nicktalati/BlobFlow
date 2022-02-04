import blob
import numpy as np
import random
import matplotlib.pyplot as plt
import cv2


def make_2d_pic(dspace, frames, noise_amount=0):
    """
    This takes a BlobSpace "dspace" and advances it forward
    "frames" times. Each time it appends the state of the
    BlobSpace onto the end of a numpy array. At each step
    a random number between plus and minus "noise_amount"
    is added to each entry.
    """
    ret = np.empty((frames, dspace.width, 3), dtype=int)
    for frame in range(frames):
        image_1d = dspace.create_1d_image()
        add_noise(image_1d, noise_amount)
        ret[frame] = image_1d
        dspace.time_step()
    return ret


def make_video(name, dspace, frames, noise_amount=0):
    out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), 30, (600, 200))
    for _ in range(frames):
        image_1d = dspace.create_1d_image()
        add_noise(image_1d, noise_amount)
        data = np.full((200, dspace.width, 3), image_1d, dtype='uint8')
        dspace.time_step()
        out.write(data)
    out.release()


def make_random_color():
    red = random.randint(10, 210)
    green = random.randint(10, 180)
    blue = random.randint(10, 160)
    return np.array([red, green, blue])


def add_noise(picture_1d, amount):
    for entry in range(len(picture_1d)):
        for color in range(3):
            new_color = picture_1d[entry][color] + random.randint(-1 * amount, amount)
            new_color = min(new_color, 255)
            new_color = max(new_color, 0)
            picture_1d[entry][color] = new_color


def make_random_blob(min_pos, max_pos, min_width, max_width, min_speed, max_speed,
                     color_var=0, speed_var=0, acc_var=0):
    """
    This makes a random blob within the specified ranges. Note that
    color_var controls the range of colors within a given blob.
    """
    position = random.uniform(min_pos, max_pos)
    width = random.randint(min_width, max_width)
    speed = random.uniform(min_speed, max_speed)
    color = make_random_color()
    values = np.full((width, 3), color)
    for value in range(width):
        for index in range(3):
            new_value = values[value][index] + random.randint(-1 * color_var, color_var)
            new_value = min(255, new_value)
            new_value = max(0, new_value)
            values[value][index] = new_value
    return blob.Blob(position, speed, values, speed_var=speed_var, acc_var=acc_var)


def show_image(array):
    plt.imshow(array)
    plt.show()


if __name__ == '__main__':
    NUM_BLOBS = 100
    SPACE_WIDTH = 600
    TIME_STEPS = 150
    MIN_SPEED = -6
    MAX_SPEED = 6
    MIN_POS = -800
    MIN_BLOB_WIDTH = 40
    MAX_BLOB_WIDTH = 60
    MAX_POS = SPACE_WIDTH - MIN_POS
    BACKGROUND = 30
    """
    The following variables essentially control the complexity
    of the resulting image:
    """
    COLOR_VAR = 25  # Works well between 0 and 40.
    SPEED_VAR = 1  # Works well between 0 and 1.
    ACC_VAR = .5  # Works well between 0 and .5. Quickly gets complicated.
    NOISE = 5  # Works well between 0 and 100.

    space = blob.BlobSpace(SPACE_WIDTH, BACKGROUND)

    for i in range(NUM_BLOBS):
        simple_blob = make_random_blob(MIN_POS, MAX_POS, MIN_BLOB_WIDTH, MAX_BLOB_WIDTH,
                                       MIN_SPEED, MAX_SPEED, color_var=COLOR_VAR,
                                       speed_var=SPEED_VAR, acc_var=ACC_VAR)
        space.add_blob(simple_blob)

    random.seed(2)
    picture = make_2d_pic(space, TIME_STEPS, NOISE)

    #random.seed(2)
    #make_video('video.mp4', space, TIME_STEPS, NOISE)


    show_image(picture)
