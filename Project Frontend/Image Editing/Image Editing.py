import os
import shutil
import time
import threading
from datetime import datetime
import subprocess

# GUI
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Pillow
from PIL import Image, ImageDraw, ImageFont, ImageTk

###############################################################################
#                          FRONTEND-ONLY CODE WITH UI                         #
###############################################################################

# --------------------- GLOBALS / PLACEHOLDERS -------------------- #
# In the original code, these might be loaded from JSON or Excel.
# For front-end-only purposes, we define some placeholders:

SETTINGS_HEADER_IMAGE = "InstaVision_Logo.png"  # Path to your header/logo image
IMAGE_BG       = "#1F1F1F"
MAIN_BG        = "#2A2A3B"
PRIMARY_COLOR  = "#00FFD9"
SECONDARY_COLOR= "#FC5DE0"
ACCENT_COLOR   = "#F5F242"
TEXT_COLOR     = "#FFFFFF"

# We pretend we have some “config” dictionary for Settings
config = {
    "replicate_api_token": "",
    "imgbb_api_key": "",
    "banned_words": [],
    "history_folder": ""  # For demonstration only
}

# For usage calculations (in a real scenario, you’d retrieve these from a backend)
monthly_usage_value = 0.0
total_usage_value = 0.0

# Some global paths to manage uploaded & edited images
loaded_image_path = None
last_edited_image_path = None
loading_bar = None

# ------------------------ MAIN TK WINDOW ------------------------ #
root = tk.Tk()
root.title("InstaVision")
root.state("zoomed")
root.configure(bg=MAIN_BG)

# Top-level frame for the main layout
top_frame = tk.Frame(root, bg=MAIN_BG)
top_frame.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid_columnconfigure(0, weight=0)  # Left panel
top_frame.grid_columnconfigure(1, weight=1)  # Right panel
top_frame.grid_rowconfigure(0, weight=1)

###############################################################################
#                                 LEFT FRAME                                  #
###############################################################################
left_frame = tk.Frame(top_frame, bg=MAIN_BG)
left_frame.grid(row=0, column=0, sticky="ns")

model_header_label = tk.Label(
    left_frame,
    text="InstaVision Image Editing",
    font=("Arial", 16, "bold"),
    fg=ACCENT_COLOR,
    bg=MAIN_BG
)
model_header_label.grid(row=0, column=0, sticky="nw", padx=35, pady=(10, 5))

model_label = tk.Label(
    left_frame,
    text="   Choose Your Editing Model",
    font=("Arial", 12, "bold"),
    bg=MAIN_BG,
    fg="#AAAAFF"
)
model_label.grid(row=0, column=0, sticky="nw", padx=40, pady=(40, 3))

model_var = tk.StringVar()
model_options = [
    "adirik_t2i-adapter-sdxl-openpose",
    "arielreplicate_deoldify-image",
    "black-forest-labs_flux-canny-pro",
    "black-forest-labs_flux-depth-pro",
    "black-forest-labs_flux-redux-dev",
    "cjwbw_rembg",
    "sujaykhandekar_object-removal",
    "timothybrooks_instruct-pix2pix"
]
model_dropdown = ttk.Combobox(
    left_frame,
    textvariable=model_var,
    values=model_options,
    state="readonly",
    width=45
)
model_dropdown.current(0)
model_dropdown["postcommand"] = lambda: model_dropdown.configure(height=20)
model_dropdown.grid(row=0, column=0, sticky="nw", padx=15, pady=(85, 10))

left_frame.grid_rowconfigure(1, weight=1)  # For spacing

###############################################################################
#                               STYLE SETUP                                   #
###############################################################################
style = ttk.Style()
style.theme_use("default")
style.configure(
    "EditButton.TButton",
    background=PRIMARY_COLOR,
    foreground=IMAGE_BG,
    padding=6,
    font=("Arial", 10, "bold")
)
style.map(
    "EditButton.TButton",
    background=[("active", SECONDARY_COLOR)],
    foreground=[("active", IMAGE_BG)]
)

###############################################################################
#                             LOADING ANIMATION                               #
###############################################################################
def start_loading_animation():
    global loading_bar
    if loading_bar is not None:
        return
    loading_bar = ttk.Progressbar(
        image_container,
        orient='horizontal',
        mode='indeterminate',
        length=300
    )
    loading_bar.place(relx=0.5, rely=0.5, anchor='center')
    loading_bar.start(10)

def stop_loading_animation():
    global loading_bar
    if loading_bar is not None:
        loading_bar.stop()
        loading_bar.destroy()
        loading_bar = None

