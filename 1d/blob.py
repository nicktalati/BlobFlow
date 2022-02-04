import random
import numpy as np


class Blob:
    """
    A blob represents a horizontal slice of a 3D picture; it is a 1D numpy
    array with values specified in "entries". Within a BlobSpace it starts
    at the specified position "pos" and moves with speed "speed", which
    changes at each time step if "speed_var" is nonzero.
    """
    def __init__(self, pos, speed, entries, speed_var=0, acc_var=0.0):
        self.entries = np.array(entries)
        self.pos = pos
        self.speed = speed
        self.speed_var = speed_var
        self.acc_var = acc_var

    def __str__(self):
        return '<Blob object at position ' + str(self.pos) + ': ' + str(self.entries) + '>'

    def time_step(self):
        """
        Tells the blob how to advance its position in time.
        """
        self.speed += random.uniform(-1 * self.acc_var, self.acc_var)
        self.pos += self.speed + self.speed * random.uniform(-1 * self.speed_var, self.speed_var)

    def is_covering(self, pixel):
        """
        Determines if a blob is covering a pixel, where "pixel" represents
        the index of a given pixel in the BlobSpace.
        """
        if pixel >= self.pos and pixel < self.pos + len(self.entries):
            return True
        return False

    def get_color(self, pixel):
        """
        Returns the color of the blob at a given pixel (relative to pos).
        """
        return self.entries[pixel]



class BlobSpace:
    """
    A BlobSpace is a collection of blobs. It has a specified window
    width given by "width" and a background color given by "background".
    """
    def __init__(self, width=100, background=255):
        self.width = width
        self.blobs = []
        self.background = background

    def add_blob(self, blob):
        self.blobs.append(blob)

    def time_step(self):
        """
        This advances each blob one time step.
        """
        for elem in self.blobs:
            elem.time_step()

    def create_1d_image(self):
        """
        This essentially prints out the BlobSpace. At each pixel, the
        color returned is the color of the earliest-indexed blob in
        blobs that covers the given pixel. If no such blobs do, the
        background color is returned.
        """
        ret = np.empty((self.width, 3))
        for pixel in range(self.width):
            ret[pixel] = self.background
            for blob in self.blobs:
                if blob.is_covering(pixel):
                    ret[pixel] = blob.get_color(int(pixel - blob.pos))
                    break
        return ret

