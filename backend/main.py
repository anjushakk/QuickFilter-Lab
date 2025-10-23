import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageOps
import io

# 1. Create the FastAPI app
app = FastAPI()

# 2. Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- NEW: Filter Logic ---

def apply_grayscale(img: Image.Image) -> Image.Image:
    """Converts image to grayscale."""
    return img.convert('L')

def apply_sepia(img: Image.Image) -> Image.Image:
    """Applies a sepia filter using NumPy."""
    # Convert to RGB first (in case it's RGBA)
    img_rgb = img.convert('RGB')
    img_array = np.array(img_rgb)
    
    # Sepia transformation matrix
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    
    # Apply the dot product
    sepia_array = img_array.dot(sepia_matrix.T)
    
    # Clip values to be in the 0-255 range
    sepia_array = np.clip(sepia_array, 0, 255)
    
    # Convert back to a PIL Image
    return Image.fromarray(sepia_array.astype(np.uint8))

def apply_invert(img: Image.Image) -> Image.Image:
    """Inverts the image colors."""
    # Convert to RGB first (in case it's RGBA)
    img_rgb = img.convert('RGB')
    return ImageOps.invert(img_rgb)

# --- NEW: Generic Helper to process and return image ---

def process_image(file_bytes: bytes, filter_function) -> bytes:
    """Helper to open, filter, and save the image."""
    # Open the image and ensure it's in 'RGB' mode for most filters
    img = Image.open(io.BytesIO(file_bytes))
    
    # Apply the chosen filter function
    filtered_img = filter_function(img)
    
    # Save the new image to a "virtual file" in memory
    img_buffer = io.BytesIO()
    filtered_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)  # Rewind the buffer
    
    return img_buffer.getvalue()

# --- NEW: Dynamic API Endpoint ---
# We now use one endpoint that accepts the filter name

@app.post("/process-image/{filter_name}")
async def process_image_filter(filter_name: str, file: UploadFile = File(...)):
    """
    Receives an image and applies a specified filter.
    """
    image_bytes = await file.read()
    
    filtered_bytes = None
    
    if filter_name == "grayscale":
        filtered_bytes = process_image(image_bytes, apply_grayscale)
    elif filter_name == "sepia":
        filtered_bytes = process_image(image_bytes, apply_sepia)
    elif filter_name == "invert":
        filtered_bytes = process_image(image_bytes, apply_invert)
    else:
        # If filter is not found, return an error
        return JSONResponse(status_code=400, content={"message": "Filter not found"})

    # Return the new image
    return StreamingResponse(io.BytesIO(filtered_bytes), media_type="image/png")

