import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Importing ttk for Combobox
from PIL import Image, ImageTk

# Create the main application window
root = tk.Tk()
root.title("Encryption with Images")
root.geometry("1400x700")  # Adjusted size for larger display areas
root.config(bg="lightblue")  # You can use any color name or hex code

# Load the background image
background_image = Image.open("images/Wallpaper.jpg")  # Replace with your image path
background_image = background_image.resize((1400, 700))  # Resize to fit the window
background_photo = ImageTk.PhotoImage(background_image)

# Create a Label to hold the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the whole window

# Placeholder variables for images and secret text
cover_image = None
secret_text = ""

# Function to load a BMP image
def load_image():
    global cover_image
    file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
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

# Function to display an image in a specified area
def display_image(image, area):
    img_resized = image.resize((500, 350))  # Resize to fit the area
    img_tk = ImageTk.PhotoImage(img_resized)
    area.create_image(0, 0, image=img_tk)
    area.image = img_tk  # Store reference to avoid garbage collection

# Layout for the GUI
cover_width, cover_height = 500, 350  # Set dimensions for larger display
result_width, result_height = 500, 350

# Original image area (cover)
cover_area = tk.Canvas(root, width=cover_width, height=cover_height, bg="#FFF4F2", relief="solid")
cover_area.grid(row=0, column=0, padx=20, pady=(50,20))
cover_area.create_text(cover_width // 2, cover_height // 2, text="Original Image", fill="gray")

# Result image area
result_area = tk.Canvas(root, width=result_width, height=result_height, bg="#FFF4F2", relief="solid")
result_area.grid(row=0, column=2, padx=10, pady=(50,20))
result_area.create_text(result_width // 2, result_height // 2, text="Result Image", fill="gray")

# Secret text area
text_area = tk.Text(root, width=30, height=5, bg="light pink")
text_area.grid(row=0, column=1, padx=10, pady=(0,0))
text_area.insert("1.0", "Enter secret text here")

# Label to display restored text
restored_text_label = tk.Label(root, text="", bg="light pink", width=30, height=2, wraplength=300)
restored_text_label.grid(row=1, column=2, pady=10,padx=(250,0))
restored_text_label.config(text="Restored text will appear here.")

# Combobox to select number of bits to use for hiding text
bit_depth_label = tk.Label(root, text="Select Bit Depth:", bg="light pink")
bit_depth_label.grid(row=0, column=1, padx=(0, 100), pady=(300, 0))

bit_depth_combobox = ttk.Combobox(root, values=[1, 2, 3], state="readonly", width=5)
bit_depth_combobox.grid(row=0, column=1, padx=(125, 55), pady=(300, 0))
bit_depth_combobox.current(0)  # Set default to 1 bit

# Buttons
load_button = tk.Button(root, text="Load Image", command=load_image, width=30, height=2, bg="light pink")
load_button.grid(row=1, column=0, pady=0)

load_text_button = tk.Button(root, text="Load Text from File", command=load_text_from_file, width=30, height=2, bg="light pink")
load_text_button.grid(row=1, column=1, pady=(50, 0))

hide_button = tk.Button(root, text="Hide Secret Text", width=30, height=2, bg="light pink")
hide_button.grid(row=0, column=1, pady=(200,50))

restore_button = tk.Button(root, text="Restore Secret Text", width=30, height=2, bg="light pink")
restore_button.grid(row=1, column=2, pady=10,padx=(0,200))

save_button = tk.Button(root, text="Save Result Image", command=save_result_image, width=30, height=2, bg="light pink")
save_button.grid(row=2, column=2, pady=10)

clear_button = tk.Button(root, text="Clear All", command=clear_all, width=30, height=2, bg="light pink")
clear_button.grid(row=2, column=1, pady=10)

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
            # Extract LSBs according to the selected bit depth
            for i in range(bit_depth):
                binary_data += str((r >> i) & 1)  # Extract LSB of red
            
            # Only extracting from the red channel for simplicity
            if len(binary_data) >= 8 * 8:  # Stop after reading enough bits
                break
        if len(binary_data) >= 8 * 8:
            break

    # Convert binary to text
    secret_message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        if byte == "00000000":  # Stop if we reach the delimiter
            break
        secret_message += chr(int(byte, 2))
    
    restored_text_label.config(text=secret_message)

# Update the Restore button to use the new function
restore_button.config(command=restore_text)

# Start the application
root.mainloop()
