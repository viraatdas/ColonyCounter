import cv2
import numpy as np

def count_colonies_with_bacteria_mask(image_path):
    # Constants based on your findings
    known_dish_diameter_pixels = 1200  # Known diameter of the petri dish in pixels
    known_colony_diameter_pixels = 20  # Approximate diameter of a colony in pixels

    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve circle detection
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    # Detect circles in the image (the Petri dish is assumed to be the largest circle)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=1000,
                               param1=50, param2=30, minRadius=0, maxRadius=0)

    # If no circles were found, return None
    if circles is None:
        return None, 0

    # Get the largest circle (assumed to be the Petri dish)
    max_circle = max(circles[0, :], key=lambda x: x[2])
    x, y, r = map(int, max_circle)

    # Calculate the scale factor based on the detected petri dish diameter
    scale_factor = r / (known_dish_diameter_pixels / 2)

    # Adjust the expected colony diameter based on the scale factor
    adjusted_colony_diameter = known_colony_diameter_pixels * scale_factor
    adjusted_colony_radius = adjusted_colony_diameter / 2

    # Create a mask for the ROI (region of interest, i.e., the Petri dish)
    mask = np.zeros(gray.shape, dtype="uint8")
    cv2.circle(mask, (x, y), r, 255, -1)

    # Bitwise-AND to isolate the ROI
    roi = cv2.bitwise_and(gray, gray, mask=mask)

    # Threshold the ROI to find the colonies
    _, binary_roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours in the thresholded ROI
    contours, _ = cv2.findContours(binary_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out contours based on the adjusted colony size
    colonies = [cnt for cnt in contours if cv2.minEnclosingCircle(cnt)[1] >= adjusted_colony_radius]

    # Draw the Petri dish circle
    cv2.circle(image, (x, y), r, (0, 255, 0), 2)

    # Draw contours (colonies) and calculate the count
    colony_count = 0
    for colony in colonies:
        (x, y), radius = cv2.minEnclosingCircle(colony)
        if radius >= adjusted_colony_radius:  # Adjust this as necessary
            center = (int(x), int(y))
            cv2.circle(image, center, int(radius), (50, 205, 50), 2)  # Lime green circle
            colony_count += 1

    # Add the colony count to the output image
    cv2.putText(image, f"Colony Count: {colony_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return image, colony_count




# The function is ready to be called with the path to your image file
# Example usage:
sample_file = "sample-images/input/sample_1.png"
result_image, count = count_colonies_with_bacteria_mask(sample_file)
cv2.imshow('Result Image', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
