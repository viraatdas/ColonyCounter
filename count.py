import cv2
import numpy as np

def count_colonies_within_petri_dish(image_path):
    # Constants
    approximate_colony_radius_pixels = 15  # Adjusted approximate radius of a colony in pixels

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

    if not contours:
        return None, 0  # If no contours are found

    # Sort contours by area and assume the largest one is the Petri dish
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    petri_dish_contour = contours[0]
    (pd_x, pd_y), pd_radius = cv2.minEnclosingCircle(petri_dish_contour)

    colony_count = 0
    for contour in contours[1:]:  # Exclude the Petri dish contour
        (x, y), radius = cv2.minEnclosingCircle(contour)
        distance_from_center = np.sqrt((x - pd_x) ** 2 + (y - pd_y) ** 2)
        
        # Check if the colony is within the Petri dish and matches the expected size
        if distance_from_center + radius <= pd_radius and radius <= approximate_colony_radius_pixels:
            cv2.circle(image, (int(x), int(y)), int(radius), (0, 0, 255), 2)  # Draw the colony
            colony_count += 1

    # Draw the Petri dish contour for visualization
    cv2.drawContours(image, [petri_dish_contour], -1, (0, 255, 0), 3)

    # Add the colony count to the image for visualization
    cv2.putText(image, f"Colony Count: {colony_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return image, colony_count


# The function is ready to be called with the path to your image file
# Example usage:
sample_file = "sample-images/input/sample_1.png"
result_image, count = count_colonies_within_petri_dish(sample_file)
cv2.imshow('Result Image', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