###############################################################################
#                            IMAGE DISPLAY LOGIC                              #
###############################################################################
def display_image_in_label(image_path):
    """Display the image from image_path within the image_display Label."""
    _, ext = os.path.splitext(image_path.lower())
    if ext == ".svg":
        # Cannot directly display SVG in a tkinter Label
        image_display.configure(text="SVG output cannot be displayed.", image="")
        return
    try:
        container_width = image_container.winfo_width()
        container_height = image_container.winfo_height()
        img = Image.open(image_path)

        if container_width < 1:
            container_width = 600
        if container_height < 1:
            container_height = 600

        if hasattr(Image, 'Resampling'):
            img.thumbnail((container_width, container_height), Image.Resampling.LANCZOS)
        else:
            img.thumbnail((container_width, container_height), Image.LANCZOS)

        tk_img = ImageTk.PhotoImage(img)
        image_display.configure(image=tk_img, text="")
        image_display.image = tk_img
    except Exception as e:
        messagebox.showerror("Display Error", f"Could not display image: {e}")

###############################################################################
#                         UPLOAD / CLEAR IMAGE LOGIC                          #
###############################################################################
upload_button = None
info_label = None

def show_upload_button():
    global upload_button, info_label
    if upload_button is None:
        upload_button = ttk.Button(
            image_container,
            text="Upload",
            style="EditButton.TButton",
            command=upload_image
        )
        upload_button.place(relx=0.5, rely=0.4, anchor="center")
    else:
        upload_button.place(relx=0.5, rely=0.4, anchor="center")

    if info_label is None:
        info_label = tk.Label(
            image_container,
            text="Image will be displayed here.",
            bg=IMAGE_BG,
            fg=ACCENT_COLOR,
            font=("Arial", 10, "bold")
        )
        info_label.place(relx=0.5, rely=0.5, anchor="center")
    else:
        info_label.place(relx=0.5, rely=0.5, anchor="center")

def hide_upload_button():
    global upload_button, info_label
    if upload_button:
        upload_button.place_forget()
    if info_label:
        info_label.place_forget()

def upload_image():
    """Prompt user to select an image, copy it locally, and display it."""
    global loaded_image_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.*"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            ext = os.path.splitext(file_path)[1]
            new_filename = f"uploaded_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
            new_path = os.path.join(os.getcwd(), new_filename)
            shutil.copy(file_path, new_path)

            loaded_image_path = new_path
            display_image_in_label(loaded_image_path)
            hide_upload_button()
        except Exception as e:
            messagebox.showerror("Upload Error", f"Could not upload image: {e}")

def clear_button_action():
    """Clear the display and reset the loaded image paths."""
    global loaded_image_path, last_edited_image_path

    if loaded_image_path and os.path.exists(loaded_image_path):
        try:
            os.remove(loaded_image_path)
        except Exception:
            pass
    loaded_image_path = None
    last_edited_image_path = None

    image_display.configure(image="", text="")
    image_display.image = None

    show_upload_button()

###############################################################################
#                              EDIT / ACTION LOGIC                             #
###############################################################################
def on_edit_complete(final_edited_path):
    """Called after editing is done (stub)."""
    stop_loading_animation()
    global last_edited_image_path
    last_edited_image_path = final_edited_path
    display_image_in_label(final_edited_path)

def run_edit_in_thread(prompt_text, selected_model):
    """Mimics calling a backend for editing; purely a front-end stub."""
    global loaded_image_path
    if not loaded_image_path or not os.path.exists(loaded_image_path):
        root.after(0, lambda: [
            stop_loading_animation(),
            messagebox.showinfo("No Image", "No uploaded image found. Please upload an image first.")
        ])
        return

    try:
        # Simulate some work being done
        time.sleep(2)

        # In a real scenario, you'd call your editing function here.
        final_edited_path = loaded_image_path

        # Optionally remove the original or rename it, etc.
        if loaded_image_path and os.path.exists(loaded_image_path):
            try:
                os.remove(loaded_image_path)
            except Exception:
                pass
        loaded_image_path = None

        root.after(0, lambda: on_edit_complete(final_edited_path))

    except Exception as e:
        stop_loading_animation()
        messagebox.showerror("Editing Error", f"An error occurred: {e}")

