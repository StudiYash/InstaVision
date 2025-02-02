# Support Files for *InstaVision.py*

## Updating the Path for **HIGHSENS 400.otf** and **instavision_metrics.xlxs** and **requirements.txt** in *InstaVision.py*

Hello, brilliant developer! If you’ve just created (or moved) the **HIGHSENS 400.otf** and **instavision_metrics.xlxs** and **requirements.txt** and need to ensure our main `InstaVision.py` file knows where to find it, follow these friendly instructions.

---

## 1. Locate the `InstaVision.py` File
- Head over to your project directory.
- Open up the **`InstaVision.py`** file in your favorite code editor (VSCode, PyCharm, or maybe good ol’ Notepad++).

---

## 2. Find the Folder Path Variable
 - Somewhere in `InstaVision.py`, you'll find a line or variable that specifies the path for HIGHSENS 400. It might look like:
    ```python
    font = ImageFont.truetype("HIGHSENS 400.otf Path", font_size)
    ```

 - Somewhere in `InstaVision.py`, you'll find a line or variable that specifies the path for instavision_metrics. It might look like:
    ```python
    EXCEL_FILE_PATH = "instavision_metrics.xlsx Path"
    ```  

 - To run `InstaVision.py` successfully on your system, initially locate the file **requirements.txt** and then open the terminal on your system. On terminal you can run the following command:
    ```python
    pip install requirements.txt
    ```