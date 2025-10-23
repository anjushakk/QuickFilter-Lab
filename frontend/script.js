// 1. Get references to our HTML elements
const imageUpload = document.getElementById('image-upload');
const originalImage = document.getElementById('original-image');
const filteredImage = document.getElementById('filtered-image');
const loader = document.getElementById('loader');
const downloadLink = document.getElementById('download-link');

// --- NEW: Get references to all filter buttons ---
const grayscaleButton = document.getElementById('grayscale-button');
const sepiaButton = document.getElementById('sepia-button');
const invertButton = document.getElementById('invert-button');

let originalFile = null;
let filteredImageURL = null; // Store the URL for downloading

// 2. Listen for when a user selects a file
imageUpload.addEventListener('change', (event) => {
    originalFile = event.target.files[0];
    
    // Revoke the old object URL to free up memory
    if (filteredImageURL) {
        URL.revokeObjectURL(filteredImageURL);
        filteredImageURL = null;
    }

    if (originalFile) {
        const reader = new FileReader();
        reader.onload = (e) => {
            originalImage.src = e.target.result;
        };
        reader.readAsDataURL(originalFile);
        
        // Reset the UI
        filteredImage.src = ""; // Clear old filtered image
        loader.style.display = 'none'; // Hide loader
        downloadLink.style.display = 'none'; // Hide download button
    }
});

// --- NEW: Reusable function to apply any filter ---
const applyFilter = async (filterName) => {
    if (!originalFile) {
        alert("Please upload an image first!");
        return;
    }

    // Show loader and reset UI
    loader.style.display = 'block';
    filteredImage.src = "";
    downloadLink.style.display = 'none';

    // Revoke the old object URL if it exists
    if (filteredImageURL) {
        URL.revokeObjectURL(filteredImageURL);
        filteredImageURL = null;
    }

    const formData = new FormData();
    formData.append('file', originalFile);

    console.log(`Sending image to backend for ${filterName} filter...`);

    try {
        // Use a dynamic URL based on the filter name
        const response = await fetch(`http://127.0.0.1:8000/process-image/${filterName}`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Image processing failed.');
        }

        const imageBlob = await response.blob();
        filteredImageURL = URL.createObjectURL(imageBlob);

        // Display the new filtered image
        filteredImage.src = filteredImageURL;
        console.log("Success! Filtered image received.");

        // Setup and show the download button
        downloadLink.href = filteredImageURL;
        downloadLink.download = `${filterName}_${originalFile.name}`; 
        downloadLink.style.display = 'inline-block'; // Show the button!

    } catch (error) {
        console.error('Error:', error);
        alert(`An error occurred: ${error.message}. Make sure the backend server is running.`);
    } finally {
        // Always hide the loader when done
        loader.style.display = 'none';
    }
};

// --- NEW: Add event listeners to all buttons ---
grayscaleButton.addEventListener('click', () => applyFilter('grayscale'));
sepiaButton.addEventListener('click', () => applyFilter('sepia'));
invertButton.addEventListener('click', () => applyFilter('invert'));