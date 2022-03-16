"""
Python Image Representation (modified from MIT 6.865)
"""
import numpy as np
import png


class Image:
    def __init__(self, x_pixels=0, y_pixels=0, num_channels=0, filename=''):
        # input either filename OR x_pixels, y_pixels, and num_channels
        self.input_path = 'input/'
        self.output_path = 'output/'
        # folders for I/O
        if x_pixels and y_pixels and num_channels:  # check if the user has passed in the inputs
            self.x_pixels = x_pixels
            self.y_pixels = y_pixels
            self.num_channels = num_channels
            self.array = np.zeros((x_pixels, y_pixels, num_channels))  # create an empty 3D array of zeroes
        elif filename:
            self.array = self.read_image(filename)
            self.x_pixels, self.y_pixels, self.num_channels = self.array.shape
        else:
            raise ValueError("Please input a filename OR specify the dimensions of the image")

    def read_image(self, filename, gamma=2.2):
        '''
        read PNG RGB image, return 3D numpy array organized along Y, X, channel
        values are float, gamma is decoded
        '''
        im = png.Reader(self.input_path + filename).asFloat()  # using the png file and passing in the filename
        resized_image = np.vstack(list(im[2]))
        resized_image.resize(im[1], im[0], 3)
        resized_image = resized_image ** gamma
        return resized_image

    def write_image(self, output_file_name, gamma=2.2):
        '''
        3D numpy array (Y, X, channel) of values between 0 and 1 -> write to png
        '''
        im = np.clip(self.array, 0, 1)
        y, x = self.array.shape[0], self.array.shape[1]
        im = im.reshape(y, x * 3)
        writer = png.Writer(x, y)
        with open(self.output_path + output_file_name, 'wb') as f:
            writer.write(f, 255 * (im ** (1 / gamma)))

        self.array.resize(y, x, 3)  # mutated the method in the first step of the function


if __name__ == '__main__':
    im = Image(filename='lake.png')
    im.write_image('test.png') # to test if I/O is working
