import blob
import numpy as np
import random
import matplotlib.pyplot as plt


def make_3d_pic(dspace, frames, noise_amount=0):
    """
    This takes a BlobSpace "dspace" and advances it forward
    "frames" times. Each time it appends the state of the
    BlobSpace onto the end of a numpy array. At each step
    a random number between plus and minus "noise_amount"
    is added to each entry.
    """
    ret = np.empty((frames, dspace.width, 3), dtype=int)
    for frame in range(frames):
        image_2d = dspace.create_2d_image()
        add_noise(image_2d, noise_amount)
        ret[frame] = image_2d
        dspace.time_step()
    return ret


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


def make_random_blob(min_pos, max_pos, min_width, max_width, min_speed, max_speed, color_var=0, speed_var=0):
    """
    This makes a random blob within the specified ranges. Note that
    color_var controls the range of colors within a given blob.
    """
    position = random.randint(min_pos, max_pos)
    width = random.randint(min_width, max_width)
    speed = random.randint(min_speed, max_speed)
    color = make_random_color()
    values = np.full((width, 3), color)
    for value in range(width):
        for index in range(3):
            new_value = values[value][index] + random.randint(-1 * color_var, color_var)
            new_value = min(255, new_value)
            new_value = max(0, new_value)
            values[value][index] = new_value
    return blob.Blob(position, speed, values, speed_var=speed_var)

def show_image(array):
    plt.imshow(array)
    plt.show()


if __name__ == '__main__':
    NUM_BLOBS = 100
    SPACE_WIDTH = 600
    TIME_STEPS = 150
    MIN_SPEED = -5
    MAX_SPEED = 5
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
    SPEED_VAR = 1   # As of now this should be 0 or 1; I haven't
                    # implemented fractions of pixels.
    NOISE = 20      # Works well between 0 and 100.

    space = blob.BlobSpace(SPACE_WIDTH, BACKGROUND)

    for i in range(NUM_BLOBS):
        simple_blob = make_random_blob(MIN_POS, MAX_POS, MIN_BLOB_WIDTH, MAX_BLOB_WIDTH,
                                       MIN_SPEED, MAX_SPEED, color_var=COLOR_VAR, speed_var=SPEED_VAR)
        space.add_blob(simple_blob)

    picture = make_3d_pic(space, 200, NOISE)
    show_image(picture)
