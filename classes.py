import csv
from abc import ABC, abstractmethod


class FileWriter(ABC):
    @property
    @abstractmethod
    def file_extension(self):
        pass

    @abstractmethod
    def _write(self, file):
        pass

    def export_data_to_file(self, file_name):
        with open(f"{file_name}.{self.file_extension}", 'w', newline='') as file:
            self._write(file)


class CsvWriter(FileWriter):
    def __init__(self, data, header=None):
        self._data = data
        self._header = header

    def file_extension(self):
        return 'csv'

    def _write(self, file):
        writer = csv.DictWriter(file, fieldnames=self._header)
        writer.writeheader()
        writer.writerows(self._data)



