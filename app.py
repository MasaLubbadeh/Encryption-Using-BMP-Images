import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # for Combobox
from PIL import Image, ImageTk
import ttkbootstrap as ttk


# Create the main application window
root = tk.Tk()
root.title("Encryption with images")
root.geometry("1400x700")  # Adjusted size for larger display areas


style = ttk.Style()
style.configure("Purple.TButton", 
                background="#7d629c",  # Purple background
                foreground="#FFFFFF",  # Text color
                font=("Arial", 10),      # Font type and size
                padding=13,             # Padding around the text
                borderwidth=0,          # Border width
               )   

# Placeholder variables for images and secret text
cover_image = None
secret_text = ""

#root.config(bg="#302a2a")  # background color

# Load the background image
background_image = Image.open("images/Wallpaper.jpg")  # Replace with your image path
background_image = background_image.resize((1400, 700))  # Resize to fit the window
background_photo = ImageTk.PhotoImage(background_image)

# Create a Label to hold the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the whole window

########################################################################################################

# Function declarations

# Function to display an image in a specified area
def display_image(image, area):
    img_resized = image.resize((500, 350))  # Resize to fit the area
    img_tk = ImageTk.PhotoImage(img_resized)
    area.create_image(0, 0, anchor="nw", image=img_tk)  # anchor="nw" is to set the image in the right place
    area.image = img_tk  # for garbage collection


# Function to load a BMP image
def load_image():
    global cover_image
    file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])  # only allows bmp files
    if file_path:
        cover_image = Image.open(file_path)
        display_image(cover_image, cover_area)


# Function to load secret text from a file
def load_text_from_file():
    global secret_text
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            secret_text = file.read()
        text_area.delete("1.0", tk.END)  # Clear existing text
        text_area.insert("1.0", secret_text)  # Insert loaded text

