from tkinter import filedialog
import numpy as np

class FileLoader:
    @staticmethod
    def load_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path:
            return None, None
        try:
            data = np.loadtxt(file_path, delimiter=',')
            if data.shape[1] != 2:
                raise ValueError("File must contain exactly two columns for x and y values.")
            return data[:, 0], data[:, 1]
        except Exception as e:
            raise ValueError(f"Could not load file: {e}")
