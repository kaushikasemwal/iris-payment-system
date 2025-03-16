import cv2

def capture_iris(image_name="iris_sample.jpg"):
    cap = cv2.VideoCapture(0)  # Open webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        cv2.imshow("Capture Iris", frame)

        # Press 's' to save image
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(f"static/iris_images/{image_name}", frame)
            print(f"✅ Iris image saved as static/iris_images/{image_name}")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_iris("iris1.jpg")  # Change filename for each capture
