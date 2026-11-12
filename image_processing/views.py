import cv2
import os
import tempfile
import numpy as np

from django.contrib.staticfiles import finders
from django.shortcuts import render
from django.http import HttpResponse, FileResponse



# VIEWS FOR IMAGE PROCESSING

    
# View for displaying Image Processing webpage/html
def image(request):
    return render(request, 'image.html')


    
# View for image upload and processing
def upload_image(request):

    if request.method == "POST":
        uploaded_file = request.FILES["image"]                                                          # Get uploaded file

        file_bytes = uploaded_file.read()                                                               # Convert uploaded file to NumPy array
        file_array = np.frombuffer(file_bytes, np.uint8)    

        img = cv2.imdecode(file_array, cv2.IMREAD_COLOR)                                                # Read image using OpenCV

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                                # Convert to grayscale

        success, encoded_img = cv2.imencode(".jpg", img_gray)                                           # Encode the processed image as JPEG

        if not success:
            return HttpResponse("Could not process image", status=500)

        return HttpResponse(encoded_img.tobytes(), content_type="image/jpeg")                           # Return image to browser

    return HttpResponse("POST request required",status=400)


# VIEWS FOR VIDEO PROCESSING

   
# View for displaying Video Processing webpage/html
def video(request):
    return render(request, 'videos.html')


# View for video upload and processing
def upload_video(request):

    if request.method == "POST":
        
        uploaded_video = request.FILES.get("video")                                                     # Get uploaded video

        if not uploaded_video:
            return HttpResponse("Please upload a video.", status=400)

        cascade_path = finders.find("videoapp/haarcascade_fullbody.xml")                                # Find Haar Cascade in static folder

        if not cascade_path:
            return HttpResponse("Haar Cascade XML file was not found.",status=500)

        input_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")                          # Create temporary input file

        for chunk in uploaded_video.chunks():                                                           # Save uploaded video into temporary file
            input_temp.write(chunk)

        input_temp.close()

        output_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")                          # Create temporary output file

        output_temp.close()

        cap = cv2.VideoCapture(input_temp.name)                                                         # Open uploaded video

        if not cap.isOpened():                                                                          # Check if video opened
            os.remove(input_temp.name)
            os.remove(output_temp.name)

            return HttpResponse("Could not open uploaded video.",status=500)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))                                                  # Get video properties
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        if width <= 0 or height <= 0 or fps <= 0:                                                       # Check video properties
            cap.release()

            os.remove(input_temp.name)
            os.remove(output_temp.name)

            return HttpResponse("Could not read video properties.",status=500)

        fourcc = cv2.VideoWriter_fourcc(*"avc1")                                                        # Create output video
        out = cv2.VideoWriter(output_temp.name, fourcc, fps, (width, height))

        if not out.isOpened():                                                                          # Check VideoWriter
            cap.release()

            os.remove(input_temp.name)
            os.remove(output_temp.name)

            return HttpResponse("Could not create output video.", status=500)

        person_detection = cv2.CascadeClassifier(cascade_path)                                          # Load Haar Cascade

        if person_detection.empty():                                                                    # Check Haar Cascade
            cap.release()
            out.release()

            os.remove(input_temp.name)
            os.remove(output_temp.name)

            return HttpResponse("Could not load Haar Cascade.", status=500)

        success, frame = cap.read()                                                                     # Read first frame
        frame_count = 0                                                                                 # Count processed frames

        while success:                                                                                  # Process video
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                                              # Convert frame to grayscale
            people = person_detection.detectMultiScale(gray, 1.3, 5)                                    # Detect people

            for (x, y, w, h) in people:                                                                 # Draw bounding boxes
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

            out.write(frame)                                                                            # Write processed frame
            frame_count += 1                                                                           # Read next frame
            success, frame = cap.read()

        cap.release()                                                                                   # Release OpenCV resources
        out.release()
        os.remove(input_temp.name)                                                                      # Delete temporary input file

        if not os.path.exists(output_temp.name):                                                        # Check output file
            return HttpResponse("Output video was not created.", status=500)

        output_size = os.path.getsize(output_temp.name)

        if output_size == 0:
            os.remove(output_temp.name)

            return HttpResponse("Output video is empty.", status=500)

        response = FileResponse(                                                                        # Return processed video
            open(output_temp.name, "rb"),
            content_type="video/mp4",
            as_attachment=False
        )

        return response

    return render(request, "video.html")