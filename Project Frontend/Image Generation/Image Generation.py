import os
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
# These mimic the style and structure of your editing UI code, but
# are focused on the Image Generation use case.

SETTINGS_HEADER_IMAGE = (
    "InstaVision_Logo.png"
)
# ^ Adjust this path if you want to display a logo in Usage/Settings windows.

IMAGE_BG         = "#1F1F1F"
MAIN_BG          = "#2A2A3B"
PRIMARY_COLOR    = "#00FFD9"
SECONDARY_COLOR  = "#FC5DE0"
ACCENT_COLOR     = "#F5F242"
TEXT_COLOR       = "#FFFFFF"

# Sample config dictionary (e.g., loaded from a file in a real app)
config = {
    "replicate_api_token": "",
    "banned_words": [],
    "history_folder_path": "",  # for demonstration only
}

# Usage placeholders
monthly_usage_value = 0.0
total_usage_value   = 0.0

# For demonstration, we pretend the "last generated image path" is stored here.
last_generated_image_path = None

# Will hold a loading bar widget while "generating" (simulated)
loading_bar = None

# Full list of generation models from your code
GENERATION_MODELS = [
    "ai-forever_kandinsky-2.2",
    "black-forest-labs_flux-1.1-pro-ultra",
    "black-forest-labs_flux-1.1-pro",
    "black-forest-labs_flux-dev",
    "black-forest-labs_flux-schnell",
    "bytedance_sdxl-lightning-4step",
    "cjwbw_animagine-xl-3.1",
    "datacte_proteus-v0.2",
    "datacte_proteus-v0.3",
    "fofr_sdxl-emoji",
    "fofr_sticker-maker",
    "lucataco_dreamshaper-xl-turbo",
    "lucataco_open-dalle-v1.1",
    "lucataco_realvisxl2-lcm",
    "nvidia_sana",
    "recraft-ai_recraft-v3",
    "stability-ai_stable-diffusion-3.5-medium",
    "stability-ai_stable-diffusion",
    "stability-ai_sdxl",
    "tstramer_material-diffusion"
]

###############################################################################
#                               MAIN WINDOW SETUP                             #
###############################################################################
root = tk.Tk()
root.title("InstaVision - Image Generation")
# “zoomed” attempts to maximize on Windows. If it doesn’t behave well, you can use geometry.
root.state("zoomed")
root.configure(bg=MAIN_BG)

# Main layout container
top_frame = tk.Frame(root, bg=MAIN_BG)
top_frame.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid_columnconfigure(0, weight=0)  # Left side
top_frame.grid_columnconfigure(1, weight=1)  # Right side
top_frame.grid_rowconfigure(0, weight=1)

###############################################################################
#                                  LEFT FRAME                                 #
###############################################################################
left_frame = tk.Frame(top_frame, bg=MAIN_BG)
left_frame.grid(row=0, column=0, sticky="ns")

# Header label
title_label = tk.Label(
    left_frame,
    text="InstaVision Image Generation",
    font=("Arial", 16, "bold"),
    fg=ACCENT_COLOR,
    bg=MAIN_BG
)
title_label.grid(row=0, column=0, sticky="nw", padx=35, pady=(10, 5))

# "Choose Model" label
model_label = tk.Label(
    left_frame,
    text="   Choose Your Generation Model",
    font=("Arial", 12, "bold"),
    bg=MAIN_BG,
    fg="#AAAAFF"
)
model_label.grid(row=0, column=0, sticky="nw", padx=40, pady=(40, 3))

model_var = tk.StringVar()
model_dropdown = ttk.Combobox(
    left_frame,
    textvariable=model_var,
    values=GENERATION_MODELS,
    state="readonly",
    width=50
)
model_dropdown.current(0)  # default to first model
model_dropdown["postcommand"] = lambda: model_dropdown.configure(height=20)
model_dropdown.grid(row=0, column=0, sticky="nw", padx=15, pady=(85, 10))

left_frame.grid_rowconfigure(1, weight=1)

# Style for the "Generate" button
style = ttk.Style()
style.theme_use("default")
style.configure(
    "GenerateButton.TButton",
    background=PRIMARY_COLOR,
    foreground=IMAGE_BG,
    padding=6,
    font=("Arial", 10, "bold")
)
style.map(
    "GenerateButton.TButton",
    background=[("active", SECONDARY_COLOR)],
    foreground=[("active", IMAGE_BG)]
)

