# import ftfy
import re
import csv


def remove_broken_lines():  # old_file, new_file, delimiter, delete=False):
    """
    This creates new csv documents and remove broken lines from the orginal
    document it receieved the data from.
    If delete is set to True it deletes the original document it got the data
    from
    """
    with open('book-data/BX-Book-Ratings.csv', 'r', encoding="latin-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0

        # read rwos in the csv file
        for row in csv_reader:
            if line_count == 0:
                fieldnames = list(row)

            try:
                int(row['ISBN'])

                # write proper values into new csv document
                with open('book-data/FX-Book-Ratings.csv', 'a') as fixed_csv:
                    writer = csv.DictWriter(fixed_csv, fieldnames=fieldnames, delimiter=',')
                    if line_count == 0:
                        writer.writeheader()
                    writer.writerow(row)

            except Exception as e:
                continue

            line_count += 1
    return line_count


def properly_encode_lines():
    """
    Creates a new csv document and encodes lines properly if possible otherwise it
    does not include it in the new csv document.
    It deletes the previous files if delete is set to True
    """
    with open('book-data/BX-Books.csv', 'r', encoding="latin-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0

        # read rwos in the csv file
        for row in csv_reader:
            try:
                if line_count == 0:
                    fieldnames = list(row)

                    # remove urls from fieldnames
                    fieldnames = [name for name in fieldnames if not re.search('Image', name)]
                stup = re.search('amp;', row['Publisher'])

                if stup:
                    row['Publisher'] = row['Publisher'].replace('amp;', '').strip()

            except UnicodeDecodeError:
                continue

            try:
                int(row['ISBN'])

                # check if year is valid
                if re.search('\d{4}', row['Year-Of-Publication']):

                    # delete keys and values from csv rows
                    row_keys = [keys for keys in row.keys() if keys not in fieldnames]
                    for keys in row_keys:
                        del row[keys]

                    # write proper values into new csv document
                    with open('book-data/FX-Books.csv', 'a') as fixed_csv:
                        writer = csv.DictWriter(fixed_csv, fieldnames=fieldnames, delimiter=',')

                        if line_count == 0:
                            writer.writeheader()

                        writer.writerow(row)

            except Exception as e:
                continue

            line_count += 1

        return line_count


def remove_null_rows():
    """
    Set rows that have NULL values/empty values to None for easier interaction with
    pandas for training datasets
    """
    with open('book-data/BX-Users.csv', 'r', encoding="latin-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0

        # read rwos in the csv file
        for row in csv_reader:
            if line_count == 0:
                fieldnames = list(row)

            try:
                int(row['User-ID'])

                if row['Age'] == 'NULL':
                    row['Age'] = None

                stup = re.search('n/a,', row['Location'])
                if stup:
                    row['Location'] = row['Location'].replace('n/a,', '').strip()

            except Exception as e:
                continue

            try:
                with open('book-data/FX-Users.csv', 'a') as fixed_csv:
                    writer = csv.DictWriter(fixed_csv, fieldnames=fieldnames, delimiter=',')

                    if line_count == 0:
                        writer.writeheader()
                    writer.writerow(row)

            except Exception as e:
                continue

            line_count += 1
        return line_count


if __name__ == '__main__':
    valid_users = remove_null_rows()
    print(f'valid users obtained is {valid_users}')

    valid_books_count = properly_encode_lines()
    print(f'valid books left is {valid_books_count}')

    valid_rating_count = remove_broken_lines()
    print(f'valid ratings left is {valid_rating_count}')
