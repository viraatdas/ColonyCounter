import cv2
import numpy as np

def count_colonies_with_canny_edge_detection(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 100, 200)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming the largest contour is the Petri dish, sort contours by area
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    if not contours:
        return None, 0  # If no contours are found

    # Assume the largest contour is the Petri dish and exclude it
    petri_dish_contour = contours[0]
    inner_contours = contours[1:]  # All other contours are potential colonies

    # Draw contours for visualization (optional)
    cv2.drawContours(image, [petri_dish_contour], -1, (0, 255, 0), 2)
    for contour in inner_contours:
        cv2.drawContours(image, [contour], -1, (0, 0, 255), 1)

    # Count of the inner contours is the count of colonies
    colony_count = len(inner_contours)

    # Optionally add the colony count to the image
    cv2.putText(image, f"Colony Count: {colony_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return image, colony_count




# The function is ready to be called with the path to your image file
# Example usage:
sample_file = "sample-images/input/sample_1.png"
result_image, count = count_colonies_with_canny_edge_detection(sample_file)
cv2.imshow('Result Image', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
