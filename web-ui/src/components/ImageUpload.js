import React, { useState, useRef } from 'react';

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [resultImage, setResultImage] = useState('');
  const [colonyCount, setColonyCount] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
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
        headers: {
          // Don't set Content-Type to multipart/form-data here, fetch will do it automatically
        },
      });

      if (response.ok) {
        const data = await response.json();
        setResultImage(`data:image/jpeg;base64,${data.result_image_base64}`);
        setColonyCount(data.colony_count);
        alert('Images submitted successfully!');
      } else {
        const errorText = await response.text();
        alert(`Failed to submit images. Server responded with status ${response.status}: ${errorText}`);
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
        onChange={handleFileChange}
        accept="image/*"
        style={{ display: 'none' }}
        ref={fileInputRef}
      />
      <button className="image-upload-btn" onClick={handleButtonClick}>Upload Image</button>
      <button className="image-upload-btn" onClick={handleSubmit}>Count Colonies</button>
      {colonyCount != null && (
        <div>
          <p>Colony Count: {colonyCount}</p>
          <img src={resultImage} alt="Result" />
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
