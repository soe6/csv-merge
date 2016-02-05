import csv


def csv2list(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        for row in csv.DictReader(csv_file, delimiter=";"):
            map(lambda x: x.encode("utf-8-sig"), row)
            data.append(row)

    return data


def csv2dic(file_path, key_col=None):
    data = {}
    with open(file_path, 'r') as csv_file:
        for row in csv.DictReader(csv_file, delimiter=";"):
            if key_col is None:
                key_col = row.keys()[0]

            data[row[key_col].decode("utf-8-sig")] = {col.decode("utf-8-sig"): val.decode("utf-8-sig")
                                                      for col, val in row.iteritems()}
    return data


def csv_save(data, file_path, field_names):
    with open(file_path, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter=";")
        writer.writeheader()

        for key, row in data.iteritems():
            out = {}
            for k, v in row.iteritems():
                if k in field_names:
                    if type(v) is unicode:
                        out[k] = v.encode("utf-8")
                    else:
                        out[k] = repr(v).replace(".", ",")

            writer.writerow(out)


def csv_get_labels(file_path):
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f, delimiter=";")
        for labels in csv_reader:
            return labels
    return []
