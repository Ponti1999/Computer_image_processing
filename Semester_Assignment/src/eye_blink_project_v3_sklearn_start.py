import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import numpy as np
from sklearn.linear_model import SGDClassifier

WIDTH = 750
HEIGHT = 500

LEFT_EYE = [33, 144, 145, 153, 154, 155, 157, 158, 159, 160, 161]
RIGHT_EYE = [249, 263, 373, 374, 380, 381, 382, 381, 382, 384, 385, 386, 387, 388, 390]

def main():
    cap = cv2.VideoCapture(0)
    detector = FaceMeshDetector(maxFaces=1)
    plotY_1 = LivePlot(WIDTH, HEIGHT, [18, 38], invert=True)
    plotY_2 = LivePlot(WIDTH, HEIGHT, [18, 42], invert=True)

    left_ratio = []
    left_eye_historical_data = []
    right_ratio = []
    right_eye_historical_data = []

    threshold = 0.85
    threshold2 = 0.8
    blinkCounter = 0
    counter = 0

    left_eye_area_data = []
    right_eye_area_data = []

    color = (255, 0, 255)

    # Create the SGDClassifier for online training
    model = SGDClassifier()

    while True:
        success, img = cap.read()

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        try:
            img, faces = detector.findFaceMesh(img, draw=True)

            if faces:
                faces = faces[0]

                # Calculate left eye ratio
                leftUp = faces[159]
                leftDown = faces[145]
                leftLeft = faces[130]
                leftRight = faces[243]
                l_length_ver = detector.findDistance(leftUp, leftDown)[0]
                l_length_hor = detector.findDistance(leftLeft, leftRight)[0]
                l_ratio = round((l_length_ver / l_length_hor) * 100, 2)

                if len(left_ratio) > 3:
                    left_ratio.pop(0)
                left_ratio.append(l_ratio)

                l_ratio_mean = sum(left_ratio) / len(left_ratio)
                if len(left_eye_historical_data) < 6:
                    left_eye_historical_data.append(l_ratio_mean)
                left_eye_ratio = sum(left_eye_historical_data) / len(left_eye_historical_data)

                # Calculate right eye ratio
                rightUp = faces[386]
                rightDown = faces[374]
                rightLeft = faces[382]
                rightRight = faces[263]
                r_length_ver = detector.findDistance(rightUp, rightDown)[0]
                r_length_hor = detector.findDistance(rightLeft, rightRight)[0]
                r_ratio = round((r_length_ver / r_length_hor) * 100, 2)

                if len(right_ratio) > 3:
                    right_ratio.pop(0)
                right_ratio.append(l_ratio)

                r_ratio_mean = sum(right_ratio) / len(right_ratio)
                if len(right_eye_historical_data) < 6:
                    right_eye_historical_data.append(r_ratio_mean)
                right_eye_ratio = sum(right_eye_historical_data) / len(right_eye_historical_data)

                # Collect eye area data for training
                left_eye_area = LeftEyeArea(faces)
                right_eye_area = RightEyeArea(faces)

                left_eye_area_data.append(left_eye_area)
                right_eye_area_data.append(right_eye_area)

                # Train the model with the collected eye area data and labels
                if len(left_eye_area_data) >= 5:
                    X_train = np.array(left_eye_area_data + right_eye_area_data).reshape(-1, 1)
                    y_train = np.array([0] * len(left_eye_area_data) + [1] * len(right_eye_area_data))
                    model.partial_fit(X_train, y_train, classes=[0, 1])

                # Predict the eye state based on the current eye area
                X_pred = np.array([[left_eye_area], [right_eye_area]])
                eye_state = model.predict(X_pred)

                if eye_state[0] == 1 and eye_state[1] == 1:
                    # Both eyes closed
                    color = (0, 200, 0)
                    counter += 1
                    if counter > 2:
                        blinkCounter += 1
                        counter = 0
                else:
                    # Eyes open or one eye closed
                    color = (255, 0, 255)
                    counter = 0

                cvzone.putTextRect(img, f'Blinks: {blinkCounter}', [20, 50], 3, 2, offset=20, border=1, colorR=color)

                # Draw lines between the eye points
                for id in LEFT_EYE:
                    cv2.circle(img, tuple(faces[id]), 5, color, cv2.FILLED)
                for id in RIGHT_EYE:
                    cv2.circle(img, tuple(faces[id]), 5, color, cv2.FILLED)
                cv2.line(img, leftUp, leftDown, color, 3)
                cv2.line(img, leftLeft, leftRight, color, 3)
                cv2.line(img, rightUp, rightDown, color, 3)
                cv2.line(img, rightLeft, rightRight, color, 3)

                # Update the plots
                l_imagePlot = plotY_1.update(l_ratio_mean, color)
                r_imagePlot = plotY_2.update(r_ratio, color)
                img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
                imageStack = cvzone.stackImages([img, l_imagePlot, r_imagePlot], 3, 1)
            else:
                img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
                imageStack = cvzone.stackImages([img], 3, 1)

            cv2.imshow("Image", imageStack)
            cv2.waitKey(1)
        except:
            print("No face detected")


def LeftEyeArea(faces):
    left_eye_points = [faces[id] for id in LEFT_EYE]
    left_eye_points = np.array(left_eye_points)
    left_eye_points_area = cv2.contourArea(left_eye_points)

    return left_eye_points_area


def RightEyeArea(faces):
    right_eye_points = [faces[id] for id in RIGHT_EYE]
    right_eye_points = np.array(right_eye_points)
    right_eye_points_area = cv2.contourArea(right_eye_points)

    return right_eye_points_area


if __name__ == "__main__":
    main()