###############################################################################
#                               LOADING BAR                                   #
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
#                             DISPLAY GENERATED IMAGE                          #
###############################################################################
def display_image_in_label(image_path):
    """Display an image from 'image_path' in the image_display label."""
    _, ext = os.path.splitext(image_path.lower())
    if ext == ".svg":
        image_display.configure(text="Cannot display SVG in tkinter label.", image="")
        return
    try:
        container_width = image_container.winfo_width()
        container_height = image_container.winfo_height()

        img = Image.open(image_path)
        # ensure container dimensions are not 0
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
        messagebox.showerror("Display Error", f"Could not display image:\n{e}")

###############################################################################
#                            GENERATION ACTION                                #
###############################################################################
def on_generation_complete(final_path):
    """Called after 'generation' finishes (fake)."""
    stop_loading_animation()

    global last_generated_image_path
    last_generated_image_path = final_path
    display_image_in_label(final_path)

def run_generation_in_thread(prompt_text, selected_model):
    """Simulate calling a backend to generate an image. Here we just wait & place a placeholder."""
    try:
        time.sleep(2)  # simulate some processing time

        # For demonstration, let's create a simple placeholder image
        # with the model name & prompt text.
        placeholder_name = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        placeholder_path = os.path.join(os.getcwd(), placeholder_name)
        create_placeholder_image(prompt_text, selected_model, placeholder_path)

        root.after(0, lambda: on_generation_complete(placeholder_path))

    except Exception as e:
        stop_loading_animation()
        messagebox.showerror("Generation Error", f"An error occurred:\n{e}")

def generate_image_action():
    """Handles the 'Generate' button click (fake generation)."""
    prompt_text = prompt_entry.get("1.0", tk.END).strip()
    if not prompt_text:
        messagebox.showerror("No Prompt", "Please enter a prompt.")
        return

    selected_model = model_var.get()
    start_loading_animation()

    thread = threading.Thread(
        target=run_generation_in_thread,
        args=(prompt_text, selected_model),
        daemon=True
    )
    thread.start()

###############################################################################
#                       PLACEHOLDER IMAGE CREATION (FAKE)                     #
###############################################################################
def create_placeholder_image(prompt, model, save_path):
    """
    Creates a 500×400 PNG with text showing the model & prompt,
    just to mimic an output image. This is purely for demonstration.
    """
    width, height = 500, 400
    bg_color = (31, 31, 31)  # same as #1F1F1F
    txt_color = (255, 255, 0)  # bright color for visibility

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        # A fallback if you don't have a .ttf on hand:
        font = ImageFont.load_default()
    except:
        font = None

    # Write the model name
    draw.text((10, 10), f"Model: {model}", fill=txt_color, font=font)

    # Write the prompt (wrap or just truncate)
    lines = []
    max_chars_per_line = 40
    for token in prompt.split():
        if not lines or len(lines[-1]) + len(token) + 1 > max_chars_per_line:
            lines.append(token)
        else:
            lines[-1] += " " + token
    y_off = 40
    for line in lines:
        draw.text((10, y_off), line, fill=txt_color, font=font)
        y_off += 20

    img.save(save_path, "PNG")

###############################################################################
#                                RIGHT FRAME                                  #
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
    text="Image will be displayed here.",
    bg=IMAGE_BG,
    fg=ACCENT_COLOR,
    relief="solid",
    bd=1
)
image_display.grid(row=0, column=0, sticky="nsew")