def edit_image_action():
    """Triggered by the 'Edit' button."""
    prompt_text = prompt_entry.get("1.0", tk.END).strip()
    if not prompt_text:
        messagebox.showerror("Error", "Please enter a prompt.")
        return

    selected_model = model_var.get()
    start_loading_animation()

    thread = threading.Thread(
        target=run_edit_in_thread,
        args=(prompt_text, selected_model),
        daemon=True
    )
    thread.start()

###############################################################################
#                           RIGHT FRAME + DISPLAY                              #
###############################################################################
right_frame = tk.Frame(top_frame, bg=MAIN_BG)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

image_container = tk.Frame(right_frame, bg=IMAGE_BG)
image_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
image_container.grid_rowconfigure(0, weight=1)
image_container.grid_columnconfigure(0, weight=1)

image_display = tk.Label(
    image_container,
    bg=IMAGE_BG,
    fg=ACCENT_COLOR,
    relief="solid",
    bd=1
)
image_display.grid(row=0, column=0, sticky="nsew")

show_upload_button()

###############################################################################
#                              DOWNLOAD BUTTON                                #
###############################################################################
style.configure(
    "DownloadButton.TButton",
    background=ACCENT_COLOR,
    foreground=IMAGE_BG,
    padding=6,
    font=("Arial", 10, "bold")
)
style.map(
    "DownloadButton.TButton",
    background=[("active", SECONDARY_COLOR)],
    foreground=[("active", IMAGE_BG)]
)

