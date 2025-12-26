from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from datetime import datetime
from PIL import Image
import base64
import io
from typing import Optional
import uvicorn
from FaceRecognition import faceRecognitionModule

app = FastAPI(title="Profile Picture Upload API", version="1.0.0")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",  # Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_FOLDER = "profilePicture"
LIVE_CAM_FOLDER = "liveCamphotos"  # New folder for live camera photos
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_RESUME = "resumes"

# Ensure upload folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LIVE_CAM_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_RESUME, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image(file_content: bytes) -> tuple[bool, str]:
    """Validate image file"""
    try:
        # Read image with PIL
        image = Image.open(io.BytesIO(file_content))

        # Check image dimensions
        width, height = image.size
        if width < 50 or height < 50:
            return False, "Image too small (minimum 50x50 pixels)"
        if width > 5000 or height > 5000:
            return False, "Image too large (maximum 5000x5000 pixels)"

        return True, "Valid image"
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Profile Picture Upload API", "status": "running"}


@app.post("/upload-profile-picture")
async def upload_profile_picture(
    profilePhoto: UploadFile = File(...), userId: Optional[str] = Form(None)
):
    """Upload profile picture endpoint"""
    try:
        # Check if file is provided
        if not profilePhoto.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Check file extension
        if not allowed_file(profilePhoto.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only PNG, JPG, JPEG, and GIF files are allowed",
            )

        # Read file content
        file_content = await profilePhoto.read()

        # Check file size
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB",
            )

        # Validate image
        is_valid, message = validate_image(file_content)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)

        # Generate unique filename
        file_extension = profilePhoto.filename.rsplit(".", 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Get file info
        file_size = os.path.getsize(file_path)

        # Get image dimensions
        with Image.open(file_path) as img:
            width, height = img.size

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Profile picture uploaded successfully",
                "data": {
                    "filename": unique_filename,
                    "original_filename": profilePhoto.filename,
                    "file_path": file_path,
                    "file_size": file_size,
                    "dimensions": {"width": width, "height": height},
                    "upload_time": datetime.now().isoformat(),
                    "user_id": userId,
                },
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error uploading profile picture: {str(e)}"
        )

@app.post("/upload-live-cam-photo")
async def upload_live_cam_photo(
    liveCamPhoto: UploadFile = File(...), userId: Optional[str] = Form(None)
):
    """Upload live camera photo endpoint"""
    try:
        # Check if file is provided
        if not liveCamPhoto.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Check file extension
        if not allowed_file(liveCamPhoto.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only PNG, JPG, JPEG, and GIF files are allowed",
            )

        # Read file content
        file_content = await liveCamPhoto.read()

        # Check file size
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB",
            )

        # Validate image
        is_valid, message = validate_image(file_content)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)

        # Generate unique filename
        file_extension = liveCamPhoto.filename.rsplit(".", 1)[1].lower()
        unique_filename = f"livecam_{uuid.uuid4()}.{file_extension}"

        # Save file
        file_path = os.path.join(LIVE_CAM_FOLDER, unique_filename)
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Get file info
        file_size = os.path.getsize(file_path)

        # Get image dimensions
        with Image.open(file_path) as img:
            width, height = img.size

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Live camera photo uploaded successfully",
                "data": {
                    "filename": unique_filename,
                    "original_filename": liveCamPhoto.filename,
                    "file_path": file_path,
                    "file_size": file_size,
                    "dimensions": {"width": width, "height": height},
                    "upload_time": datetime.now().isoformat(),
                    "user_id": userId,
                },
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error uploading live camera photo: {str(e)}"
        )


@app.post("/face-recognition")
async def face_recognition(
    profilePhotoPath: str = Form(...), liveCamPhotoPath: str = Form(...)
):
    """Face recognition endpoint"""
    try:
        profilePhotoPath = profilePhotoPath.split("/")[-1]
        liveCamPhotoPath = liveCamPhotoPath.split("/")[-1]
        profilePhotoPath = os.path.join(UPLOAD_FOLDER, profilePhotoPath)
        liveCamPhotoPath = os.path.join(LIVE_CAM_FOLDER, liveCamPhotoPath)
        result = faceRecognitionModule(profilePhotoPath, liveCamPhotoPath)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Face recognition successful",
                "data": {"result": result},
            },
        )

    except HTTPException:
        raise

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
