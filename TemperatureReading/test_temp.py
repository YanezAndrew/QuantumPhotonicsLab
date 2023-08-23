import cv2
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open the default camera (index 0)
cap = cv2.VideoCapture(0)

# Check if the camera was opened successfully
if not cap.isOpened():
    print("Error opening camera")
    exit()

# Define the set of known symbols you want to extract
known_symbols = set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

while True:
    ret, frame = cap.read()  # Read a frame from the camera

    if not ret:
        print("Error reading frame")
        break  # Break the loop if an error occurs

    cv2.imshow('Live Video', frame)  # Display the frame

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break  # Exit the loop if 'q' key is pressed
    elif key == ord('s'):
        # Save the current frame as an image
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured!")

        # Read the captured image
        img = cv2.imread("captured_image.jpg")

        # Apply OCR on the image and extract only known symbols
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # A text file is created and flushed
        file = open("recognized.txt", "w+")
        file.write("")
        file.close()

        # Looping through the identified contours
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cropped = img[y:y + h, x:x + w]
            print(cnt)
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped, config='--psm 6 -c tessedit_char_whitelist=' + ''.join(known_symbols))
            print(text)
            # Open the file in append mode
            file = open("recognized.txt", "a")

            # Appending the text into the file
            file.write(text)
            file.write("\n")

            # Close the file
            file.close()

        print("Text extraction complete!")
        break

# Release the camera
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
