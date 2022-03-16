"""
Image Manipulation - Python (Leeda Foroughi)
"""

from image import Image
import numpy as np

# def brighten(image, factor):
#     # when brightening, increase each channel by a factor amount
#     # factor is a value > 0, depending on how much you want to brighten (< 1 = darken, > 1 = brighten)
#     x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
#     new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # create a new array to copy values to
#     # use NumPy to multiple all the pixels by the factor (Vectorized)
#     new_image.array = image.array * factor
#     return new_image
#
# def adjust_contrast(image, factor, mid):
#     # adjust the contrast by increasing the difference from the user-defined midpoint by a factor amount
#     x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
#     new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # create a new array to copy values to
#     # use NumPy to make changes to image (Vectorized)
#     new_image.array = (image.array - mid) * factor + mid
#     return new_image

def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be the pixels/neighbors to the left/right, top/bottom, and diagonals)
    # kernel size is always an *odd* number
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # create a new array to copy values to
    neighbor_range = kernel_size // 2  # this is a variable that tells us how many neighbors we actually look at (ie for a kernel of 3, this value should be 1)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                # iterating through each neighboring pixel and summing
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_image.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_image.y_pixels-1, y+neighbor_range)+1):
                        total += image.array[x_i, y_i, c]
                new_image.array[x, y, c] = total / (kernel_size ** 2)
    return new_image

def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we can see
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # create a new array to copy values to
    neighbor_range = kernel.shape[0] // 2  # this is a variable that shows how many neighboring pixels there are (ie for a 3x3 kernel, this value should be 1)
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_image.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_image.y_pixels-1, y+neighbor_range)+1):
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_image.array[x, y, c] = total
    return new_image

def combine_images(image1, image2):
    # combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be equal
    x_pixels, y_pixels, num_channels = image1.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # create a new array to copy values to
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_image.array[x, y, c] = (image1.array[x, y, c]**2 + image2.array[x, y, c]**2)**0.5
    return new_image
    
if __name__ == '__main__':
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')

    # Brightening
    # brightened_image = brighten(city, 2)
    # brightened_image.write_image('brightened.png')
    #
    # # # Darkening
    # darkened_im = brighten(lake, 0.3)
    # darkened_im.write_image('darkened.png')
    # #
    # # Increase contrast
    # incr_contrast = adjust_contrast(lake, 2, 0.5)
    # incr_contrast.write_image('increased_contrast.png')
    #
    # # Decrease contrast
    # decr_contrast = adjust_contrast(lake, 0.5, 0.5)
    # decr_contrast.write_image('decreased_contrast.png')
    #
    # Blur using kernel 3
    # blur_3 = blur(city, 3)
    # blur_3.write_image('blur_k3.png')
    #
    #
    # Apply a sobel edge detection kernel on the x and y axis
    sobel_x = apply_kernel(city, np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]]))

    sobel_x.write_image('edge_x.png')

    sobel_y = apply_kernel(city, np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]]))
    sobel_y.write_image('edge_y.png')

   # combine these to make an edge detector
    sobel_xy = combine_images(sobel_x, sobel_y)
    sobel_xy.write_image('edge_xy.png')

