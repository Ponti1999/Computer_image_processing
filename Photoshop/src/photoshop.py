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
        self.right_sidebar_frame.grid_rowconfigure(7, weight=1)

        self.right_button_0 = customtkinter.CTkButton(self.right_sidebar_frame, text="Uniform filtered" ,command=self.uniform_filtered)
        self.right_button_0.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_1 = customtkinter.CTkButton(self.right_sidebar_frame, text="Gaussian filtered" ,command=self.gaussian_filtered)
        self.right_button_1.grid(row=1, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_2 = customtkinter.CTkButton(self.right_sidebar_frame, text="Median filtered" ,command=self.median_filtered)
        self.right_button_2.grid(row=2, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_3 = customtkinter.CTkButton(self.right_sidebar_frame, text="Sobel filtered" ,command=self.sobel_filtered)
        self.right_button_3.grid(row=3, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_4 = customtkinter.CTkButton(self.right_sidebar_frame, text="Negal" ,command=self.monitor_performance(self.negal_filter))
        self.right_button_4.grid(row=4, column=2, padx=20, pady=(20, 10), sticky="ns")

        self.right_button_5 = customtkinter.CTkButton(self.right_sidebar_frame, text="Gamma correction" ,command=self.monitor_performance(self.gamma_correction_filter))
        self.right_button_5.grid(row=5, column=2, padx=20, pady=(20, 10), sticky="ns")


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
            self.delete_image_size()
        except Exception as e:
            print(e)

    def delete_image_size(self):
        self.image_entry_x.delete(0, customtkinter.END)
        self.image_entry_y.delete(0, customtkinter.END)


    def login(self):
        print("Login button clicked")

    def uniform_filtered(self):
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.uniform_filter = unsharp_mask(self.img)
        print(f'Image shape: {self.img.shape}, mean: {self.img.mean()}, max: {self.img.max()}, min: {self.img.min()}')
        with open(PATH + 'image.txt', 'w') as f:
            for item in self.img:
                f.writelines(str(item))
        # print(self.uniform_filter)
        plt.imshow(self.uniform_filter, cmap='Greys')
        plt.show()

    def gaussian_filtered(self):
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.gaussian_filter = gaussian(self.img, sigma=GAUSSIAN_FILTERED_SIGMA)
        plt.imshow(self.gaussian_filter, cmap='Greys')
        plt.show()

    def median_filtered(self):
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=False))
        self.median_filter = median(self.img)
        plt.imshow(self.median_filter)
        plt.show()

    def sobel_filtered(self):
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=False))
        self.sobel_filter = sobel(self.img)
        plt.imshow(self.sobel_filter)
        plt.show()

    def roberts_filter(self):
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.roberts = roberts(self.img)
        plt.imshow(self.roberts, cmap='Greys')
        plt.show()

    def canny_edge_filter(self):
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.canny_edge = canny(self.img)
        plt.imshow(self.canny_edge, cmap='Greys')
        plt.show()

    def deconvolution_filter(self):
        self.psf = np.ones((3, 3)) / 9
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.deconvolved = restoration.unsupervised_wiener(self.img, self.psf)
        plt.imshow(self.deconvolved, cmap='Greys')
        plt.show()

    def negal_filter(self):
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.negal = 255 - self.img
        self.image_file_name = self.image_choice.get().split('.')[0]
        self.plot_image(self.img, title='Original', image_name='_'.join([self.image_file_name,'original.png']))
        self.plot_image(self.negal, title='Negal', image_name='_'.join([self.image_file_name,'negal.png']))
        self.image_open = Image.open(PATH + self.image_file_name + '_negal.png')
        self.display_image_function(''.join([PATH, self.image_file_name, '_negal.png']))


    def gamma_correction_filter(self):
        ## First, we normalize the pixel value by dividing it with the maximum pixel value, i.e., x / 255.0.
        ## Then, we raise this normalized pixel value to the power of the gamma value.
        ## Finally, we scale the gamma-corrected value back to the 8-bit range by multiplying with the maximum pixel value,
        ## Since we are using 8-bit images, the maximum pixel value is 255. We need to round the the gamma-corrected pixel value to the nearest integer.
        gamma = 0.5
        self.img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=True))
        self.gamma_corrected = (self.img / 255) ** gamma * 255
        self.image_file_name = self.image_choice.get().split('.')[0]
        self.plot_image(self.img, title='Original', image_name='_'.join([self.image_file_name,'original.png']))
        self.plot_image(self.gamma_corrected, title='Gamma corrected', image_name='_'.join([self.image_file_name,'gamma_corrected.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_gamma_corrected.png']))


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



    def plot_image(self, image, cmap_value:str = 'Greys_r', title: str = '', image_name:str = ''):
        plt.title(title)
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
