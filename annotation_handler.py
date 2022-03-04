import csv
import os
import shutil

# -- -- -- DATA FILE INFO
DATA_FOLDER = "./data"
DATA_FILE = "annotations.csv"
HEADER = ['image_id', 'annotations']

FILE_PATH = os.path.join(DATA_FOLDER, DATA_FILE)
TEMP_FILE_PATH = os.path.join(DATA_FOLDER, 'temp.csv')


# -- -- CREATE DATA FILE
def create_data_file():
    # ensure the DATA_FOLDER exists
    try:
        os.makedirs(DATA_FOLDER)
    except OSError:
        pass
    # ensure the DATA_FILE exists
    if not os.path.isfile(FILE_PATH):
        file = open(FILE_PATH, 'a+')
        writer = csv.writer(file)
        writer.writerow(HEADER)
        file.close()
    # TODO check header exists and if not add header to the file


def _add_row(image_id, annotations):
    inp = open(FILE_PATH, 'a+')
    writer = csv.writer(inp)
    writer.writerow([image_id, annotations])
    inp.close()


def delete_row(image_id):
    with open(FILE_PATH, 'r') as inp, open(TEMP_FILE_PATH, 'w+') as temp:
        csv_reader = csv.DictReader(inp)
        csv_writer = csv.DictWriter(temp, csv_reader.fieldnames)
        csv_writer.writeheader()
        for row in csv_reader:
            if row['image_id'] != image_id:
                csv_writer.writerow(row)
        inp.close()
        temp.close()
    shutil.move(TEMP_FILE_PATH, FILE_PATH)


def update_row(image_id, annotations):
    delete_row(image_id)
    _add_row(image_id, annotations)


def get_row(image_id):
    with open(FILE_PATH, 'r') as inp:
        csv_reader = csv.DictReader(inp)
        for row in csv_reader:
            if row['image_id'] == image_id :
                inp.close()
                return row['annotations']
    inp.close()
    return "[]"


create_data_file()
