import csv

class FileExporter:
    def __init__(self,file_path = None):
        if file_path == None:
            self.file_path = input("Which path do you want to export your file to: ")
        else:
            self.file_path = file_path

    def export_data(self, data, header):
        try:
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=header)

                # Write the header
                writer.writeheader()

                # Write all data rows
                writer.writerows(data)
            print("Data sucessfully exported to:", self.file_path)
        except Exception as e:
            print("Error exporting data:", e)


