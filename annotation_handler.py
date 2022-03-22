import csv
import os
import shutil

# -- -- -- DATA FILE INFO
DATA_FOLDER = "./data"
HEADER = ['image_id', 'annotations']
ID_COLUMN_NAME = 'image_id'


# -- -- CREATE DATA FILE
def create_data_file(file_path):
    # ensure the DATA_FOLDER exists
    try:
        os.makedirs(DATA_FOLDER)
    except OSError:
        pass
    # ensure the DATA_FILE exists
    if not os.path.isfile(file_path):
        file = open(file_path, 'a+')
        writer = csv.writer(file)
        writer.writerow(HEADER)
        file.close()
    else:
        pass
        # TODO check header exists and if not add header to the file
        # TODO check header matches the header and if not raise error


class AnnotationHandler:
    def __init__(self, user_id):
        self.user_id = user_id

        data_file = str(user_id)+"_"+"annotations.csv"
        temp_file = str(user_id)+"_"+"annotations_temp.csv"
        file_path = os.path.join(DATA_FOLDER, data_file)
        temp_file_path = os.path.join(DATA_FOLDER, temp_file)
        self.file_path = file_path
        self.temp_file_path = temp_file_path

        create_data_file(self.file_path)

    def _add_row(self, image_id, annotations):
        inp = open(self.file_path, 'a+')
        writer = csv.writer(inp)
        writer.writerow([image_id, annotations])
        inp.close()

    def delete_row(self, image_id):
        with open(self.file_path, 'r') as inp, open(self.temp_file_path, 'w+') as temp:
            csv_reader = csv.DictReader(inp)
            csv_writer = csv.DictWriter(temp, csv_reader.fieldnames)
            csv_writer.writeheader()
            for row in csv_reader:
                if not (row['image_id'] == image_id):
                    csv_writer.writerow(row)
            inp.close()
            temp.close()
        shutil.move(self.temp_file_path, self.file_path)

    def update_row(self, image_id, annotations):
        self.delete_row(image_id)
        self._add_row(image_id, annotations)

    def get_row(self, column_id):
        with open(self.file_path, 'r') as inp:
            csv_reader = csv.DictReader(inp)
            for row in csv_reader:
                if row[ID_COLUMN_NAME] == column_id:
                    inp.close()
                    return row
        inp.close()
        return None