###############################################################################
#                               DOWNLOAD BUTTON                               #
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
    """Save the 'last_generated_image_path' to a user-chosen location."""
    global last_generated_image_path
    if not last_generated_image_path or not os.path.exists(last_generated_image_path):
        messagebox.showerror("No Image", "No generated image available to download.")
        return

    _, ext = os.path.splitext(last_generated_image_path.lower())
    file_path = filedialog.asksaveasfilename(
        defaultextension=ext,
        filetypes=[("Image Files", "*.*"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            Image.open(last_generated_image_path).save(file_path, "PNG")
            messagebox.showinfo("Saved", f"Image saved to: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the image:\n{e}")

download_btn = ttk.Button(
    image_container,
    text="Download",
    style="DownloadButton.TButton",
    command=download_image
)
download_btn.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

###############################################################################
#                               BOTTOM FRAME                                  #
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
prompt_entry.insert("1.0", "Type your prompt here...")
prompt_entry.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(5, 0))

# "Generate" button
generate_btn = ttk.Button(
    left_frame,
    text="Generate",
    style="GenerateButton.TButton",
    command=generate_image_action
)
generate_btn.grid(row=2, column=0, sticky="sew", padx=15, pady=10)

###############################################################################
#                               USAGE BUTTON                                  #
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
    Opens a Toplevel window to display usage info (no real logic).
    """
    usage_dialog = tk.Toplevel(root)
    usage_dialog.title("InstaVision Usage")
    usage_dialog.state("zoomed")
    usage_dialog.configure(bg=MAIN_BG)

    top_usage_frame = tk.Frame(usage_dialog, bg=MAIN_BG)
    top_usage_frame.place(relx=0, rely=0, relwidth=1, relheight=0.6)

    # Try loading a header image
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
        header_label.image = tk_img  # store ref
        header_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showwarning("Usage Header Image", f"Could not load usage header image:\n{e}")

    content_frame = tk.Frame(usage_dialog, bg=MAIN_BG)
    content_frame.place(relx=0, rely=0.6, relwidth=1, relheight=0.4)

    content_frame.grid_rowconfigure(0, weight=0)
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
#                             SETTINGS BUTTON                                 #
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
    Opens a Toplevel window to demonstrate a settings screen (no real logic).
    """
    settings_dialog = tk.Toplevel(root)
    settings_dialog.title("InstaVision Settings")
    settings_dialog.state("zoomed")
    settings_dialog.configure(bg=MAIN_BG)

    top_settings_frame = tk.Frame(settings_dialog, bg=MAIN_BG)
    top_settings_frame.place(relx=0, rely=0, relwidth=1, relheight=0.6)

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
        messagebox.showwarning("Settings Header Image", f"Could not load settings header image:\n{e}")

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

    # Example replicate token
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

    # Banned words
    banned_label = tk.Label(
        content_frame,
        text="Banned Words (comma-separated)",
        font=("Arial", 14, "bold"),
        bg=MAIN_BG,
        fg=TEXT_COLOR
    )
    banned_label.grid(row=2, column=0, sticky="e", padx=(30, 10), pady=(5, 3))

    banned_text = tk.Text(content_frame, width=60, height=2, fg="black", bg="white")
    banned_text.grid(row=2, column=1, sticky="w", padx=(0, 30), pady=(5, 3))
    current_banned = config.get("banned_words", [])
    banned_text.insert("1.0", ", ".join(current_banned))

    # History folder
    history_btn_style = ttk.Style()
    history_btn_style.configure(
        "HistoryButton.TButton",
        background="#AAAAFF",
        foreground=IMAGE_BG,
        padding=6,
        font=("Arial", 10, "bold")
    )
    history_btn_style.map(
        "HistoryButton.TButton",
        background=[("active", "#8888DD")],
        foreground=[("active", IMAGE_BG)]
    )

    def open_history_folder():
        folder_path = config.get("history_folder_path", "")
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Invalid or unset history folder path.")
            return
        try:
            os.startfile(folder_path)  # Windows
        except:
            # Mac/Linux fallback
            try:
                subprocess.Popen(["open", folder_path])
            except:
                messagebox.showerror("Error", f"Unable to open: {folder_path}")

    history_btn = ttk.Button(
        content_frame,
        text="History",
        style="HistoryButton.TButton",
        command=open_history_folder
    )
    history_btn.grid(row=3, column=1, sticky="w", padx=(0, 30), pady=(10, 5))

    # Save button
    save_btn_style = ttk.Style()
    save_btn_style.configure(
        "SettingsSave.TButton",
        background=ACCENT_COLOR,
        foreground=IMAGE_BG,
        padding=6,
        font=("Arial", 12, "bold")
    )
    save_btn_style.map(
        "SettingsSave.TButton",
        background=[("active", SECONDARY_COLOR)],
        foreground=[("active", IMAGE_BG)]
    )

    def save_settings():
        config["replicate_api_token"] = replicate_entry.get().strip()

        new_banned = banned_text.get("1.0", tk.END).strip()
        if new_banned:
            config["banned_words"] = [w.strip() for w in new_banned.split(",") if w.strip()]
        else:
            config["banned_words"] = []

        messagebox.showinfo("Settings Saved", "Your settings have been updated!")
        settings_dialog.destroy()

    save_btn = ttk.Button(
        content_frame,
        text="Save Settings",
        style="SettingsSave.TButton",
        command=save_settings
    )
    save_btn.grid(row=4, column=0, columnspan=2, pady=(20, 10))

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
