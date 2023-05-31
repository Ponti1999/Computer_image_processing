import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk
import time

MIN_WINDOW_WIDTH = 1100
MAIN_WINDOW_HIGH = 600
WIDTH = 650
HEIGHT = 450

LEFT_EYE = [33,144,145,153,154,155,157,158,159,160,161]
RIGHT_EYE = [249,263,373,374,380,381,382,381,382,384,385,386,387,388,390]

class EyeBlinkDetectionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.detector = FaceMeshDetector(maxFaces=1)
        self.plotY_1 = LivePlot(WIDTH // 2, HEIGHT // 2, [18, 38], invert=True)
        self.plotY_2 = LivePlot(WIDTH // 2, HEIGHT // 2, [18, 42], invert=True)

        self.left_ratio = []
        self.left_eye_historical_data = []
        self.right_ratio = []
        self.right_eye_historical_data = []

        self.threshold = 0.9
        self.blinkCounter = 0
        self.counter = 0

        self.color = (255, 0, 255)

        self.window = ctk.CTk()

        self.window.geometry(f"{MIN_WINDOW_WIDTH}x{MAIN_WINDOW_HIGH}")
        self.window.title("Eye Blink Detection")

         # Configure grid columns
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        self.left_sidebar_frame = ctk.CTkFrame(self.window, width=WIDTH//4, height=MAIN_WINDOW_HIGH)
        self.left_sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.left_sidebar_frame.grid_rowconfigure(4, weight=1)

        self.face_mesh_checkbox = ctk.CTkCheckBox(self.left_sidebar_frame, text="Face Mesh")
        self.face_mesh_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.eye_highlight_checkbox = ctk.CTkCheckBox(self.left_sidebar_frame, text="Eyes highlight")
        self.eye_highlight_checkbox.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.plotY1_checkbox = ctk.CTkCheckBox(self.left_sidebar_frame, text="Plot Right Eye Values")
        self.plotY1_checkbox.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.plotY2_checkbox = ctk.CTkCheckBox(self.left_sidebar_frame, text="Plot Left Eye Values")
        self.plotY2_checkbox.grid(row=3, column=0, sticky="w", padx=10, pady=10)


        self.main_display = ctk.CTkLabel(self.window, width=WIDTH, height=HEIGHT, text='')
        self.main_display.grid(row=0, column=1, sticky="nsew")


        self.right_sidebar_frame = ctk.CTkFrame(self.window, width=WIDTH//4, height=MAIN_WINDOW_HIGH)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")

        self.right_eye_plot_display = ctk.CTkLabel(self.right_sidebar_frame, width=WIDTH//2, height=HEIGHT//2, text='')
        self.right_eye_plot_display.grid(row=0, column=0, sticky="nsew")
        self.left_eye_plot_display = ctk.CTkLabel(self.right_sidebar_frame, width=WIDTH//2, height=HEIGHT//2, text='')
        self.left_eye_plot_display.grid(row=1, column=0, sticky="nsew")

    def start(self):
        self.update()

    def update(self):
        success, img = self.cap.read()

        if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        try:
            img, faces = self.detector.findFaceMesh(img, draw=True)
            self.display_image(img)

            if faces:
                faces = faces[0]
                if self.eye_highlight_checkbox.get():
                    self.toggle_eye_highlight(img, faces)

                l_ratio, r_ratio = self.calculate_eye_ratios(faces)

                if self.plotY1_checkbox.get():
                    self.display_plot(self.plotY_1.update(l_ratio, self.color), True, False)
                if self.plotY2_checkbox.get():
                    self.display_plot(self.plotY_2.update(r_ratio, self.color), False, True)
            self.window.update()
        except:
            print("No face detected")

        self.window.after(1, self.update)

    def calculate_eye_ratios(self, faces):
        leftUp = faces[159]
        leftDown = faces[145]
        leftLeft = faces[130]
        leftRight = faces[243]

        rightUp = faces[386]
        rightDown = faces[374]
        rightLeft = faces[382]
        rightRight = faces[263]

        l_length_ver = self.detector.findDistance(leftUp, leftDown)[0]
        l_length_hor = self.detector.findDistance(leftLeft, leftRight)[0]

        r_length_ver = self.detector.findDistance(rightUp, rightDown)[0]
        r_length_hor = self.detector.findDistance(rightLeft, rightRight)[0]

        l_ratio = round((l_length_ver / l_length_hor) * 100, 2)
        r_ratio = round((r_length_ver / r_length_hor) * 100, 2)

        if len(self.left_ratio) > 3:
            self.left_ratio.pop(0)
        self.left_ratio.append(l_ratio)

        if len(self.right_ratio) > 3:
            self.right_ratio.pop(0)
        self.right_ratio.append(r_ratio)

        l_ratio_mean = sum(self.left_ratio) / len(self.left_ratio)
        r_ratio_mean = sum(self.right_ratio) / len(self.right_ratio)

        if len(self.left_eye_historical_data) < 6:
            self.left_eye_historical_data.append(l_ratio_mean)
        if len(self.right_eye_historical_data) < 6:
            self.right_eye_historical_data.append(r_ratio_mean)

        left_eye_ratio = sum(self.left_eye_historical_data) / len(self.left_eye_historical_data)
        right_eye_ratio = sum(self.right_eye_historical_data) / len(self.right_eye_historical_data)

        if len(self.left_eye_historical_data) > 5 and len(self.right_eye_historical_data) > 5:
            if (left_eye_ratio * self.threshold) < l_ratio_mean and (right_eye_ratio * self.threshold) < r_ratio_mean:
                self.left_eye_historical_data.pop(0)
                self.right_eye_historical_data.pop(0)
                self.left_eye_historical_data.append(l_ratio_mean)
                self.right_eye_historical_data.append(r_ratio_mean)
                self.color = (255, 0, 255)
                self.counter = 1
            if self.counter != 0:
                self.counter += 1
                if self.counter > 2:
                    self.blinkCounter += 1
                    self.color = (0, 200, 0)
                    self.counter = 0

        return l_ratio_mean, r_ratio_mean


    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (WIDTH, HEIGHT))
        img = Image.fromarray(img)
        self.photo_image = ImageTk.PhotoImage(image=img)
        self.main_display.configure(image=self.photo_image)


    def display_plot(self, img, lef, right):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (WIDTH // 2, HEIGHT // 2))
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        if right:
            self.right_eye_plot_display.configure(image=img)
        if lef:
            self.left_eye_plot_display.configure(image=img)

    def toggle_face_mesh(self):
        if self.face_mesh_checkbox.get():
            # Checkbox is checked
            print("Face Mesh enabled")
        else:
            # Checkbox is unchecked
            print("Face Mesh disabled")

    def toggle_plotY1(self):
        if self.plotY1_checkbox.get():
            # Checkbox is checked
            print("toggle_plotY1")
        else:
            # Checkbox is unchecked
            print("no toggle_plotY1")

    def toggle_plotY2(self):
        if self.plotY2_checkbox.get():
            # Checkbox is checked
            print("toggle_plotY2")
        else:
            # Checkbox is unchecked
            print("no toggle_plotY2")

    def toggle_eye_highlight(self, img, faces):
        for id in LEFT_EYE:
            cv2.circle(img, tuple(faces[id]), 5, self.color, cv2.FILLED)
        for id in RIGHT_EYE:
            cv2.circle(img, tuple(faces[id]), 5, self.color, cv2.FILLED)

if __name__=="__main__":
    app = EyeBlinkDetectionApp()
    app.start()
    app.window.mainloop()

    # app.mainloop()