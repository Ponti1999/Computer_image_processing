import tkinter
import customtkinter
from skimage import io, img_as_ubyte
from matplotlib import pyplot as plt
from PIL import ImageTk, Image
import numpy as np
import psutil
import time
from multiprocessing import Pool
import multiprocessing as mp
import os


PATH = 'Photoshop/img/'
WINDOW_WIDTH = 1100
WINDOW_HIGH = 580
IMAGE_LOAD_DIVIDER = 1.5
GAUSSIAN_FILTERED_SIGMA = 1
GAUSSIAN_FILTERED_SIZE = 5
MEDIAN_FILTERED_SIZE = 5


def process_block(block):
    i, j, block_img = block
    block_filtered = np.zeros_like(block_img)
    for x in range(1, block_img.shape[0]-1):
        for y in range(1, block_img.shape[1]-1):
            mean = np.mean(block_img[x-1:x+2, y-1:y+2])
            block_filtered[x, y] = mean
    return (i, j, block_filtered)


# Define a function to compute the Sobel edge detection for a given pixel
def compute_sobel(args):
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    img, i, j = args
    gx = np.sum(kernel_x * img[i-1:i+2, j-1:j+2])
    gy = np.sum(kernel_y * img[i-1:i+2, j-1:j+2])
    mag = np.sqrt(gx**2 + gy**2)
    return mag > 128


def compute_laplace(img, i, j, kernel, threshold):
    laplace_filtered = np.sum(kernel * img[i-1:i+2, j-1:j+2])
    if laplace_filtered < threshold:
        return 0
    else:
        return 255


