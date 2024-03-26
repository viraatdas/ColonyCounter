import cv2
import numpy as np
import argparse


def count_colonies_within_petri_dish(image_path):
    # Constants
    # Adjusted approximate radius of a colony in pixels
    approximate_colony_radius_pixels = 15
    # Margin from the edge of the Petri dish where colonies will not be counted
    edge_exclusion_margin = 50

    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Apply binary thresholding
    _, binary = cv2.threshold(
        enhanced, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return binary, None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Count colonies in a Petri dish image')
    parser.add_argument('image_path', type=str,
                        help='Path to the input image file')
    args = parser.parse_args()

    sample_file = args.image_path
    result_image, count = count_colonies_within_petri_dish(sample_file)
    cv2.imshow('Result Image', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
