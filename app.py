import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  #  for Combobox
from PIL import Image, ImageTk

# Create the main application window
root = tk.Tk()
root.title("Encryption with images")
root.geometry("1400x700")  # Adjusted size for larger display areas

# Placeholder variables for images and secret text
cover_image = None
secret_text = ""

#Adding background to thee main window

# Load the background image
background_image = Image.open("images/Wallpaper.jpg")  
background_image = background_image.resize((1400, 700))  
background_photo = ImageTk.PhotoImage(background_image)
# Background image must be held in a label so i created one
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the whole window



#GUI components

#Declaring variables to have fixed width and height for the original and result image
cover_width, cover_height = 500, 350  #original image dimentions
result_width, result_height = 500, 350  #result image dimentions

#############################################################################################################

#Creating a place to upload the Original image
#Area to display the chosen image
cover_area = tk.Canvas(root, width=cover_width, height=cover_height, bg="#FFF4F2", relief="solid")
cover_area.grid(row=0, column=0, padx=20, pady=(50,20))
cover_area.create_text(cover_width // 2, cover_height // 2, text="Original Image", fill="gray")
#Button to upload the bmp image
load_button = tk.Button(root, text="Load Image", width=30, height=2, bg="light pink")
load_button.grid(row=1, column=0, pady=0)

#############################################################################################################

#Creating a place for the Result image
#Area to display the result image
result_area = tk.Canvas(root, width=result_width, height=result_height, bg="#FFF4F2", relief="solid")
result_area.grid(row=0, column=2, padx=10, pady=(50,20))
result_area.create_text(result_width // 2, result_height // 2, text="Result Image", fill="gray")
#Button to restore the secret text from the image
restore_button = tk.Button(root, text="Restore Secret Text", width=30, height=2, bg="light pink")
restore_button.grid(row=1, column=2, pady=10,padx=(0,200))
#Button to save the result image
save_button = tk.Button(root, text="Save Result Image", width=30, height=2, bg="light pink")
save_button.grid(row=2, column=2, pady=10)
#Label to display the restored text
restored_text_label = tk.Label(root, text="", bg="light pink", width=30, height=2, wraplength=300)
restored_text_label.grid(row=1, column=2, pady=10,padx=(250,0))
restored_text_label.config(text="Restored text will appear here.")

#############################################################################################################

#Creating a place for entering the secret text by using 2 methods
#method 1 by entering the text manually
text_area = tk.Text(root, width=30, height=5, bg="light pink")
text_area.grid(row=0, column=1, padx=10, pady=(0,0))
text_area.insert("1.0", "Enter secret text here")
#method 2 uploading secret text from a file
load_text_button = tk.Button(root, text="Load Text from File", width=30, height=2, bg="light pink")
load_text_button.grid(row=1, column=1, pady=(50, 0))
#Combobox for selecting number of bits to use for hiding the secret text (1/2/3)
bit_depth_label = tk.Label(root, text="Select Bit Depth:", bg="light pink")
bit_depth_label.grid(row=0, column=1, padx=(0, 100), pady=(300, 0))

bit_depth_combobox = ttk.Combobox(root, values=[1, 2, 3], state="readonly", width=5)
bit_depth_combobox.grid(row=0, column=1, padx=(125, 55), pady=(300, 0))
bit_depth_combobox.current(0)  # Set default to 1 bit

#############################################################################################################
#Button to clear everything
clear_button = tk.Button(root, text="Clear All", width=30, height=2, bg="light pink")
clear_button.grid(row=2, column=1, pady=10)


# Start the application
root.mainloop()
