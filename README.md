### Table of Contents

| Section                       | Description                                 |
|-------------------------------|---------------------------------------------|
| 1. [Introduction](#introduction)              | Brief overview of the project.              |
| 2. [Requirements](#requirements)              | List of software and hardware requirements. |
| 3. [Setup and Installation](#installation)          | Steps to set up and run the project.        |
| 4. [Usage](#usage)                          | How to use the scanner and its features.    |
| 5. [Detailed Explanation](#process) | In-depth look into the project's processes.  |
| 6. [Contribution Guidelines](#contribution)  | How to contribute to the project.           |

---

### Introduction  

This Document Scanner project takes an image (supporting `.heic` format as well) as input, detects the document within the image, corrects its perspective, and produces a clean, scanned version of the document.  

---

### Features  
- **HEIC to PNG Conversion**: Converts HEIC format images to PNG for processing. 
- **Edge Detection**: Uses the Canny edge detector after converting the image to grayscale and applying Gaussian blur for accurate edge detection. 
- **Contour Detection**: Finds the document's contour based on the hypothesis that the largest contour with 4 edges is our target document. 
- **Perspective Transformation**: Applies a four-point perspective transformation to obtain a top-down view of the document. 
- **Thresholding**: Uses a local thresholding technique with a Gaussian method for clarity.  

---

### Requirements  
- Python 3.x 
- OpenCV 
- imutils 
- skimage  

---

### Installation  

1. Clone the repository: 
```bash 
git clone [your-repository-link]
```

2. Navigate to the project directory:
```bash
cd [your-project-directory]
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

---

### Usage

To scan an image:
```bash
python [script-name].py --image [path-to-input-image]
```


The output will be saved in `./images/scanned_images/` with a prefix `scanned_`.

---

### Process

1. **HEIC Conversion**: `.heic` images are first converted to `.png` format for further processing.
2. **Edge Detection**: Convert image to grayscale, apply Gaussian blur, and then Canny edge detection.
3. **Finding Contours**: Contours in the image are identified, and the largest one with 4 edges is considered the document's outline.
4. **Perspective Transformation**: Using the detected contour, the image is warped to give a bird's-eye view of the document.
5. **Thresholding**: A local threshold is applied to give the image a clean, scanned appearance.


<details>
  <summary><b>Detailed Explanation</b></summary>

##### 1. HEIC to PNG Conversion

In modern devices, especially Apple products, images can be saved in the `.heic` format, which provides high-quality images at nearly half the size of JPEG. This project has a built-in functionality to convert these `.heic` images to `.png` format, ensuring compatibility with a broader range of image processing tools and libraries.

- **Function**: `convert_heic2png(args["image"])`
  
##### 2. Edge Detection

Edge detection is a crucial step in the process to find the boundaries of the document within the image.

- **Grayscale Conversion**: The image is first converted to grayscale using OpenCV's `cvtColor` function, which helps in highlighting the important features (edges) without the distraction of color.

- **Gaussian Blur**: A Gaussian blur filter is then applied. This step reduces high-frequency noise that can affect edge detection. The kernel size chosen is `5x5`, which means each pixel value is set to a weighted average of its neighbors, effectively blurring the image.

- **Canny Edge Detection**: The Canny function in OpenCV is then used to detect edges in the image. Two threshold values, 75 and 200 in this case, help in removing weak edges and preserving strong ones.

##### 3. Finding the Contours

The objective here is to detect the document's outline. The code is based on the hypothesis that the largest contour with exactly 4 edges is our document.

- **Contour Detection**: The `findContours` function from OpenCV is used to retrieve all the contours in the image. Contours are simply the boundaries of the connected components in an image. 

- **Contour Filtering**: From all detected contours, only the five largest are kept for further examination, reducing processing time and increasing accuracy.

- **Polygon Approximation**: For each of these contours, a polygon approximation is performed. The purpose is to find a polygon that closely resembles the contour shape. We're particularly interested in contours that approximate to a polygon with 4 vertices (rectangle), suggesting a potential document.

##### 4. Perspective Transformation

Once we have the document's four corners, we perform a perspective transformation to obtain a top-down, "bird's-eye view" of the document, as if it was scanned directly facing the scanner.

- **Four-point Transform**: The custom function `four_point_transform` is used. This function takes the original image and the coordinates of the document's four corners to provide a warped version of the document.

##### 5. Thresholding

After obtaining a top-down view of the document, we want to enhance its readability and give it a "scanned" appearance.

- **Grayscale Conversion**: The warped image is first converted to grayscale.

- **Adaptive Thresholding**: Instead of a global thresholding value, an adaptive method called `threshold_local` from the `skimage` library is used. This method computes a threshold for small regions of the image, giving a more fine-tuned result. The method chosen is `gaussian` which provides a balanced thresholding.

</details>

---

### Contributing

Contributions are welcome! Please ensure that you test your changes thoroughly before submitting a pull request.

### License

This project is licensed under the [MIT License](https://chat.openai.com/c/link-to-license-file).