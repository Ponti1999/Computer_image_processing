import tkinter
import customtkinter
from skimage import io, img_as_ubyte, img_as_float, restoration
from skimage.filters import roberts, gaussian, median, sobel, unsharp_mask
from skimage.feature import canny
from matplotlib import pyplot as plt
from PIL import ImageTk, Image
import os
import numpy as np
import psutil
import time

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

PATH = 'Photoshop/img/'
WINDOW_WIDTH = 1100
WINDOW_HIGH = 580
IMAGE_LOAD_DIVIDER = 1.5
GAUSSIAN_FILTERED_SIGMA = 5
MEDIAN_FILTERED_SIZE = 5

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HIGH}")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Left sidebar
        self.left_sidebar_frame = customtkinter.CTkFrame(master=self, width=250, height=WINDOW_HIGH)
        self.left_sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.left_sidebar_frame.grid_rowconfigure(4, weight=1)

        # Instruction label
        # self.instruction_label = customtkinter.CTkLabel(self.left_sidebar_frame, text="Select The Image", font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.instruction_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Dropdown menu
        self.image_choice = customtkinter.CTkComboBox(self.left_sidebar_frame, values=FILES_IMAGES)
        self.image_choice.grid(row=0, column=0, padx=20, pady=10)
        # Entry for picture size
        self.image_entry_width = customtkinter.CTkLabel(self.left_sidebar_frame, text="Image width: ")
        self.image_entry_width.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.image_entry_x = customtkinter.CTkEntry(self.left_sidebar_frame, width=75)
        self.image_entry_x.grid(row=1, column=0, padx=10, sticky="e")
        self.image_entry_height = customtkinter.CTkLabel(self.left_sidebar_frame, text="Image height: ")
        self.image_entry_height.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.image_entry_y = customtkinter.CTkEntry(self.left_sidebar_frame, width=75)
        self.image_entry_y.grid(row=2, column=0, padx=10, sticky="e")
        # Button for importing the image
        self.load_image = customtkinter.CTkButton(self.left_sidebar_frame, text="Load image" ,command=self.display_image_function)
        self.load_image.grid(row=3, column=0, padx=10)

        # Main frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_display = customtkinter.CTkLabel(self.main_frame, width=700, height=450, text='')
        self.main_display.grid(row=0, column=1, sticky="nsew")

        self.main_display_label = customtkinter.CTkLabel(self, text="Run time: ")
        self.main_display_label.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
        self.main_display_run_label = customtkinter.CTkLabel(self, text="")
        self.main_display_run_label.grid(row=1, column=1, padx=100, pady=5, sticky="nw")


        self.main_display_label = customtkinter.CTkLabel(self, text="Memory usage: ")
        self.main_display_label.grid(row=2, column=1, padx=5, pady=5, sticky="nw")
        self.main_display_momory_label = customtkinter.CTkLabel(self, text="")
        self.main_display_momory_label.grid(row=2, column=1, padx=100, pady=5, sticky="nw")



        # Right sidebar
        self.right_sidebar_frame = customtkinter.CTkFrame(master=self, width=200, height=WINDOW_HIGH)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=3, sticky="nsew")
        self.right_sidebar_frame.grid_rowconfigure(10, weight=1)

        self.right_button_0 = customtkinter.CTkButton(self.right_sidebar_frame, text="Negate" ,command=self.monitor_performance(self.negate_filter))
        self.right_button_0.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_1 = customtkinter.CTkButton(self.right_sidebar_frame, text="Gamma correction" ,command=self.monitor_performance(self.gamma_correction_filter))
        self.right_button_1.grid(row=1, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_2 = customtkinter.CTkButton(self.right_sidebar_frame, text="Logarithmic correction" ,command=self.monitor_performance(self.log_transformation_filter))
        self.right_button_2.grid(row=2, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_3 = customtkinter.CTkButton(self.right_sidebar_frame, text="Gray transformation" ,command=self.monitor_performance(self.gray_filter))
        self.right_button_3.grid(row=3, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_4 = customtkinter.CTkButton(self.right_sidebar_frame, text="Histogram create" ,command=self.monitor_performance(self.histogram_maker))
        self.right_button_4.grid(row=4, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_5 = customtkinter.CTkButton(self.right_sidebar_frame, text="Histogram Equalization" ,command=self.monitor_performance(self.histogram_equalization))
        self.right_button_5.grid(row=5, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_6 = customtkinter.CTkButton(self.right_sidebar_frame, text="      " )
        self.right_button_6.grid(row=6, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_label = customtkinter.CTkLabel(self.right_sidebar_frame, text="Value: ")
        self.right_label.grid(row=9, column=2, padx=10, pady=10, sticky="w")
        self.right_entry = customtkinter.CTkEntry(self.right_sidebar_frame, width=75)
        self.right_entry.grid(row=9, column=2, padx=10, sticky="e")



    def display_image_function(self, *args):
        try:
            if args:
                self.image_open = Image.open(*args)
                self.image_choice.configure(values=os.listdir(PATH))
            else:
                self.image_file = self.image_choice.get()
                self.image_open = Image.open(PATH + self.image_file)
            if self.image_entry_x.get() == "" or self.image_entry_y.get() == "":
                self.image_entry_x.insert(0, self.image_open.size[0]/IMAGE_LOAD_DIVIDER)
                self.image_entry_y.insert(0, self.image_open.size[1]/IMAGE_LOAD_DIVIDER)
            self.image_resized = self.image_open.resize((int(float(self.image_entry_x.get())), int(float(self.image_entry_y.get()))), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(self.image_resized)
            self.main_display.configure(anchor="center", image=self.image)
            # self.delete_image_size()
        except Exception as e:
            print(e)

    def delete_image_size(self):
        self.image_entry_x.delete(0, customtkinter.END)
        self.image_entry_y.delete(0, customtkinter.END)


    def negate_filter(self):
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.negate_filter = 255 - self.img

        fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor='none')
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.2)
        axes[0].imshow(self.img)
        axes[1].imshow(self.gamma_corrected, cmap='gray')
        axes[0].axis('off')
        axes[1].axis('off')
        axes[0].set_title('')
        axes[1].set_title('')
        self.image_file_name = self.image_choice.get().split('.')[0]
        self.image_path = ''.join([PATH, self.image_file_name,'_negate.png'])
        plt.savefig(self.image_path)

        self.plot_image(self.negate_filter, image_name='_'.join([self.image_file_name,'negate_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_negate_only.png']))


    def gamma_correction_filter(self):
        ## First, we normalize the pixel value by dividing it with the maximum pixel value, i.e., x / 255.0.
        ## Then, we raise this normalized pixel value to the power of the gamma value.
        ## Finally, we scale the gamma-corrected value back to the 8-bit range by multiplying with the maximum pixel value,
        ## Since we are using 8-bit images, the maximum pixel value is 255. We need to round the the gamma-corrected pixel value to the nearest integer.
        self.gamma = 0.5
        if self.right_entry.get():
            self.gamma = float(self.right_entry.get())
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.gamma_corrected = (self.img / 255) ** self.gamma * 255

        fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor='none')
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.2)
        axes[0].imshow(self.img)
        axes[1].imshow(self.gamma_corrected, cmap='gray')
        axes[0].axis('off')
        axes[1].axis('off')
        axes[0].set_title('')
        axes[1].set_title('')
        self.image_file_name = self.image_choice.get().split('.')[0]
        self.image_path = ''.join([PATH, self.image_file_name,'_gamma_corrected.png'])
        plt.savefig(self.image_path)

        self.plot_image(self.gamma_corrected,  image_name='_'.join([self.image_file_name,'gamma_corrected_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_gamma_corrected_only.png']))

    def log_transformation_filter(self):
        ## s = c * log(1 + r)
        self.c = 5
        if self.right_entry.get():
            self.c = float(self.right_entry.get())
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.log_corrected = self.c * np.log(1 + self.img)

        fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor='none')
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.2)
        axes[0].imshow(self.img)
        axes[1].imshow(self.log_corrected, cmap='gray')
        axes[0].axis('off')
        axes[1].axis('off')
        axes[0].set_title('')
        axes[1].set_title('')
        self.image_file_name = self.image_choice.get().split('.')[0]
        self.image_path = ''.join([PATH, self.image_file_name,'_logarithmic_corrected.png'])
        plt.savefig(self.image_path)

        self.plot_image(self.log_corrected, image_name='_'.join([self.image_file_name,'logarithmic_corrected_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_logarithmic_corrected_only.png']))

    def gray_filter(self):
        self.gamma = 1
        if self.right_entry.get():
            self.gamma = float(self.right_entry.get())
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=False))

        # Get the dimensions of the image
        height, width, channels = self.img.shape

        # Create a new 2D array to store the grayscale image
        self.img_gray = np.zeros((height, width), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                # Get the pixel value of each color channel
                r, g, b = self.img[y, x]

                # Apply gamma correction to each channel
                r_corrected = int((r / 255.0) ** self.gamma * 255.0)
                g_corrected = int((g / 255.0) ** self.gamma * 255.0)
                b_corrected = int((b / 255.0) ** self.gamma * 255.0)

                # Calculate the grayscale value of the pixel
                self.gray_value = int((r_corrected + g_corrected + b_corrected) / 3)

                # Formula for luminance, which is a weighted sum of the color channels.
                # The weights used in the formula are based on the sensitivity of the human eye to different colors.
                # self.gray_value = int(0.2126 * r_corrected + 0.7152 * g_corrected + 0.0722 * b_corrected)

                # The weights used are 0.3, 0.59, and 0.11, which are commonly used values that give a pleasing result for most images.
                # self.gray_value = int(0.3 * r_corrected + 0.59 * g_corrected + 0.11 * b_corrected)

                # Set the grayscale value in the img_gray array
                self.img_gray[y, x] = self.gray_value


        # self.image_file_name = self.image_choice.get().split('.')[0]

        fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor='none')
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.2)

        axes[0].imshow(self.img)
        axes[1].imshow(self.img_gray, cmap='gray')
        axes[0].axis('off')
        axes[1].axis('off')
        axes[0].set_title('')
        axes[1].set_title('')
        self.image_file_name = self.image_choice.get().split('.')[0]
        self.image_path = ''.join([PATH, self.image_file_name,'_gray.png'])
        plt.savefig(self.image_path)

        self.plot_image(self.img_gray, image_name='_'.join([self.image_file_name,'gray_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_gray.png']))


    def histogram_maker(self):
        print('Path: ', PATH + self.image_choice.get())
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.img_min, self.img_max = self.img.min(), self.img.max()
        # Create an empty dictionary to store pixel value counts
        self.counts = {}

        # Loop over each pixel in the image and increment the count for the corresponding pixel value
        for i in range(self.img.shape[0]):
            for j in range(self.img.shape[1]):
                pixel_value = self.img[i,j]
                if pixel_value in self.counts:
                    self.counts[pixel_value] += 1
                else:
                    self.counts[pixel_value] = 1

        # Convert the dictionary to two lists: pixel values and counts
        self.pixel_values = list(self.counts.keys())
        self.counts_list = list(self.counts.values())

        plt.xlabel("Pixel Values")
        plt.ylabel("Frequency")
        plt.bar(self.pixel_values, self.counts_list)
        plt.xlabel("Pixel Values")
        plt.ylabel("Frequency")
        plt.bar(self.pixel_values, self.counts_list)

        self.image_file_name = self.image_choice.get().split('.')[0]
        self.image_path = ''.join([PATH, self.image_file_name,'_histogram.png'])
        plt.savefig(self.image_path)
        self.display_image_function(''.join([PATH, self.image_file_name, '_histogram.png']))

    def histogram_equalization(self):
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))

        # Calculate the PDF (probability density function)
        self.pdf = {}
        for row in range(self.img.shape[0]):
            for col in range(self.img.shape[1]):
                pixel_value = self.img[row, col]
                if pixel_value not in self.pdf:
                    self.pdf[pixel_value] = (0, 0)
                pdf_value, pixel_count = self.pdf[pixel_value]
                pdf_value += 1 / self.img.size
                pixel_count += 1
                self.pdf[pixel_value] = (pdf_value, pixel_count)

        for key, value in self.pdf.items():
            pixel_value = key
            pdf_value = value[0]
            pixel_count = value[1]
            print(f"Pixel value: {pixel_value}, PDF value: {pdf_value}, Pixel count: {pixel_count}")

        # Calculate the CDF (cumulative distribution function)
        self.cdf = {}
        cdf_values = []
        cdf_sum = 0
        for i in range(256):
            if i in self.pdf:
                pdf_value = self.pdf[i][0]
                pixel_count = self.pdf[i][1]
                cdf_sum += pdf_value * pixel_count
            self.cdf[i] = cdf_sum
            cdf_values.append(cdf_sum)

        # Equalize image
        self.img_equalized = np.interp(self.img.flatten(), list(self.cdf.keys()), list(self.cdf.values())).reshape(self.img.shape)

        # Display the original and equalized images side by side
        fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor='none')
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.2)
        axes[0].imshow(self.img, cmap='gray')
        axes[1].imshow(self.img_equalized, cmap='gray')
        axes[0].axis('off')
        axes[1].axis('off')
        axes[0].set_title('')
        axes[1].set_title('')

        self.image_file_name = self.image_choice.get().split('.')[0]
        self.image_path = ''.join([PATH, self.image_file_name,'_equalization.png'])
        plt.savefig(self.image_path)
        self.plot_image(self.img_equalized, image_name='_'.join([self.image_file_name,'equalization_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_equalization.png']))


    def monitor_performance(self, func):
        def wrapper():
            start_time = time.time()
            process = psutil.Process()
            mem_start = process.memory_info().rss / 1024 / 1024
            func()
            mem_end = process.memory_info().rss / 1024 / 1024
            end_time = time.time()
            elapsed_time = end_time - start_time
            peak_mem_usage = max(mem_start, mem_end)
            self.main_display_momory_label.configure(text=f"{peak_mem_usage:.3f} MB")
            self.main_display_run_label.configure(text=f"{elapsed_time:.3f} seconds")
        return wrapper



    def plot_image(self, image, cmap_value:str = 'Greys_r', image_name:str = ''):
        image_name = PATH + image_name
        plt.imsave(image_name, image, cmap=cmap_value)



if __name__ == "__main__":
    # print('0', os.listdir("../Computer_image_processing/Photoshop/img"))
    # print('1', os.listdir("Photoshop/img"))
    # print('2', os.listdir("Photoshop/"))
    FILES_IMAGES = os.listdir(PATH)
    # FILES_IMAGES = os.listdir("Photoshop/img")
    # FILES_IMAGES = [item.split('.', 1)[0] for item in FILES_IMAGES]
    app = App()
    app.mainloop()
