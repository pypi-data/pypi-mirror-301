import cv2
import numpy as np
from tensorflow.keras.models import load_model
from cvzone.HandTrackingModule import HandDetector
import os
import pkg_resources  # Use pkg_resources to access package data

class SignLanguageRecognizer:
    def __init__(self, model_path=None,detection_confidence=0.7, tracking_confidence=0.5):
        self.detector = HandDetector(maxHands=1,
                                     detectionCon=detection_confidence,
                                     minTrackCon=tracking_confidence)

        if model_path is None:
            # Use pkg_resources to load the model from the package
            model_path = pkg_resources.resource_filename(
                __name__, 'models/signLanguageDetectoralpnum.h5')

        self.model = load_model(model_path)

        self.labels = {
            0: '1',
            1: '10',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: 'A',
            11: 'B',
            12: 'Nothing',
            13: 'C',
            14: 'D',
            15: 'E',
            16: 'F',
            17: 'G',
            18: 'H',
            19: 'I',
            20: 'J',
            21: 'K',
            22: 'L',
            23: 'M',
            24: 'N',
            25: 'O',
            26: 'P',
            27: 'Q',
            28: 'R',
            29: 'S',
            30: 'T',
            31: 'U',
            32: 'V',
            33: 'W',
            34: 'X',
            35: 'Y',
            36: 'Z',
            37: 'del',
            39: 'space'
        }

    def predict_from_image(self, image):
        """
        Predicts the ASL sign from a given image.

        Parameters:
            image (numpy.ndarray): The input image in BGR format.

        Returns:
            str: The predicted label.
            numpy.ndarray: The image with prediction label annotated.
        """
        label = self.labels.get(12, 'Nothing')  # Default to 'Nothing'

        # Find hand landmarks
        hands, img = self.detector.findHands(image)

        if hands:
            # Get the first detected hand
            hand = hands[0]

            # Extract the 21 landmarks of the hand
            landmarks = hand['lmList']  # List of 21 landmarks

            # Flatten the list of landmarks into a 1D array
            landmarks_flattened = np.array(landmarks).flatten()

            # Add batch dimension
            landmarks_input = np.expand_dims(landmarks_flattened, axis=0)

            # Predict using the model
            prediction = self.model.predict(landmarks_input, verbose=0)
            index = np.argmax(prediction)
            label = self.labels.get(index, 'Unknown')
        else:
            label = self.labels.get(12, 'Nothing')  # 'Nothing'

        # Annotate the image with the prediction
        cv2.putText(img, f'Prediction: {label}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        return label, img

    def run_webcam(self):
        """
        Runs the sign language recognizer using the webcam and displays the prediction in real-time.

        Press 'q' to quit the webcam feed.
        """
        # Initialize webcam
        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()

            if success:
                label, annotated_img = self.predict_from_image(img)

                # Display the webcam feed with prediction
                cv2.imshow('ASL Sign Language Detector', annotated_img)

            # Break loop with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the capture and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

# If this script is run directly, start the webcam recognizer
if __name__ == "__main__":
    recognizer = SignLanguageRecognizer()
    recognizer.run_webcam()
