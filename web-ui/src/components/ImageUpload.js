import React, { useState, useRef } from 'react';

const ImageUpload = () => {
  const [images, setImages] = useState([]);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    if (event.target.files) {
      const filesArray = Array.from(event.target.files).map((file) => ({
        url: URL.createObjectURL(file),
        name: file.name,
      }));
      setImages(filesArray);
    }
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    images.forEach((image, index) => {
      formData.append(`image${index}`, image.url);
    });

    try {
      const response = await fetch('http://127.0.0.1:5000/count-colonies', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        alert('Images submitted successfully!');
      } else {
        alert('Failed to submit images.');
      }
    } catch (error) {
      console.error('Submission error:', error);
      alert('An error occurred while submitting the images.');
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="image-upload-container">
      <input
        type="file"
        multiple
        onChange={handleFileChange}
        accept="image/*"
        style={{ display: 'none' }}
        ref={fileInputRef}
      />
      <button className="image-upload-btn" onClick={handleButtonClick}>Upload Images</button>
      <div className="image-preview">
        {images.map((image, index) => (
          <img key={index} src={image.url} alt={image.name} />
        ))}
      </div>
      <button className="image-upload-btn" onClick={handleSubmit}>Count Colonies</button>
    </div>
  );
};

export default ImageUpload;
