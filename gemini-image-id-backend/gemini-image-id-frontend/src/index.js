import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [image, setImage] = useState(null);
    const [identificationResult, setIdentificationResult] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleImageChange = (event) => {
        setImage(event.target.files[0]);
    };

    const handleSubmit = async () => {
        if (!image) {
            setError('Please select an image.');
            return;
        }

        setLoading(true);
        setError('');
        setIdentificationResult('');

        const formData = new FormData();
        formData.append('image', image);

        try {
            const response = await axios.post('http://localhost:5000/identify-image', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setIdentificationResult(response.data.identification);
        } catch (err) {
            console.error("Error sending image:", err);
            setError('Failed to upload and identify the image.');
            setIdentificationResult('');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Image Identification using Gemini</h1>
            <input type="file" accept="image/*" onChange={handleImageChange} />
            <button onClick={handleSubmit} disabled={loading}>
                {loading ? 'Identifying...' : 'Identify Image'}
            </button>

            {error && <p style={{ color: 'red' }}>{error}</p>}

            {identificationResult && (
                <div>
                    <h2>Identification Result:</h2>
                    <p>{identificationResult}</p>
                </div>
            )}
        </div>
    );
}

export default App;