# Function to save the modified image
def save_result_image():
    if cover_image is None:
        messagebox.showerror("Error", "No result image to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
    if file_path:
        cover_image.save(file_path)
        messagebox.showinfo("Success", "Image saved successfully.")

# Function to clear images and text area
def clear_all():
    global cover_image, secret_text
    cover_image = None
    secret_text = ""
    text_area.delete("1.0", tk.END)  # Clear text area
    cover_area.delete("all")  # Clear original image area
    result_area.delete("all")  # Clear result image area
    cover_area.create_text(cover_width // 2, cover_height // 2, text="Original Image", fill="gray")
    result_area.create_text(result_width // 2, result_height // 2, text="Result Image", fill="gray")


# GUI components

# Declaring variables to have fixed width and height for the original and result image
cover_width, cover_height = 500, 350  # original image dimensions
result_width, result_height = 500, 350  # result image dimensions

#############################################################################################################

# Creating a place to upload the Original image
# Area to display the chosen image
cover_area = tk.Canvas(root, width=cover_width, height=cover_height, bg="#FFF4F2", relief="solid")
cover_area.grid(row=0, column=0, padx=20, pady=(50, 20))
cover_area.create_text(cover_width // 2, cover_height // 2, text="Original Image", fill="gray")
# Button to upload the bmp image
load_button = ttk.Button(root, text="Load Image", command=load_image, width=27, style="Purple.TButton")
load_button.grid(row=1, column=0, pady=0)

# Button to restore hidden text from the image
restore_button = ttk.Button(root, text="Restore Secret Text",width=27,style="Purple.TButton")
restore_button.grid(row=2, column=0, pady=10)  # Adjusted row for new button

#############################################################################################################

# Creating a place for the Result image
# Area to display the result image
result_area = tk.Canvas(root, width=result_width, height=result_height, bg="#FFF4F2", relief="solid")
result_area.grid(row=0, column=2, padx=10, pady=(50, 20))
result_area.create_text(result_width // 2, result_height // 2, text="Result Image", fill="gray")
# Button to save the result image
save_button = ttk.Button(root, text="Save Result Image", command=save_result_image,width=27,style="Purple.TButton")
save_button.grid(row=2, column=2, pady=10)
# Label to display the restored text
restored_text_label = tk.Label(root, text="",  width=60, height=2, wraplength=300)
restored_text_label.grid(row=1, column=2, pady=10, padx=(0, 0))
restored_text_label.config(text="Restored text will appear here.")

#############################################################################################################

# Creating a place for entering the secret text by using 2 methods
# method 1 by entering the text manually
text_area = tk.Text(root, width=30, height=5)
text_area.grid(row=0, column=1, padx=10, pady=(0, 0))
text_area.insert("1.0", "Enter secret text here")
# method 2 uploading secret text from a file
load_text_button = ttk.Button(root, text="Load Text from File", command=load_text_from_file,width=27,style="Purple.TButton")
load_text_button.grid(row=1, column=1, pady=(50, 0))
# Combobox for selecting number of bits to use for hiding the secret text (1/2/3)
bit_depth_label = tk.Label(root, text="Select Bit Depth:")
bit_depth_label.grid(row=0, column=1, padx=(0, 100), pady=(300, 0))

bit_depth_combobox = ttk.Combobox(root, values=[1, 2, 3], state="readonly", width=5)
bit_depth_combobox.grid(row=0, column=1, padx=(125, 55), pady=(300, 0))
bit_depth_combobox.current(0)  # Set default to 1 bit

#############################################################################################################

# Button to clear everything
clear_button = ttk.Button(root, text="Clear All", command=clear_all,width=27,style="Purple.TButton")
clear_button.grid(row=2, column=1, pady=10)

#############################################################################################################

# Button to hide the secret text in the image
hide_button = ttk.Button(root, text="Hide Secret Text",width=27,style="Purple.TButton")
hide_button.grid(row=0, column=1, pady=(200, 50))

##############################################################################################################
# Function to hide secret text in the cover image
def hide_text():
    global cover_image, secret_text
    if cover_image is None:
        messagebox.showerror("Error", "Please load a cover image first.")
        return

    secret_text = text_area.get("1.0", "end-1c")  # Get text from text area
    binary_secret = ''.join(format(ord(char), '08b') for char in secret_text)  # Convert text to binary

    # Add a unique delimiter (e.g., eight "0" bytes to mark the end of text)
    binary_secret += "00000000" * 8

    # Get the selected bit depth
    bit_depth = int(bit_depth_combobox.get())

    # Process to embed the text in the LSBs
    pixels = cover_image.load()
    width, height = cover_image.size
    data_index = 0

    for y in range(height):
        for x in range(width):
            if data_index < len(binary_secret):
                r, g, b = pixels[x, y]
                # Set the LSBs according to the selected bit depth
                for i in range(bit_depth):
                    if data_index < len(binary_secret):
                        r = (r & ~(1 << i)) | int(binary_secret[data_index]) << i
                        data_index += 1
                pixels[x, y] = (r, g, b)
            else:
                break
        if data_index >= len(binary_secret):
            break

    # Display the modified image in the result area
    display_image(cover_image, result_area)
    messagebox.showinfo("Success", "Secret text hidden in image.")

# Update the Hide button to use the new function
hide_button.config(command=hide_text)

#############################################################################################################

# Function to restore (extract) the hidden secret text
def restore_text():
    global cover_image
    if cover_image is None:
        messagebox.showerror("Error", "Please load a cover image first.")
        return

    binary_data = ""
    pixels = cover_image.load()
    width, height = cover_image.size

    # Get the selected bit depth
    bit_depth = int(bit_depth_combobox.get())

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            # Extract the LSBs according to the selected bit depth
            for i in range(bit_depth):
                binary_data += str((r >> i) & 1)

    # Split binary data into bytes and decode to text
    secret_bytes = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if byte == "00000000":  # Check for the delimiter
            break
        secret_bytes.append(chr(int(byte, 2)))

    secret_text = ''.join(secret_bytes)
    restored_text_label.config(text=secret_text)  # Display the restored text

# Link the restore function to the button
restore_button.config(command=restore_text)

#############################################################################################################

# Start the application
root.mainloop()
