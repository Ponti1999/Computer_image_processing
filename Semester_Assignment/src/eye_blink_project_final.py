import numpy as np
import time
import argparse
import logging
import json
from help.search_json import search_item_in_users, get_level_length, create_search_conditions, list_users_values
from help.write_json import write_json
import pygame
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

CONFIG_PATH = "../config/config.json"

WIDTH = 750
HEIGHT = 500

LEFT_EYE = [33,144,145,153,154,155,157,158,159,160,161]
RIGHT_EYE = [249,263,373,374,380,381,382,381,382,384,385,386,387,388,390]

def setup(o_threshold:float, o_camera_movement_trashed:float, o_blink_alert:int, o_color:tuple):

    threshold = o_threshold
    camera_movement_trashed = o_camera_movement_trashed
    blink_alert = o_blink_alert
    color = o_color

    return threshold, camera_movement_trashed, blink_alert, color



def start(developer_mode:bool=False, results:dict=None):
    print(f'Successfully started the app!')
    # Here we can set the source of the video. Webcam / mp4 file.
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('./Semester_Assignment/Video.mp4')

    detector = FaceMeshDetector(maxFaces=1)

    plotY_1 = LivePlot(WIDTH, HEIGHT, [100,2000], invert=True)
    plotY_2 = LivePlot(WIDTH, HEIGHT, [100,2000], invert=True)

    imageStack = None

    counter = 0
    blinkCounter = 0
    frameCounter = 0
    errorCounter = 0
    left_eye_area_data = []
    right_eye_area_data = []
    last_check_time = time.time()
    # These are the variables we use to calculate the blinks
    threshold, camera_movement_trashed, blink_alert, color = setup(results['threshold'], results['camera_movement_trashed'], results['blink_alert'], results['color'])

    while True:
        success, img = cap.read()

        # If it is a video and we would run out of the frames then start the video over again
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        try:
            # Create a mesh and turn it on in the developer mode
            img, faces = detector.findFaceMesh(img, draw=developer_mode)

            if faces:
                # We have only 1 face so it is 0
                faces = faces[0]
                # We want to get the left and right eye circles on the display
                if developer_mode:
                    for id in LEFT_EYE:
                        cv2.circle(img, tuple(faces[id]), 5, color, cv2.FILLED)
                    for id in RIGHT_EYE:
                        cv2.circle(img, tuple(faces[id]), 5, color, cv2.FILLED)

                left_eye_area = LeftEyeArea(faces)
                if len(left_eye_area_data) != 5:
                    left_eye_area_data.append(left_eye_area)
                left_eye_closed = sum(left_eye_area_data)/len(left_eye_area_data)
                left_eye_threshold = left_eye_closed * threshold


                right_eye_area = RightEyeArea(faces)
                if len(right_eye_area_data) != 5:
                    right_eye_area_data.append(right_eye_area)
                right_eye_closed = sum(right_eye_area_data)/len(right_eye_area_data)
                right_eye_threshold = right_eye_closed * threshold


                eye_blink = left_eye_threshold < left_eye_area and right_eye_threshold < right_eye_area
                if len(left_eye_area_data) == 5 and len(right_eye_area_data) == 5:
                    if left_eye_closed > left_eye_area * camera_movement_trashed and right_eye_closed > right_eye_area * camera_movement_trashed:
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

                # We want to display the number of blinks on the screen
                cvzone.putTextRect(img, f'Blinks: {blinkCounter}', [20, 50], 3, 2, offset=20, border=1, colorR=color)

                if developer_mode:
                    # We want to plot a graph of the l_ratio changes on a new window
                    l_imagePlot = plotY_1.update(left_eye_area, color)
                    r_imagePlot = plotY_2.update(right_eye_area, color)
                    img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
                    imageStack = cvzone.stackImages([img, l_imagePlot, r_imagePlot], 3, 1)

                frameCounter += 1
                logging.info(f'frame: {frameCounter}, left_eye_area: {left_eye_area}, right_eye_area: {right_eye_area}, left_eye_closed: {left_eye_closed}, right_eye_closed: {right_eye_closed}, left_eye_threshold: {left_eye_threshold}, right_eye_threshold: {right_eye_threshold}, blinkCounter: {blinkCounter}')

            else:
                if developer_mode:
                    img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
                    imageStack = cvzone.stackImages([img], 3, 1)

            if developer_mode:
                # Resize the display window
                cv2.imshow("Image", imageStack)
                cv2.waitKey(25)

        except Exception as e:
            if errorCounter > 4:
                logging.error(f'The system had 5 error, the system will shut down')
                exit(0)
            logging.exception(f'Exception occurred: {e}')
            logging.exception(f'The system will restart in 2.5 seconds')
            time.sleep(2.5)
            errorCounter += 1
            start(developer_mode)


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


def parse_color(value):
    try:
        r, g, b = value.split(',')
        r, g, b = int(r.strip()), int(g.strip()), int(b.strip())
        return (r, g, b)
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid color format. Expected format: 'r, g, b'")


def user_setup_load(verbose_bool:bool=False, user_str:str=None):
    profiles, values = list_users_values(path=CONFIG_PATH, user=user_str, verbose=verbose_bool)
    if values is None:
        print(f'Currently available profiles:')
        for key in profiles:
            print(key)
    else:
        try:
            start(developer_mode=verbose_bool, results=values)
        except Exception as e:
            raise argparse.ArgumentTypeError(f'Exception occurred: {e}')


def menu():
    parser = argparse.ArgumentParser(description='Fatigue monitoring app based on eye blink detection')
    subparsers = parser.add_subparsers(dest='mode', help='Mode of the app')

    developer_parser = subparsers.add_parser('developer', help='Developer mode')
    developer_parser.add_argument('-t', '--threshold', type=float, help='Threshold for the eye area')
    developer_parser.add_argument('-m', '--camera_movement_trashed', type=float, help='Threshold for the camera movement')
    developer_parser.add_argument('-b', '--blink_alert', type=int, help='Threshold for the blink alert')
    developer_parser.add_argument('-c', '--color', type=parse_color, help='Threshold for the color')
    developer_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    developer_parser.add_argument('-s', '--set', type=str, help='Set the user profile')


    userparser = subparsers.add_parser('user', help='User mode')
    userparser.add_argument('-s', '--set', type=str, help='Set the user profile')

    args = parser.parse_args()

    if args.mode == 'developer':
        exception = ["mode", "verbose"]
        num_developer_args = sum(arg is not None for arg in [args.threshold, args.camera_movement_trashed, args.blink_alert, args.color])
        results = search_item_in_users(CONFIG_PATH, create_search_conditions(args, exception))
        max_length, values = get_level_length(CONFIG_PATH)
        if len(results) != max_length:
            if num_developer_args == 4:
                write_json(path=CONFIG_PATH, verbose=args.verbose, values=create_search_conditions(args, exception))
                results = search_item_in_users(CONFIG_PATH, create_search_conditions(args, exception))
                start(developer_mode=args.verbose, results=results)
            else:
                if args.verbose:
                    print('One element is missing from the call. It will load the default values. If you want to change to other profile please use the -l -s flags.')
                user_setup_load(verbose_bool=args.verbose, user_str=args.set)
        else:
            start(developer_mode=args.verbose, results=results)

    elif args.mode == 'user':
        user_setup_load(user_str=args.set)


if __name__=="__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="../logs/logs_plot3.log"
    )
    menu()
