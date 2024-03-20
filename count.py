import cv2
import numpy as np

def count_colonies(image_path):
  image = cv2.imread(image_path)

  # Convert the image to grayscale
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Apply thresholding to create a binary image
  _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

  # Find contours in the binary image
  contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Count the number of contours (colonies)
  colony_count = len(contours)

  # Create a copy of the original image to draw on
  output = image.copy()

  # Iterate over each contour and draw a point at its center
  for contour in contours:
      # Calculate the moments of the contour
      moments = cv2.moments(contour)
      
      if moments["m00"] != 0:
          # Calculate the centroid coordinates
          cX = int(moments["m10"] / moments["m00"])
          cY = int(moments["m01"] / moments["m00"])
          
          # Draw a point at the centroid
          cv2.circle(output, (cX, cY), 3, (0, 0, 255), -1)

  # Add the colony count to the output image
  cv2.putText(output, f"Colony Count: {colony_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

  # Display the output image
  cv2.imshow('Bacterial Colonies', output)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

sample_file = "sample-images/sample_1.png"
count_colonies(sample_file)