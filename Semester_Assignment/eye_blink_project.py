import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import argparse

Width = 640
Height = 400

cap = cv2.VideoCapture('./Semester_Assignment/Video.mp4')

# We set it to detect only one face
detector = FaceMeshDetector(maxFaces=1)

plotY = LivePlot(Width, Height, [25,50], invert=True)

idList = [22,23,24,26,110,157,158,159,160,161,130,243]

ratioList = []

blinkCounter = 0

counter = 0

colorPurple = (255, 0, 255)
colorGreen = (0, 255, 0)
colorBlack = (0, 0, 0)

while True:
    success, img = cap.read()

    # If it is a video and we would run out of the frames then start the video over again
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Create a mesh and turn off the draw
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        # We have only 1 face so it is 0
        faces = faces[0]
        for id in idList:
            cv2.circle(img, tuple(faces[id]), 5, colorGreen, cv2.FILLED)

        # We want to measure the distance between the eyes (closing the eyes)
        # but it will not be enough because if we move closer to the camera the distance will change
        leftUp = faces[159]
        leftDown = faces[23]

        leftLeft = faces[130]
        leftRight = faces[243]
        # We can add the img parameter to draw the line on the image (print will give back the img mash points too)
        # and in the method documentation there is an error, there is no draw parameter!
        lengthVer = detector.findDistance(leftUp, leftDown)[0]

        # We are checking the horizontal distance between the eyes (for ratio calculation against the movement problem)
        lengthHor = detector.findDistance(leftLeft, leftRight)[0]

        ratio = round((lengthVer/lengthHor)*100, 2)
        # print(f'lenghtVer: {lengthVer}')
        # print(f'lenghtHor: {lengthHor}')
        print(f'ratio: {ratio}')

        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioList.append(ratio)

        ratioMean = sum(ratioList)/len(ratioList)

        color = colorPurple
        if ratioMean < 37 and counter == 0:
            blinkCounter += 1
            color = colorGreen
            counter = 1
        if counter != 0:
            counter += 1
            if counter == 10:
                color = colorBlack
                counter = 0

        cvzone.putTextRect(img, f'Blinks: {blinkCounter}', [20, 50], 3, 2, offset=20, border=1, colorR=colorPurple, colorB=colorBlack)
        # Draw a line between the 2 points
        cv2.line(img, leftUp, leftDown, color, 3)
        cv2.line(img, leftLeft, leftRight, color, 3)

        # We want to plot a graph of the ratio changes on a new window
        imagePlot = plotY.update(ratioMean, color=colorGreen)
        img = cv2.resize(img, (Width, Height), interpolation=cv2.INTER_AREA)
        imageStack = cvzone.stackImages([img, imagePlot], 2, 1)

    else:
        img = cv2.resize(img, (Width, Height), interpolation=cv2.INTER_AREA)
        imageStack = cvzone.stackImages([img], 2, 1)







    # Resize the display window
    cv2.imshow("Image", imageStack)
    cv2.waitKey(25)
