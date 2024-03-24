import React, { useState, useRef } from "react";
import { BeforeAfter } from "react-simple-before-after";
import sampleImage from "../assets/sample_1.png";

const countColoniesApi =
  "https://colony-counter-c9342bb08f9c.herokuapp.com/count-colonies";
const ImageUpload = () => {
  const sample_image = {
    url: sampleImage,
    name: "sample_1.png",
  };

  const [images, setImages] = useState([sample_image]); // Store the images for preview
  const [resultImages, setResultImages] = useState([]); // Store the processed images for preview
  const [colonyCounts, setColonyCounts] = useState([]); // Store the colony counts for each image
  const [selectedIndex, setSelectedIndex] = useState(0); // The index of the selected image
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    setImages([]);
    if (event.target.files) {
      const filesArray = Array.from(event.target.files).map((file) => ({
        url: URL.createObjectURL(file),
        name: file.name,
      }));
      setImages(filesArray);
      setSelectedIndex(null);
    }
  };

  const handleSubmit = async () => {
    if (images.length === 0) {
      setImages([sample_image]);
    }

    // Initialize empty arrays to store results for each image
    let newResultImages = [];
    let newColonyCounts = [];

    for (let image of images) {
      const formData = new FormData();
      // Retrieve image file from image URL
      const responseToBlob = await fetch(image.url);
      const blob = await responseToBlob.blob();
      formData.append(
        "file",
        new File([blob], image.name, { type: "image/jpeg" })
      );

      try {
        const response = await fetch(countColoniesApi, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          newResultImages.push(
            `data:image/jpeg;base64,${data.result_image_base64}`
          );
          newColonyCounts.push(data.colony_count);
        } else {
          alert("Failed to submit an image.");
          // In a real application, you might want to handle this more gracefully
          return;
        }
      } catch (error) {
        console.error("Submission error for an image:", error);
        alert("An error occurred while submitting an image.");
        // In a real application, you might want to handle this more gracefully
        return;
      }
    }

    // Update the state with the new results after all images have been processed
    setResultImages(newResultImages);
    setColonyCounts(newColonyCounts);
    setSelectedIndex(0);
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleImageSelect = (index) => {
    setSelectedIndex(index);
  };

  const colonyCount = colonyCounts[selectedIndex];
  const resultImage = resultImages[selectedIndex];
  const image = images[selectedIndex];

  return (
    <div className="image-upload-container">
      <input
        type="file"
        multiple
        onChange={handleFileChange}
        accept="image/*"
        style={{ display: "none" }}
        ref={fileInputRef}
      />
      <button className="image-upload-btn" onClick={handleButtonClick}>
        Upload Images
      </button>
      <div className="image-preview">
        {images.map((image, index) => (
          <img
            key={index}
            src={image.url}
            alt={image.name}
            style={{
              width: "100px",
              height: "auto",
              border: selectedIndex === index ? "3px solid red" : "none",
            }}
            onClick={() => handleImageSelect(index)}
          />
        ))}
      </div>
      <button className="image-upload-btn" onClick={handleSubmit}>
        Count Colonies
      </button>
      {colonyCount != null && (
        <div>
          <p>Colony Count: {colonyCount}</p>
          <BeforeAfter beforeImage={image.url} afterImage={resultImage} />
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
