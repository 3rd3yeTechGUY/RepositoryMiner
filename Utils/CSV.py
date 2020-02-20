def build_csv_from_array(array, separator=","):
    csv = ""
    for element in array:
        csv += str(element) + separator
    return csv
