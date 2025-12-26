import face_recognition
import cv2

def faceRecognitionModule(profilePicturePath, liveCamPicturePath):
    # Load a sample picture and learn to recognize it
    # Load a sample picture and learn to recognize it
    known_image = face_recognition.load_image_file(profilePicturePath)
    known_encodings = face_recognition.face_encodings(known_image)
    if not known_encodings:
        print("No face found in profile picture.")
        return False
    known_encoding = known_encodings[0]

    # Load an unknown image to test
    unknown_image = face_recognition.load_image_file(liveCamPicturePath)
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    if not unknown_encodings:
        print("No face found in live camera capture.")
        return False
    unknown_encoding = unknown_encodings[0]

    # Compare faces
    results = face_recognition.compare_faces([known_encoding], unknown_encoding)

    if results[0]:
        print("It's the same person!")
        return True
    else:
        print("It's a different person.")
        return False