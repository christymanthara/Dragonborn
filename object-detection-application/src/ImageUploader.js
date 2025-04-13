import React, { useState } from "react";
import axios from "axios";

const ImageUploader = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [detections, setDetections] = useState([]);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);

    // Preview image
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      alert("Please upload an image file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);
      const response = await axios.post("http://"+document.location.hostname+":8000/detect", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log(response.data);  // Check if this is showing correct data

      setDetections(response.data.detections);
      setLoading(false);
    } catch (error) {
      console.error("Error uploading the file:", error);
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h2>Upload an Image for Object Detection</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept="image/*" />
        <button type="submit" disabled={!selectedFile || loading}>
          {loading ? "Detecting..." : "Upload and Detect"}
        </button>
      </form>

      {/* Display Image Preview */}
      {imagePreview && (
        <div>
          <h3>Image Preview:</h3>
          <img src={imagePreview} alt="Preview" style={{ width: "400px", marginTop: "10px" }} />
        </div>
      )}

      {/* Display Detection Results */}
      {detections.length > 0 ? (
        <div style={{ marginTop: "20px" }}>
            <h3>Detections:</h3>
            <ul>
            {detections.map((detection, index) => (
                <li key={index}>
                <strong>{detection.class}</strong> - Confidence: {Math.round(detection.confidence * 100)}% <br />
                Bounding Box: [ {detection.bbox.join(", ")} ]
                </li>
            ))}
            </ul>
        </div>
        ) : (
        <p>No detections to display</p>
        )}

    </div>
  );
};

export default ImageUploader;
