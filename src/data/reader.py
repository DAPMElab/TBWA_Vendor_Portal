
import csv
import os
this_dir = os.path.dirname(__file__)

data_paths = {
    'diverse': os.path.join(this_dir, 'assets/tbwa/diverse_vendors_list.csv')
}


def get_data(dataset, path_to_data=None):
    """ Returns the columns and a list of data with the specified dataset """
    # TODO: redesign when db is implemented to insert row by row

    if not path_to_data:
        if dataset not in data_paths:
            raise Exception('Invalid dataset')
        else:
            path_to_data = data_paths[dataset]


    with open(path_to_data, 'rb') as f:
        data_reader = csv.reader(f)
        columns = data_reader.next()
        return columns, [row for row in data_reader]


