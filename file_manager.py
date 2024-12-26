import numpy as np
from tkinter import filedialog


class FileManager:
    def load_file(self):
        file_path = self.get_file_path()
        if not file_path:
            return None, None
        try:
            with open(file_path, 'r') as file:
                data = file.readlines()
            return self._parse_csv_or_txt(data)

        except Exception as e:
            raise ValueError(f"Could not load file: {e}")

    def _parse_csv_or_txt(self, data):
        try:
            parsed_data = np.loadtxt(data, delimiter=',')
            if parsed_data.shape[1] != 2:
                raise ValueError("File must contain exactly two columns for x and y values.")
            return parsed_data[:, 0], parsed_data[:, 1]
        except Exception as e:
            raise ValueError(f"Could not parse CSV or TXT file: {e}")

    def _export_file(self, segments):
        file_path = self.get_file_path()
        if not file_path:
            return
        with open(file_path, 'w') as file:
            for x_seg, y_seg in segments:
                for x, y in zip(x_seg, y_seg):
                    file.write(f"{x},{y}\n")

    def get_file_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("CSV files", "*.csv"),
                                                            ("All files", "*.*")])
        return file_path