def download_image():
    """Save last edited image to chosen path."""
    global last_edited_image_path
    if not last_edited_image_path or not os.path.exists(last_edited_image_path):
        messagebox.showerror("Error", "No image available to download.")
        return

    _, ext = os.path.splitext(last_edited_image_path.lower())
    file_path = filedialog.asksaveasfilename(
        defaultextension=ext,
        filetypes=[("Image Files", "*.*"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            Image.open(last_edited_image_path).save(file_path, "PNG")
            messagebox.showinfo("Saved", f"Image saved to: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the image:\n{e}")

download_button = ttk.Button(
    image_container,
    text="Download",
    style="DownloadButton.TButton",
    command=download_image
)
download_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

###############################################################################
#                             BOTTOM FRAME                                    #
###############################################################################
bottom_frame = tk.Frame(root, bg=MAIN_BG)
bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
bottom_frame.grid_columnconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(1, weight=0)
bottom_frame.grid_columnconfigure(2, weight=0)
bottom_frame.grid_columnconfigure(3, weight=0)

prompt_header_label = tk.Label(
    bottom_frame,
    text="Enter Text Prompt",
    font=("Arial", 11, "bold"),
    bg=MAIN_BG,
    fg=TEXT_COLOR
)
prompt_header_label.grid(row=0, column=0, sticky="nw", pady=(0, 5))

prompt_entry = tk.Text(
    bottom_frame,
    height=7,
    wrap=tk.WORD,
    bd=1,
    relief="solid",
    fg=TEXT_COLOR,
    bg="#353546"
)
prompt_entry.insert("1.0", "Type your editing instructions here...")
prompt_entry.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(5, 0))

edit_button = ttk.Button(
    left_frame,
    text="Edit",
    style="EditButton.TButton",
    command=edit_image_action
)
edit_button.grid(row=2, column=0, sticky="sew", padx=15, pady=10)

# "Clear" button
style.configure(
    "ClearButton.TButton",
    background="#CCCCCC",
    foreground=IMAGE_BG,
    padding=6,
    font=("Arial", 10, "bold")
)
style.map(
    "ClearButton.TButton",
    background=[("active", "#AAAAAA")],
    foreground=[("active", IMAGE_BG)]
)

clear_button = ttk.Button(
    bottom_frame,
    text="Clear",
    style="ClearButton.TButton",
    command=clear_button_action
)
clear_button.grid(row=0, column=1, sticky="ne", padx=10, pady=(0, 5))

###############################################################################
#                                USAGE BUTTON                                 #
###############################################################################
style.configure(
    "UsageButton.TButton",
    background="#AAAAFF",
    foreground=IMAGE_BG,
    padding=6,
    font=("Arial", 10, "bold")
)
style.map(
    "UsageButton.TButton",
    background=[("active", "#8888DD")],
    foreground=[("active", IMAGE_BG)]
)

def usage_button_action():
    """
    Open a new Toplevel window to show usage (front-end only).
    In the real app, you would fetch usage data from your backend logic.
    """
    usage_dialog = tk.Toplevel(root)
    usage_dialog.title("InstaVision Usage")
    usage_dialog.state("zoomed")
    usage_dialog.configure(bg=MAIN_BG)

    top_usage_frame = tk.Frame(usage_dialog, bg=MAIN_BG)
    top_usage_frame.place(relx=0, rely=0, relwidth=1, relheight=0.6)

    # Try to load and display a header image (logo) if present
    try:
        img = Image.open(SETTINGS_HEADER_IMAGE)
        screen_width = usage_dialog.winfo_screenwidth()
        screen_height = int(usage_dialog.winfo_screenheight() * 0.6)
        if hasattr(Image, 'Resampling'):
            img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        else:
            img = img.resize((screen_width, screen_height), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        header_label = tk.Label(top_usage_frame, image=tk_img, bg=MAIN_BG)
        header_label.image = tk_img
        header_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showwarning("Usage Header Image", f"Could not load usage header image:\n{e}")

    content_frame = tk.Frame(usage_dialog, bg=MAIN_BG)
    content_frame.place(relx=0, rely=0.6, relwidth=1, relheight=0.4)

    for i in range(2):
        content_frame.grid_rowconfigure(i, weight=0)
    content_frame.grid_columnconfigure(0, weight=0)
    content_frame.grid_columnconfigure(1, weight=1)

    usage_title = tk.Label(
        content_frame,
        text="InstaVision Usage Summary",
        font=("Arial", 20, "bold"),
        bg=MAIN_BG,
        fg=TEXT_COLOR
    )
    usage_title.grid(row=0, column=0, columnspan=2, pady=(10, 30))

    # Show placeholder usage data
    label_monthly = tk.Label(
        content_frame,
        text=f"Usage This Month:  ${monthly_usage_value:.4f}",
        font=("Arial", 14, "bold"),
        bg=MAIN_BG,
        fg=TEXT_COLOR
    )
    label_monthly.grid(row=1, column=0, sticky="e", padx=(30, 10), pady=(5, 3))

    label_total = tk.Label(
        content_frame,
        text=f"Total Lifetime Usage:  ${total_usage_value:.4f}",
        font=("Arial", 14, "bold"),
        bg=MAIN_BG,
        fg=TEXT_COLOR
    )
    label_total.grid(row=2, column=0, sticky="e", padx=(30, 10), pady=(5, 3))

usage_button = ttk.Button(
    bottom_frame,
    text="Usage",
    style="UsageButton.TButton",
    command=usage_button_action
)
usage_button.grid(row=0, column=2, sticky="ne", padx=10, pady=(0, 5))

###############################################################################
#                              SETTINGS BUTTON                                #
###############################################################################
style.configure(
    "SettingsButton.TButton",
    background=SECONDARY_COLOR,
    foreground=IMAGE_BG,
    padding=6,
    font=("Arial", 10, "bold")
)
style.map(
    "SettingsButton.TButton",
    background=[("active", PRIMARY_COLOR)],
    foreground=[("active", IMAGE_BG)]
)

def open_settings_dialog():
    """
    Open a new Toplevel window with “Settings.” 
    In the real app, you'd load/save these from a config file or database.
    """
    settings_dialog = tk.Toplevel(root)
    settings_dialog.title("InstaVision Settings")
    settings_dialog.state("zoomed")
    settings_dialog.configure(bg=MAIN_BG)

    top_settings_frame = tk.Frame(settings_dialog, bg=MAIN_BG)
    top_settings_frame.place(relx=0, rely=0, relwidth=1, relheight=0.6)

    # Try to load a header image
    try:
        img = Image.open(SETTINGS_HEADER_IMAGE)
        screen_width = settings_dialog.winfo_screenwidth()
        screen_height = int(settings_dialog.winfo_screenheight() * 0.6)
        if hasattr(Image, 'Resampling'):
            img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        else:
            img = img.resize((screen_width, screen_height), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)

        header_label = tk.Label(top_settings_frame, image=tk_img, bg=MAIN_BG)
        header_label.image = tk_img
        header_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showwarning("Settings Image", f"Could not load settings header image:\n{e}")

    content_frame = tk.Frame(settings_dialog, bg=MAIN_BG)
    content_frame.place(relx=0, rely=0.6, relwidth=1, relheight=0.4)

    for i in range(5):
        content_frame.grid_rowconfigure(i, weight=0)
    content_frame.grid_columnconfigure(0, weight=0)
    content_frame.grid_columnconfigure(1, weight=1)

    settings_title = tk.Label(
        content_frame,
        text="InstaVision Settings",
        font=("Arial", 20, "bold"),
        bg=MAIN_BG,
        fg=TEXT_COLOR
    )
    settings_title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Replicate API Token
    replicate_label = tk.Label(
        content_frame,
        text="Replicate API Token",
        font=("Arial", 14, "bold"),
        bg=MAIN_BG,
        fg=TEXT_COLOR
    )
    replicate_label.grid(row=1, column=0, sticky="e", padx=(30, 10), pady=(5, 3))

    replicate_entry = tk.Entry(content_frame, width=60, fg="black", bg="white")
    replicate_entry.grid(row=1, column=1, sticky="w", padx=(0, 30), pady=(5, 3))
    replicate_entry.insert(0, config.get("replicate_api_token", ""))

    # ImgBB API Key
    imgbb_label = tk.Label(
        content_frame,
        text="ImgBB API Key",
        font=("Arial", 14, "bold"),
        bg=MAIN_BG,
        fg=TEXT_COLOR
    )
    imgbb_label.grid(row=2, column=0, sticky="e", padx=(30, 10), pady=(5, 3))

    imgbb_entry = tk.Entry(content_frame, width=60, fg="black", bg="white")
    imgbb_entry.grid(row=2, column=1, sticky="w", padx=(0, 30), pady=(5, 3))
    imgbb_entry.insert(0, config.get("imgbb_api_key", ""))

    # Banned Words
    banned_label = tk.Label(
        content_frame,
        text="Banned Words (comma-separated)",
        font=("Arial", 14, "bold"),
        bg=MAIN_BG,
        fg=TEXT_COLOR
    )
    banned_label.grid(row=3, column=0, sticky="e", padx=(30, 10), pady=(10, 3))

    banned_text = tk.Text(content_frame, width=60, height=2, fg="black", bg="white")
    banned_text.grid(row=3, column=1, sticky="w", padx=(0, 30), pady=(10, 3))
    current_banned = config.get("banned_words", [])
    banned_text.insert("1.0", ", ".join(current_banned))

    # History folder button
    history_button_style = ttk.Style()
    history_button_style.configure(
        "HistoryButton.TButton",
        background="#AAAAFF",
        foreground=IMAGE_BG,
        padding=6,
        font=("Arial", 10, "bold")
    )
    history_button_style.map(
        "HistoryButton.TButton",
        background=[("active", "#8888DD")],
        foreground=[("active", IMAGE_BG)]
    )

    def open_history_folder():
        history_path = config.get("history_folder", "")
        if not history_path or not os.path.isdir(history_path):
            messagebox.showerror("Error", "History folder path is invalid or not set.")
            return
        try:
            # Windows
            os.startfile(history_path)
        except:
            # macOS/Linux fallback
            try:
                subprocess.Popen(["open", history_path])
            except:
                messagebox.showerror("Error", f"Unable to open folder: {history_path}")

    history_button = ttk.Button(
        content_frame,
        text="History",
        style="HistoryButton.TButton",
        command=open_history_folder
    )
    history_button.grid(row=4, column=1, sticky="w", padx=(0, 30), pady=(10, 3))

    # Save Settings
    save_button_style = ttk.Style()
    save_button_style.configure(
        "SettingsSave.TButton",
        background=ACCENT_COLOR,
        foreground=IMAGE_BG,
        padding=6,
        font=("Arial", 12, "bold")
    )
    save_button_style.map(
        "SettingsSave.TButton",
        background=[("active", SECONDARY_COLOR)],
        foreground=[("active", IMAGE_BG)]
    )

    def save_settings():
        config["replicate_api_token"] = replicate_entry.get().strip()
        config["imgbb_api_key"] = imgbb_entry.get().strip()

        new_banned = banned_text.get("1.0", tk.END).strip()
        if new_banned:
            config["banned_words"] = [w.strip() for w in new_banned.split(",") if w.strip()]
        else:
            config["banned_words"] = []

        # In the real app, you'd persist these to a file or DB.
        messagebox.showinfo("Settings Saved", "Your settings have been updated!")
        settings_dialog.destroy()

    save_button = ttk.Button(
        content_frame,
        text="Save Settings",
        style="SettingsSave.TButton",
        command=save_settings
    )
    save_button.grid(row=4, column=0, columnspan=2, pady=(20, 10))

settings_button = ttk.Button(
    bottom_frame,
    text="Settings",
    style="SettingsButton.TButton",
    command=open_settings_dialog
)
settings_button.grid(row=0, column=3, sticky="ne", padx=10, pady=(0, 5))

###############################################################################
#                                  MAINLOOP                                   #
###############################################################################
if __name__ == "__main__":
    root.mainloop()
