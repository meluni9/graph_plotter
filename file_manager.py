import re
import numpy as np
from tkinter import filedialog

class FileManager:
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path:
            return None, None
        try:
            with open(file_path, 'r') as file:
                data = file.readlines()

            if self.is_xy_pair_format(data):
                return self.parse_xy_pairs(data)
            else:
                return self._parse_csv_or_txt(data)

        except Exception as e:
            raise ValueError(f"Could not load file: {e}")

    def is_xy_pair_format(self, data):
        for line in data:
            if self._match_format(line):
                return True
        return False

    def parse_xy_pairs(self, data):
        x_values = []
        y_values = []
        for line in data:
            match = self._match_format(line)
            if match:
                x_values.append(float(match.group(1)))
                y_values.append(float(match.group(2)))
            else:
                raise ValueError(f"Invalid line format: {line.strip()}")
        return np.array(x_values), np.array(y_values)

    @staticmethod
    def _match_format(line):
        return re.match(r'\(\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*\)', line.strip())

    @staticmethod
    def _parse_csv_or_txt(data):
        try:
            parsed_data = np.loadtxt(data, delimiter=',')
            if parsed_data.shape[1] != 2:
                raise ValueError("File must contain exactly two columns for x and y values.")
            return parsed_data[:, 0], parsed_data[:, 1]
        except Exception as e:
            raise ValueError(f"Could not parse CSV or TXT file: {e}")

    @staticmethod
    def _export_data(segments):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("CSV files", "*.csv"),
                                                            ("All files", "*.*")])
        if not file_path:
            return
        with open(file_path, 'w') as file:
            for x_seg, y_seg in segments:
                for x, y in zip(x_seg, y_seg):
                    file.write(f"{x},{y}\n")
