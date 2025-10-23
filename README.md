# QuickFilter Lab 📸

A full-stack web application that applies real-time filters to your photos using a Python/FastAPI backend and a vanilla JavaScript frontend.

![Uploading image.png…]()

### About The Project

This project is a complete web tool built from scratch. It allows a user to upload any image, apply an artistic filter (like Grayscale, Sepia, or Invert), and get the processed image back instantly.

It demonstrates a modern full-stack workflow by separating a powerful **Python backend** (which does all the heavy lifting) from a dynamic, responsive **JavaScript frontend** (which the user sees and interacts with).

### ✨ Features

*   **Real-time Filtering:** Apply Grayscale, Sepia, and Invert filters.
    
*   **Dynamic UI:** A clean, dark-mode interface built with vanilla HTML, CSS, and JS.
    
*   **Image Upload:** Modern file selector for any image type.
    
*   **Loading State:** A CSS spinner appears while the backend is processing the image.
    
*   **Download Button:** Instantly download your newly filtered image.
    

### 🛠️ Tech Stack

*   **Backend:** Python, FastAPI, Uvicorn
    
*   **Image Processing:** Pillow, NumPy
    
*   **Frontend:** Vanilla JavaScript (ES6+), HTML5, CSS3
    

### 🚀 Getting Started

To run this project locally, you will need two terminals open.

#### 1\. Backend (Python/FastAPI)

1.  Navigate to the `backend` folder:
    
        cd backend
        
    
2.  (Optional but recommended) Create and activate a virtual environment:
    
        # On Windows
        python -m venv venv
        .\venv\Scripts\activate
        
        # On macOS/Linux
        python3 -m venv venv
        source venv/bin/activate
        
    
3.  Install the required libraries:
    
        pip install -r requirements.txt
        
    
4.  Run the FastAPI server:
    
        uvicorn main:app --reload
        
    
    The backend will now be running on `http://122.0.0.1:8000`.
    

#### 2\. Frontend (JavaScript)

1.  Navigate to the `frontend` folder.
    
2.  Open the `index.html` file directly in your web browser (e.g., by double-clicking it).
    

That's it! You can now upload an image and apply filters.
