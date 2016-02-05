from os import rename
from os import remove
from os import path
from csv import reader


def merge_files(merge_file_path, source_file_data, key_column_merge_file, columns):
    bk_file_path = ''.join([merge_file_path, "_bk"])

    if not path.isfile(merge_file_path):
        Exception("File not found!")
        exit()

    c = 0
    while path.isfile(bk_file_path):
        bk_file_path = ''.join([bk_file_path, str(c)])
        c += 1

    rename(merge_file_path, bk_file_path)

    key_column_merge_file_id = -1

    mod_rows_counter = 0
    with open(merge_file_path, 'w') as out_file:
        with open(bk_file_path, 'r') as f:
            csv_reader = reader(f, delimiter=";")
            for k, items in enumerate(csv_reader):
                items = [x.decode('utf-8-sig') for x in items]
                if k is 0:
                    key_column_merge_file_id = items.index(str(key_column_merge_file).decode("utf-8-sig"))
                    new_labels = items
                    for col in columns:
                        new_labels.append(col.decode("utf-8-sig"))

                    new_line = ';'.join(new_labels)
                    out_file.writelines(''.join([new_line, '\n']).encode("utf-8"))

                    continue

                item_merge_key = items[key_column_merge_file_id]
                if item_merge_key in source_file_data:
                    mod_rows_counter += 1
                    for col in columns:
                        items.append(source_file_data[item_merge_key][col.decode("utf-8-sig")])

                new_line = ';'.join(items)
                out_file.writelines(''.join([new_line, '\n']).encode("utf-8"))

    remove(bk_file_path)
    return mod_rows_counter
