import React, { useState, useRef } from 'react';

const ImageUpload = () => {
  const [images, setImages] = useState([]); // Store the images for preview
  const [selectedFile, setSelectedFile] = useState(null); // The file to be sent
  const [resultImage, setResultImage] = useState(''); // The processed image
  const [colonyCount, setColonyCount] = useState(null); // The colony count result
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    if (event.target.files) {
      const filesArray = Array.from(event.target.files).map((file) => ({
        url: URL.createObjectURL(file),
        name: file.name,
      }));
      setSelectedFile(event.target.files[0]); // Assuming you're processing the first selected file
      setImages(filesArray);
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert('Please select a file before submitting.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/count-colonies', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResultImage(`data:image/jpeg;base64,${data.result_image_base64}`);
        setColonyCount(data.colony_count);
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
          <img key={index} src={image.url} alt={image.name} style={{ width: '100px', height: 'auto' }} />
        ))}
      </div>
      <button className="image-upload-btn" onClick={handleSubmit}>Count Colonies</button>
      {colonyCount != null && (
        <div>
          <p>Colony Count: {colonyCount}</p>
          <img src={resultImage} alt="Processed Result" />
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
