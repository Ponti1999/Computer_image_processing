import customtkinter
import tkinter
from PIL import ImageTk, Image
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

WINDOW_WIDTH = 1100
WINDOW_HIGH = 580


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
        self.left_sidebar_frame = customtkinter.CTkFrame(master=self, width=200, height=WINDOW_HIGH)
        self.left_sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.left_sidebar_frame.grid_rowconfigure(4, weight=1)

        # Instruction label
        self.instruction_label = customtkinter.CTkLabel(self.left_sidebar_frame, text="Select The Image", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.instruction_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Dropdown menu
        self.image_choice = customtkinter.CTkComboBox(self.left_sidebar_frame, values=FILES_IMAGES)
        self.image_choice.grid(row=1, column=0, padx=20, pady=10)
        # Button for importing the image
        self.load_image = customtkinter.CTkButton(self.left_sidebar_frame, text="Load image" ,command=self.display_image_function)
        self.load_image.grid(row=2, column=0, padx=20, pady=10)

        # create main entry and button
        self.main_display = customtkinter.CTkCanvas(self, width=300, height=300)
        self.main_display.grid(row=0, column=1, sticky="nsew")



        # Right sidebar
        self.right_sidebar_frame = customtkinter.CTkFrame(master=self, width=200, height=WINDOW_HIGH)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=3, sticky="nsew")
        self.right_sidebar_frame.grid_rowconfigure(4, weight=1)

        self.right_button_1 = customtkinter.CTkButton(self.right_sidebar_frame, text="1. funkció" ,command=self.display_image_function)
        self.right_button_1.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="nsew")




    def display_image_function(self):
        self.image_file = self.image_choice.get()
        self.image = ImageTk.PhotoImage(Image.open("Photoshop/img/" + self.image_file))
        self.main_display.create_image(0, 0, anchor="nw", image=self.image)

    def login():
        print("Login button clicked")


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