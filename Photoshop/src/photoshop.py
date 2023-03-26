import tkinter
import customtkinter
from skimage import io, img_as_ubyte
from matplotlib import pyplot as plt
from scipy import ndimage
from PIL import ImageTk, Image
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

WINDOW_WIDTH = 1100
WINDOW_HIGH = 580
IMAGE_LOAD_DIVIDER = 4
UNIFORM_FILTERED_SIZE = 5
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


        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_display = customtkinter.CTkLabel(self.main_frame, width=700, height=450, text='')
        self.main_display.grid(row=0, column=1, sticky="nsew")



        # Right sidebar
        self.right_sidebar_frame = customtkinter.CTkFrame(master=self, width=200, height=WINDOW_HIGH)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=3, sticky="nsew")
        self.right_sidebar_frame.grid_rowconfigure(4, weight=1)

        self.right_button_1 = customtkinter.CTkButton(self.right_sidebar_frame, text="Uniform filtered" ,command=self.uniform_filtered)
        self.right_button_1.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_1 = customtkinter.CTkButton(self.right_sidebar_frame, text="Gaussian filtered" ,command=self.gaussian_filtered)
        self.right_button_1.grid(row=1, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_1 = customtkinter.CTkButton(self.right_sidebar_frame, text="Median filtered" ,command=self.median_filtered)
        self.right_button_1.grid(row=2, column=2, padx=20, pady=(20, 10), sticky="nsew")

        self.right_button_1 = customtkinter.CTkButton(self.right_sidebar_frame, text="Sobel filtered" ,command=self.sobel_filtered)
        self.right_button_1.grid(row=3, column=2, padx=20, pady=(20, 10), sticky="nsew")



    def display_image_function(self):
        try:
            self.image_file = self.image_choice.get()
            self.image_open = Image.open("Photoshop/img/" + self.image_file)
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
        self.img = img_as_ubyte(io.imread("Photoshop/img/" + self.image_choice.get(), as_gray=True))
        self.uniform_filter = ndimage.uniform_filter(self.img, size=UNIFORM_FILTERED_SIZE)
        print(self.img)
        # print(self.uniform_filter)
        plt.imshow(self.uniform_filter)
        plt.show()

    def gaussian_filtered(self):
        self.img = img_as_ubyte(io.imread("Photoshop/img/" + self.image_choice.get(), as_gray=True))
        self.gaussian_filter = ndimage.gaussian_filter(self.img, sigma=GAUSSIAN_FILTERED_SIGMA)
        plt.imshow(self.gaussian_filter)
        plt.show()

    def median_filtered(self):
        self.img = img_as_ubyte(io.imread("Photoshop/img/" + self.image_choice.get(), as_gray=False))
        self.median_filter = ndimage.median_filter(self.img, size=MEDIAN_FILTERED_SIZE)
        plt.imshow(self.median_filter)
        plt.show()

    def sobel_filtered(self):
        self.img = img_as_ubyte(io.imread("Photoshop/img/" + self.image_choice.get(), as_gray=False))
        self.sobel_filter = ndimage.sobel(self.img)
        plt.imshow(self.sobel_filter)
        plt.show()



if __name__ == "__main__":
    FILES_IMAGES = os.listdir("Photoshop/img")
    # FILES_IMAGES = [item.split('.', 1)[0] for item in FILES_IMAGES]
    app = App()
    app.mainloop()



# root = customtkinter.CTk()

# root.title("Test")
# root.geometry("800x650")

# canvas = customtkinter.CTkCanvas(master=root, width=400, height=400, bg="#2F2F2F")
# canvas.pack(anchor=tkinter.W, padx=20, pady=20)



# add_folder_images = ImageTk.PhotoImage(Image.open("Photoshop/img/add_folder.png").resize((20, 20), Image.ANTIALIAS))
# add_list_images = ImageTk.PhotoImage(Image.open("Photoshop/img/add_list.png").resize((20, 20), Image.ANTIALIAS))



# button_1 = customtkinter.CTkButton(master=root, text="Add Folder", image=add_folder_images, width=190, height=40, compound="top")
# button_1.pack(anchor=tkinter.E, pady=20, padx=20)

# button_2 = customtkinter.CTkButton(master=root, text="Add List", image=add_list_images, width=190, height=40, compound="right", fg_color="#D35B58", hover_color="#C77C78", command=login)
# button_2.pack(pady=20, padx=20)

# image_var = tkinter.StringVar()
# combobox = customtkinter.CTkComboBox(master=root, values=FILES_IMAGES, command=combobox_callback)
# combobox.pack(padx=20, pady=10)

# display  = ImageTk.PhotoImage(Image.open("Photoshop/img/add_list.png").resize((20, 20), Image.ANTIALIAS))

# display_image = customtkinter.CTkLabel(master=root, image=display, text="")
# display_image.pack(padx=20, pady=10)