import tkinter as tk
from PIL import Image, ImageTk

# Path to the InstaVision logo image
INSTAVISION_LOGO_PATH = "InstaVision_Logo.png"  # Replace with the actual path to your logo

def display_modified_window():
    """Display a maximized window with a logo and two hoverable buttons."""
    root = tk.Tk()
    # Maximize the window (not full-screen)
    root.state("zoomed")

    # Configure window background
    root.configure(bg="#002b36")  # Dark blue background

    # -- Border frame for the logo --
    BORDER_WIDTH = 10
    logo_border_frame = tk.Frame(root, bg="#2A2A3B", padx=BORDER_WIDTH, pady=BORDER_WIDTH)
    logo_border_frame.pack(fill="both", expand=True)

    # Load and display the InstaVision logo
    try:
        # Temporarily withdraw the window to get proper screen dimensions
        root.withdraw()

        # Update geometry info to ensure .winfo_screenwidth() / .winfo_screenheight() is accurate
        root.update_idletasks()

        # Show it again (maximized)
        root.deiconify()

        # Calculate available size for the image
        # (We’ll reserve some space for the buttons at the bottom)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # For example, reserve ~20% height for the button area
        available_height_for_logo = int(screen_height * 0.75)

        logo_img = Image.open(INSTAVISION_LOGO_PATH)
        logo_img = logo_img.resize(
            (screen_width - 2 * BORDER_WIDTH, available_height_for_logo - 2 * BORDER_WIDTH),
            Image.Resampling.LANCZOS,
        )
        logo_photo = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(logo_border_frame, image=logo_photo, bg="#2A2A3B")
        logo_label.image = logo_photo  # Keep reference to avoid garbage collection
        logo_label.pack(fill="both", expand=True)
    except Exception as e:
        print(f"Error loading InstaVision Logo: {e}")
        root.destroy()
        return

    # -- Frame for the buttons at the bottom --
    button_frame = tk.Frame(root, bg="#002b36")
    button_frame.pack(fill="both", expand=False)

    # Define normal and hover colors
    normal_bg = "#268bd2"
    hover_bg = "#ec1444"
    text_color = "#ffffff"

    # Define hover functions
    def on_enter(e):
        e.widget["bg"] = hover_bg

    def on_leave(e):
        e.widget["bg"] = normal_bg

    # Common style for both buttons
    button_style = {
        "font": ("Arial", 16, "bold"),
        "fg": text_color,
        "bg": normal_bg,
        "relief": tk.RAISED,
        "bd": 2,
        "width": 15,  # Adjust the width as per your preference
        "height": 2
    }

    # Create the two buttons side by side
    image_gen_button = tk.Button(button_frame, text="Image Generation", **button_style)
    image_edit_button = tk.Button(button_frame, text="Image Editing", **button_style)

    # Bind hover events
    image_gen_button.bind("<Enter>", on_enter)
    image_gen_button.bind("<Leave>", on_leave)
    image_edit_button.bind("<Enter>", on_enter)
    image_edit_button.bind("<Leave>", on_leave)

    # Use pack or grid to place them horizontally and evenly
    image_gen_button.pack(side=tk.LEFT, expand=True, padx=20, pady=20)
    image_edit_button.pack(side=tk.LEFT, expand=True, padx=20, pady=20)

    # Run the Tkinter event loop
    root.mainloop()

# Run the modified window
display_modified_window()