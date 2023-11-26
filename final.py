import cv2
from PIL import Image
import webbrowser
from googleapiclient.discovery import build
import tkinter as tk
from tkinter import simpledialog

def take_picture(output_path="captured_image.jpg", camera_index=0):
    # Open the video capture
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Save the captured frame as an image
    if ret:
        cv2.imwrite(output_path, frame)
        print(f"Picture taken and saved as {output_path}")
    else:
        print("Error: Unable to capture picture.")

    # Release the camera
    cap.release()

def process_image(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)

        # Display some information about the original image
        print(f"Original Image Format: {img.format}")
        print(f"Original Image Mode: {img.mode}")
        print(f"Original Image Size: {img.size}")

        # Perform various operations on the image here
        # For example, resize the image
        resized_img = img.resize((500, 400))

        # Save the processed image to a new file
        resized_img.save("resized_image.jpg")

        # Display the processed image
        resized_img.show()

        print("Image processing completed.")
    except Exception as e:
        print(f"Error processing image: {e}")

def search_and_open_youtube(query, max_results=3):
    API_KEY = 'AIzaSyCHfAcqhUwZDHRNWM_hBmmcNyuwZKcM_Mw'
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    request = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        order='viewCount',
        maxResults=max_results,
    )
    response = request.execute()

    # Display the list of videos with numbers
    for i, item in enumerate(response['items'], 1):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        views = youtube.videos().list(part='statistics', id=video_id).execute()['items'][0]['statistics']['viewCount']

        # Construct the video URL
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        print(f"{i}. Video: {title}\n   Views: {views}\n   URL: {video_url}")

    # Ask the user to input their choice
    choice = input("Enter the number of the video you want to open: ")

    # Validate the user's input
    try:
        choice = int(choice)
        if 1 <= choice <= len(response['items']):
            chosen_video = response['items'][choice - 1]
            chosen_video_id = chosen_video['id']['videoId']
            chosen_video_url = f'https://www.youtube.com/watch?v={chosen_video_id}'

            # Open the chosen video URL in the default web browser
            webbrowser.open(chosen_video_url)

        else:
            print("Invalid choice. Please enter a valid number.")

    except ValueError:
        print("Invalid input. Please enter a number.")

def show_feedback(rating):
    # Add the logic for displaying feedback here...
    print(f"Thank you for your rating! You gave a rating of {rating} out of 5.")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to choose between boat and plane models
    user_choice = simpledialog.askstring("Input", "Enter '1' for origami boat model or '2' for origami plane model:")

    if user_choice == '1':
        # Take a picture of a boat
        take_picture(output_path="boat_image.jpg")
        # Process the captured image
        process_image("boat_image.jpg")
        # Search and open YouTube for origami boat model
        search_and_open_youtube(query='origami boat model', max_results=3)

    elif user_choice == '2':
        # Take a picture of a plane
        take_picture(output_path="plane_image.jpg")
        # Process the captured image
        process_image("plane_image.jpg")
        # Search and open YouTube for origami plane model
        search_and_open_youtube(query='origami plane model', max_results=3)

    else:
        print("Invalid choice. Please enter either '1' or '2.")

    # Ask the user to provide a rating out of 5
    rating = simpledialog.askfloat("Rating", "Please provide a rating out of 5:")

    # Validate the user's input
    if 0 <= rating <= 5:
        # Set a delay of 10000 milliseconds (10 seconds) before showing feedback
        root.after(10000, show_feedback, rating)
    else:
        print("Invalid rating. Please enter a number between 0 and 5.")

    root.mainloop()

if __name__ == "__main__":
    main()
