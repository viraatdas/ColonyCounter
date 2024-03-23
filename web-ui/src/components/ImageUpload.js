import React, { Component } from 'react';
import BeforeAfterSlider from 'react-before-after-slider';

class ImageUpload extends Component {
  state = {
    images: [], // Each object in this array will hold original, processed, and count
  };

  fileInputRef = React.createRef();

  handleFileChange = (event) => {
    const files = event.target.files;
    if (files) {
      this.processFiles(Array.from(files));
    }
  };

  processFiles = (files) => {
    files.forEach(file => {
      const reader = new FileReader();
      reader.onloadend = () => {
        // Add the original image to state for display
        const originalUrl = reader.result;
        this.setState(prevState => ({
          images: [...prevState.images, { original: originalUrl, processed: '', count: 0 }],
        }));
        // Here you'd upload the file and update the state with the processed image and count
        // This is just a placeholder to show structure
        this.uploadAndProcessImage(file);
      };
      reader.readAsDataURL(file);
    });
  };

  uploadAndProcessImage = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/count-colonies', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        this.setState(prevState => ({
          images: prevState.images.map(img => img.original === URL.createObjectURL(file) ? {
            ...img,
            processed: `data:image/jpeg;base64,${data.result_image_base64}`,
            count: data.colony_count
          } : img)
        }));
      } else {
        console.error('Failed to submit image');
      }
    } catch (error) {
      console.error('Submission error:', error);
    }
  };

  handleButtonClick = () => {
    this.fileInputRef.current.click();
  };

  render() {
    return (
      <div className="image-upload-container">
        <input
          type="file"
          multiple
          onChange={this.handleFileChange}
          accept="image/*"
          style={{ display: 'none' }}
          ref={this.fileInputRef}
        />
        <button onClick={this.handleButtonClick}>Upload Images</button>
        {this.state.images.map((img, index) => (
          img.processed && <div key={index}>
            <BeforeAfterSlider
              before={img.original}
              after={img.processed}
              width={640}
              height={480}
            />
            <p>Colony Count: {img.count}</p>
          </div>
        ))}
      </div>
    );
  }
}

export default ImageUpload;
