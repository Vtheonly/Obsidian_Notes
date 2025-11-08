# Lab 1: Environment Setup and Basic Image Manipulation

**Objective:** To set up the Python development environment using PyCharm and to understand how digital images are represented and manipulated at the pixel level using the OpenCV and NumPy libraries.

## 1. Environment and Project Setup (Exercise 1)

This initial exercise involves configuring the necessary tools for the course. The chosen tools provide a standard, powerful stack for computer vision tasks.

-   **Python:** The programming language used for its simplicity, readability, and extensive ecosystem of libraries.
-   **PyCharm (Community Edition):** An Integrated Development Environment (IDE) that provides code editing, debugging, and project management features, streamlining the development process.
-   **Virtual Environment:** PyCharm creates a virtual environment for the project.
    -   **Insight:** A virtual environment is a critical best practice. It isolates the project's dependencies (like specific versions of OpenCV and NumPy) from other Python projects on the system. This prevents version conflicts and ensures the project is reproducible on other machines.
-   **OpenCV-Python:** A specialized library for computer vision. It provides a vast collection of functions for image/video analysis, processing, and machine learning.
-   **NumPy:** A fundamental library for numerical computing in Python.
    -   **Insight:** OpenCV represents images as NumPy arrays. Therefore, proficiency in NumPy is essential for any efficient image manipulation in Python.

## 2. Fundamental Image Operations (Exercise 2)

This section covers the core mechanics of loading, displaying, and accessing image data.

### Loading and Displaying an Image

The following functions are the primary tools for image I/O:
-   `cv2.imread('path/to/image', flag)`: Loads an image from a file. The flag determines the loading mode (e.g., `cv2.IMREAD_COLOR`, `cv2.IMREAD_GRAYSCALE`).
-   `cv2.imshow('Window Name', image_array)`: Displays an image in a window.
-   `cv2.waitKey(0)`: Pauses the program execution indefinitely until a key is pressed. This is necessary to keep the image window visible.
-   `cv2.destroyAllWindows()`: Closes all open OpenCV windows.

### Image Representation in Memory

The most critical concept is that a digital image, when loaded by OpenCV, is nothing more than a NumPy array.

-   **Grayscale Image:** A 2D array where each element is an integer (typically 0-255) representing the intensity of a single pixel.
-   **Color Image:** A 3D array of shape `(height, width, channels)`. Each element is a vector representing the color of a pixel.

### Accessing Image Properties

The `shape` attribute of the NumPy array provides the image's dimensions.
-   `height, width = gray_image.shape`
-   `height, width, channels = color_image.shape`
    -   `height`: The number of pixel rows.
    -   `width`: The number of pixel columns.
    -   `channels`: The number of color components per pixel (e.g., 3 for BGR).

### Accessing and Modifying Pixel Values

Pixel values are accessed using NumPy's array indexing.
-   **Syntax:** `image[row, column]`
-   **Coordinates vs. Indexing:** It is crucial to distinguish between `(x, y)` Cartesian coordinates and `(row, col)` NumPy indexing.
    -   `x` corresponds to `column`.
    -   `y` corresponds to `row`.
    -   Therefore, accessing a pixel at `(x=150, y=100)` is done with `pixel = image[100, 150]`.
-   **Color Order:** OpenCV loads color images in **BGR (Blue, Green, Red)** order by default, not the more common RGB.
    -   `pixel = color_image[100, 150]` would return a list like `[blue_value, green_value, red_value]`.
-   **Modification:** To change a pixel's color, simply assign a new value:
    `color_image[100, 150] = [255, 0, 0]` (sets the pixel to pure blue).

## 3. Fixed Thresholding (Exercise 3)

Thresholding is a foundational segmentation technique used to create a binary image from a grayscale image.

-   **Concept:** A threshold value is chosen. All pixels with an intensity value *above* the threshold are set to a maximum value (e.g., 255 for white), and all pixels with an intensity value *at or below* the threshold are set to a minimum value (e.g., 0 for black).
-   **Algorithm:**
    ```python
    for each pixel in the grayscale image:
        If pixel_value > threshold:
            set output_pixel_value = 255
        Else:
            set output_pixel_value = 0
    ```
-   **Purpose:** This process is used to isolate objects of interest from the background, assuming they have a distinct intensity range. It is a simple yet effective way to preprocess an image for further analysis, like object counting or shape analysis.