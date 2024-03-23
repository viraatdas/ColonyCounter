import React, { useState } from 'react';

const ImageUpload = () => {
  const [images, setImages] = useState([]);

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
        // Handle response here
        alert('Images submitted successfully!');
      } else {
        alert('Failed to submit images.');
      }
    } catch (error) {
      console.error('Submission error:', error);
      alert('An error occurred while submitting the images.');
    }
  };

  return (
    <div>
      <input type="file" multiple onChange={handleFileChange} accept="image/*" />
      <div>
        {images.map((image, index) => (
          <img key={index} src={image.url} alt={image.name} style={{ width: '100px', height: 'auto' }} />
        ))}
      </div>
      <button onClick={handleSubmit}>Count Colonies</button>
    </div>
  );
};

export default ImageUpload;
