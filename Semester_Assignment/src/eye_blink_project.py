import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import numpy as np
import logging
import time
import pygame

WIDTH = 750
HEIGHT = 500

LEFT_EYE = [33,144,145,153,154,155,157,158,159,160,161]
RIGHT_EYE = [249,263,373,374,380,381,382,381,382,384,385,386,387,388,390]

def main():
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('./Semester_Assignment/Video.mp4')
    detector = FaceMeshDetector(maxFaces=1)
    plotY_1 = LivePlot(WIDTH, HEIGHT, [100,2000], invert=True)
    plotY_2 = LivePlot(WIDTH, HEIGHT, [100,2000], invert=True)

    left_ratio = []
    left_eye_historical_data = []
    right_ratio = []
    right_eye_historical_data = []

    camera_movement_trashed = 1.4

    threshold = 0.85
    threshold2 = 0.8
    blinkCounter = 0
    counter = 0

    frameCounter = 0
    last_check_time = time.time()

    left_eye_area_data = []
    right_eye_area_data = []


    color = (255, 0, 255)

    while True:
        success, img = cap.read()

        # If it is a video and we would run out of the frames then start the video over again
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        try:
            # Create a mesh and turn off the draw
            img, faces = detector.findFaceMesh(img, draw=True)

            if faces:
                # We have only 1 face so it is 0
                faces = faces[0]
                for id in LEFT_EYE:
                    cv2.circle(img, tuple(faces[id]), 5, color, cv2.FILLED)
                for id in RIGHT_EYE:
                    cv2.circle(img, tuple(faces[id]), 5, color, cv2.FILLED)

                leftUp = faces[159]
                leftDown = faces[145]
                leftLeft = faces[130]
                leftRight = faces[243]
                # l_length_ver = detector.findDistance(leftUp, leftDown)[0]
                # l_length_hor = detector.findDistance(leftLeft, leftRight)[0]
                # l_ratio = round((l_length_ver/l_length_hor)*100, 2)

                # if len(left_ratio) > 3:
                #     left_ratio.pop(0)
                # left_ratio.append(l_ratio)

                # l_ratio_mean = sum(left_ratio)/len(left_ratio)
                # if len(left_eye_historical_data) < 6:
                #     left_eye_historical_data.append(l_ratio_mean)
                # left_eye_ratio = sum(left_eye_historical_data)/len(left_eye_historical_data)


                rightUp = faces[386]
                rightDown = faces[374]
                rightLeft = faces[382]
                rightRight = faces[263]
                # r_length_ver = detector.findDistance(rightUp, rightDown)[0]
                # r_length_hor = detector.findDistance(rightLeft, rightRight)[0]
                # r_ratio = round((r_length_ver/r_length_hor)*100, 2)

                # if len(right_ratio) > 3:
                #     right_ratio.pop(0)
                # right_ratio.append(l_ratio)

                # r_ratio_mean = sum(right_ratio)/len(right_ratio)
                # if len(right_eye_historical_data) < 6:
                #     right_eye_historical_data.append(r_ratio_mean)
                # right_eye_ratio = sum(right_eye_historical_data)/len(right_eye_historical_data)


                # if len(left_eye_historical_data) > 5 and len(right_eye_historical_data) > 5:
                #     if (left_eye_ratio * threshold) < l_ratio_mean and (right_eye_ratio * threshold) < r_ratio_mean:
                #         left_eye_historical_data.pop(0)
                #         right_eye_historical_data.pop(0)
                #         left_eye_historical_data.append(l_ratio_mean)
                #         right_eye_historical_data.append(r_ratio_mean)
                #         color = (255,0, 255)
                #         counter = 1
                #     if counter != 0:
                #         counter += 1
                #         if counter > 2:
                #             blinkCounter += 1
                #             color = (0,200,0)
                #             counter = 0


                left_eye_area = LeftEyeArea(faces)
                if len(left_eye_area_data) != 5:
                    left_eye_area_data.append(left_eye_area)
                left_eye_closed = sum(left_eye_area_data)/len(left_eye_area_data)
                left_eye_threshold = left_eye_closed * threshold2


                right_eye_area = RightEyeArea(faces)
                if len(right_eye_area_data) != 5:
                    right_eye_area_data.append(right_eye_area)
                right_eye_closed = sum(right_eye_area_data)/len(right_eye_area_data)
                right_eye_threshold = right_eye_closed * threshold2


                eye_blink = left_eye_threshold < left_eye_area and right_eye_threshold < right_eye_area
                if len(left_eye_area_data) == 5 and len(right_eye_area_data) == 5:
                    if left_eye_closed > left_eye_area * camera_movement_trashed and right_eye_closed > right_eye_area * camera_movement_trashed:
                        # logging.info(f'camera movement detected {left_eye_closed} < {left_eye_area} and {right_eye_closed} < {right_eye_area}')
                        if len(left_eye_area_data) == 5:
                            left_eye_area_data.pop(0)
                        if len(right_eye_area_data) == 5:
                            right_eye_area_data.pop(0)
                    elif eye_blink:
                        left_eye_area_data.pop(0)
                        right_eye_area_data.pop(0)
                        left_eye_area_data.append(left_eye_area)
                        right_eye_area_data.append(right_eye_area)
                        color = (255,0, 255)
                        counter = 1
                    if counter != 0:
                        counter += 1
                        if counter > 2:
                            blinkCounter += 1
                            color = (0,200,0)
                            counter = 0

                current_time = time.time()
                if current_time - last_check_time >= 60:
                    check_blink_counter(0)
                    last_check_time = current_time


                cvzone.putTextRect(img, f'Blinks: {blinkCounter}', [20, 50], 3, 2, offset=20, border=1, colorR=color)
                # Draw a line between the 2 points (on each side)
                cv2.line(img, leftUp, leftDown, color, 3)
                cv2.line(img, leftLeft, leftRight, color, 3)
                cv2.line(img, rightUp, rightDown, color, 3)
                cv2.line(img, rightLeft, rightRight, color, 3)

                # We want to plot a graph of the l_ratio changes on a new window
                l_imagePlot = plotY_1.update(left_eye_area, color)
                r_imagePlot = plotY_2.update(right_eye_area, color)
                img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
                imageStack = cvzone.stackImages([img, l_imagePlot, r_imagePlot], 3, 1)

                frameCounter += 1
                logging.info(f'frame: {frameCounter}, left_eye_area: {left_eye_area}, right_eye_area: {right_eye_area}, left_eye_closed: {left_eye_closed}, right_eye_closed: {right_eye_closed}, left_eye_threshold: {left_eye_threshold}, right_eye_threshold: {right_eye_threshold}, blinkCounter: {blinkCounter}')

            else:
                img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
                imageStack = cvzone.stackImages([img], 3, 1)

            # Resize the display window
            cv2.imshow("Image", imageStack)
            cv2.waitKey(25)

        except Exception as e:
            logging.exception(f'Exception occurred: {e}')
            exit(1)


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


def check_blink_counter(blink_counter):
    if blink_counter < 12:
        pygame.mixer.init()
        pygame.mixer.music.load("./sounds/alarm.mp3")
        pygame.mixer.music.play()


if __name__=="__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="./logs/logs_plot2.log"
    )
    main()