def negate_pixel(pixel):
        return 255 - pixel



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
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

        self.right_button_0 = customtkinter.CTkButton(self.right_sidebar_frame, text="Negate" ,command=self.monitor_performance(self.negate_filter, gray=True))
        self.right_button_0.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_1 = customtkinter.CTkButton(self.right_sidebar_frame, text="Gamma correction" ,command=self.monitor_performance(self.gamma_correction_filter, gray=True))
        self.right_button_1.grid(row=1, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_2 = customtkinter.CTkButton(self.right_sidebar_frame, text="Logarithmic correction" ,command=self.monitor_performance(self.log_transformation_filter, gray=True))
        self.right_button_2.grid(row=2, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_3 = customtkinter.CTkButton(self.right_sidebar_frame, text="Gray transformation" ,command=self.monitor_performance(self.gray_filter, gray=False))
        self.right_button_3.grid(row=3, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_4 = customtkinter.CTkButton(self.right_sidebar_frame, text="Histogram create" ,command=self.monitor_performance(self.histogram_maker, gray=True))
        self.right_button_4.grid(row=4, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_5 = customtkinter.CTkButton(self.right_sidebar_frame, text="Histogram Equalization" ,command=self.monitor_performance(self.histogram_equalization, gray=True))
        self.right_button_5.grid(row=5, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_6 = customtkinter.CTkButton(self.right_sidebar_frame, text="3x3 mean filter multi process", command=self.monitor_performance(self.mean_filter, gray=True))
        self.right_button_6.grid(row=6, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_6 = customtkinter.CTkButton(self.right_sidebar_frame, text="3x3 mean filter basic", command=self.monitor_performance(self.mean_filter2, gray=True))
        self.right_button_6.grid(row=7, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_6 = customtkinter.CTkButton(self.right_sidebar_frame, text="Gaussian filter", command=self.monitor_performance(self.gaussian_filter, gray=True))
        self.right_button_6.grid(row=8, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_6 = customtkinter.CTkButton(self.right_sidebar_frame, text="Sobel edge detector", command=self.monitor_performance(self.sobel_edge_detector, gray=True))
        self.right_button_6.grid(row=9, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_6 = customtkinter.CTkButton(self.right_sidebar_frame, text="Laplace edge detector", command=self.monitor_performance(self.laplace_edge_detector, gray=True))
        self.right_button_6.grid(row=10, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_label = customtkinter.CTkLabel(self.right_sidebar_frame, text="Value: ")
        self.right_label.grid(row=11, column=2, padx=10, pady=10, sticky="w")
        self.right_entry = customtkinter.CTkEntry(self.right_sidebar_frame, width=75)
        self.right_entry.grid(row=11, column=2, padx=10, sticky="e")



    def display_image_function(self, *args):
        try:
            if args:
                self.image_open = Image.open(*args)
                self.image_choice.configure(values=os.listdir(PATH))
            else:
                self.image_file = self.image_choice.get()
                self.image_open = Image.open(PATH + self.image_file)
            if self.image_entry_x.get() == "" or self.image_entry_y.get() == "":
                if self.image_open.size[0] > 1500:
                    self.image_entry_x.insert(0, self.image_open.size[0]/3)
                    self.image_entry_y.insert(0, self.image_open.size[1]/3)
                else:
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


    def monitor_performance(self, func, gray:bool):
        def wrapper():
            img = img_as_ubyte(io.imread(PATH + self.image_choice.get(), as_gray=gray))
            start_time = time.time()
            process = psutil.Process()
            mem_start = process.memory_info().rss / 1024 / 1024
            func(img)
            mem_end = process.memory_info().rss / 1024 / 1024
            end_time = time.time()
            elapsed_time = end_time - start_time
            peak_mem_usage = max(mem_start, mem_end)
            self.main_display_momory_label.configure(text=f"{peak_mem_usage:.3f} MB")
            self.main_display_run_label.configure(text=f"{elapsed_time:.3f} seconds")
        return wrapper


    def negate_filter(self, img):
        # 7 sec run time
        # self.img_negate_filter = np.zeros_like(img)
        # with mp.Pool(processes=4) as pool:
        #     tasks = [(img[i, j]) for i in range(img.shape[0]) for j in range(img.shape[1])]
        #     # Submit the tasks to the process pool and get the results
        #     results = pool.map(negate_pixel, tasks)
        #     # Reshape the results into an image
        #     self.img_negate_filter = np.reshape(results, img.shape)

        # 0.9 sec run time
        self.img_negate_filter = 255 - img

        self.original_and_equalized(img, self.img_negate_filter, '_negate.png')

        self.plot_image(self.img_negate_filter, image_name='_'.join([self.image_file_name,'negate_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_negate.png']))


    def gamma_correction_filter(self, img):
        self.gamma = 0.5
        if self.right_entry.get():
            self.gamma = float(self.right_entry.get())
        self.gamma_corrected = (img / 255) ** self.gamma * 255

        self.original_and_equalized(img, self.gamma_corrected, '_gamma_corrected.png')

        self.plot_image(self.gamma_corrected,  image_name='_'.join([self.image_file_name,'gamma_corrected_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_gamma_corrected.png']))


    def log_transformation_filter(self, img):
        ## s = c * log(1 + r)
        self.c = 5
        if self.right_entry.get():
            self.c = float(self.right_entry.get())
        self.log_corrected = self.c * np.log(1 + img)

        self.original_and_equalized(img, self.log_corrected, '_logarithmic_corrected.png')

        self.plot_image(self.log_corrected, image_name='_'.join([self.image_file_name,'logarithmic_corrected_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_logarithmic_corrected.png']))


    def gray_filter(self, img):
        self.gamma = 1
        if self.right_entry.get():
            self.gamma = float(self.right_entry.get())

        # Create a new 2D array to store the grayscale image
        self.img_gray = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)

        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                # Get the pixel value of each color channel
                r, g, b = img[y, x]

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

        self.original_and_equalized(img, self.img_gray, '_gray.png')

        self.plot_image(self.img_gray, image_name='_'.join([self.image_file_name,'gray_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_gray.png']))


    def histogram_maker(self, img):
        self.img_min, self.img_max = img.min(), img.max()
        # Create an empty dictionary to store pixel value counts
        self.counts = {}

        # Loop over each pixel in the image and increment the count for the corresponding pixel value
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pixel_value = img[i,j]
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


    def histogram_equalization(self, img):
        # Calculate the PDF (probability density function)
        self.pdf = {}
        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                pixel_value = img[row, col]
                if pixel_value not in self.pdf:
                    self.pdf[pixel_value] = (0, 0)
                pdf_value, pixel_count = self.pdf[pixel_value]
                pdf_value += 1 / img.size
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
        self.img_equalized = np.interp(img.flatten(), list(self.cdf.keys()), list(self.cdf.values())).reshape(img.shape)

        # Display the original and equalized images side by side
        self.original_and_equalized(img, self.img_equalized, '_equalization.png')

        self.plot_image(self.img_equalized, image_name='_'.join([self.image_file_name,'equalization_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_equalization.png']))


    def mean_filter(self, img):
        self.filtered_img = np.zeros_like(img)

        # Divide the image into smaller blocks
        block_size = 100
        blocks = []
        for i in range(0, img.shape[0], block_size):
            for j in range(0, img.shape[1], block_size):
                blocks.append((i, j, img[i:i+block_size, j:j+block_size]))

        # Process all blocks in parallel using different processes
        with mp.Pool() as pool:
            results = pool.map(process_block, blocks)

        # Merge the results to form the final filtered image
        for i, j, block_filtered in results:
            self.filtered_img[i:i+block_size, j:j+block_size] = block_filtered

        # Display the original and equalized images side by side
        self.original_and_equalized(img, self.filtered_img, '_mean_mp.png')

        self.plot_image(self.filtered_img, image_name='_'.join([self.image_file_name,'mean_mp_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_mean_mp.png']))


    def mean_filter2(self, img):
        self.filtered_img = np.zeros_like(img)
        for i in range(1, img.shape[0]-1):
            for j in range(1, img.shape[1]-1):
                mean = np.mean(img[i-1:i+2, j-1:j+2])
                self.filtered_img[i, j] = mean

        # Display the original and equalized images side by side
        self.original_and_equalized(img, self.filtered_img, '_mean.png')

        self.plot_image(self.filtered_img, image_name='_'.join([self.image_file_name,'mean_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_mean.png']))


    def gaussian_kernel(self, size, sigma):
        global GAUSSIAN_FILTERED_SIGMA
        self.gaussian_filtered_sigma = GAUSSIAN_FILTERED_SIGMA
        if self.right_entry.get():
            gaussian_filtered_sigma = float(self.right_entry.get())
        kernel = np.zeros((size, size))
        center = size // 2
        for i in range(size):
            for j in range(size):
                x = i - center
                y = j - center
                kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        return kernel / (2 * np.pi * sigma**2)

    def gaussian_filter(self, img):
        kernel = self.gaussian_kernel(GAUSSIAN_FILTERED_SIZE, self.gaussian_filtered_sigma)
        padded_image = np.pad(img, GAUSSIAN_FILTERED_SIZE // 2, mode='edge')
        self.gaussian_filtered = np.zeros_like(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                self.gaussian_filtered[i, j] = np.sum(kernel * padded_image[i:i+GAUSSIAN_FILTERED_SIZE, j:j+GAUSSIAN_FILTERED_SIZE])

        # Display the original and equalized images side by side
        self.original_and_equalized(img, self.gaussian_filtered, '_gaussian.png')

        self.plot_image(self.gaussian_filtered, image_name='_'.join([self.image_file_name,'gaussian_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_gaussian.png']))


    def sobel_edge_detector(self, img):
        # 14 sec run time
        # Initialize output image
        self.sobel_filtered = np.zeros_like(img)

        # Create a process pool with 4 workers
        with mp.Pool(processes=4) as pool:
            # Create a list of tasks to compute the Sobel edge detection for each pixel in the image
            tasks = [(img, i, j) for i in range(1, img.shape[0]-1) for j in range(1, img.shape[1]-1)]
            # Submit the tasks to the process pool and get the results
            results = pool.map(compute_sobel, tasks)
            # Reshape the results into an image
            self.sobel_filtered[1:-1, 1:-1] = np.reshape([255 if r else 0 for r in results], (img.shape[0]-2, img.shape[1]-2))

        # 19 sec run time
        # Initialize output image
        # Iterate over each pixel in the image
        # for i in range(1, img.shape[0]-1):
        #     for j in range(1, img.shape[1]-1):
        #         # Compute gradient in x and y directions
        #         gx = np.sum(kernel_x * img[i-1:i+2, j-1:j+2])
        #         gy = np.sum(kernel_y * img[i-1:i+2, j-1:j+2])

        #         # Compute magnitude of gradient
        #         mag = np.sqrt(gx**2 + gy**2)

        #         # Threshold magnitude to obtain binary edge map
        #         if mag > 128:
        #             self.sobel_filtered[i, j] = 255

        # 79 sec
        # Define a function to compute the Sobel edge detection for a given pixel
        # def compute_sobel(i, j):
        #     gx = np.sum(kernel_x * img[i-1:i+2, j-1:j+2])
        #     gy = np.sum(kernel_y * img[i-1:i+2, j-1:j+2])
        #     mag = np.sqrt(gx**2 + gy**2)
        #     return mag > 128

        # # Create a thread pool with 4 workers
        # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        #     # Iterate over each pixel in the image
        #     for i in range(1, img.shape[0]-1):
        #         for j in range(1, img.shape[1]-1):
        #             # Submit a task to the thread pool to compute the Sobel edge detection for the current pixel
        #             future = executor.submit(compute_sobel, i, j)
        #             # Store the result in the output image
        #             self.sobel_filtered[i, j] = 255 if future.result() else 0

        self.original_and_equalized(img, self.sobel_filtered, '_sobel.png')

        self.plot_image(self.sobel_filtered, image_name='_'.join([self.image_file_name,'sobel_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_sobel.png']))

    def laplace_edge_detector(self, img):
        self.threshold = 50
        if self.right_entry.get():
            self.threshold = float(self.right_entry.get())
        kernel = np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]])

        # Apply Laplace filter to image
        self.laplace_filtered = np.zeros_like(img)

        # for i in range(1, img.shape[0]-1):
        #     for j in range(1, img.shape[1]-1):
        #         self.laplace_filtered[i,j] = np.sum(kernel * img[i-1:i+2, j-1:j+2])

        # # Threshold edge image
        # self.laplace_filtered[self.laplace_filtered < threshold] = 0
        # self.laplace_filtered[self.laplace_filtered >= threshold] = 255

        # Create a process pool with specified number of workers
        with mp.Pool(processes=4) as pool:
            # Create a list of tasks to compute the Laplace edge detection for each pixel in the image
            tasks = [(img, i, j, kernel, self.threshold) for i in range(1, img.shape[0]-1) for j in range(1, img.shape[1]-1)]
            # Submit the tasks to the process pool and get the results
            results = pool.starmap(compute_laplace, tasks)
            # Reshape the results into an image
            self.laplace_filtered[1:-1, 1:-1] = np.reshape(results, (img.shape[0]-2, img.shape[1]-2))

        # Display the original and equalized images side by side
        self.original_and_equalized(img, self.laplace_filtered, '_laplace.png')
        self.plot_image(self.laplace_filtered, image_name='_'.join([self.image_file_name,'laplace_only.png']))
        self.display_image_function(''.join([PATH, self.image_file_name, '_laplace.png']))

    def original_and_equalized(self, img, new_image, path_name:str):
        fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor='none')
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.2)
        axes[0].imshow(img, cmap='gray')
        axes[1].imshow(new_image, cmap='gray')
        axes[0].axis('off')
        axes[1].axis('off')
        axes[0].set_title('')
        axes[1].set_title('')
        self.image_file_name = self.image_choice.get().split('.')[0]
        self.image_path = ''.join([PATH, self.image_file_name, path_name])
        plt.savefig(self.image_path)



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
