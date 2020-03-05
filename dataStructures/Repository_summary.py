from dataStructures.TableFunctionEntry import TableFunctionEntry


class RepositorySummary:
    def __init__(self):
        self.__commits = []
        self.__table_function_etries = []
        self.__number_of_changes_to_files = {}
        self.methods = {}

    def add_method(self, method_dto, metrics):
        self.__table_function_etries.append(TableFunctionEntry(method_dto, metrics))

    def __update_number_changes_files(self, file_list):
        for file in file_list:
            if file in self.__number_of_changes_to_files.keys():
                self.__number_of_changes_to_files[file] += 1
            else:
                self.__number_of_changes_to_files[file] = 1

    def print_commits(self):
        for commit in self.__commits:
            print("{}, {}".format(commit.hash, commit.author.name))

    def print_table(self):
        for table_function_entry in self.__table_function_etries:
            print(table_function_entry.get_as_csv())

    def get_table(self):
        return self.__table_function_etries

    def get_table_entries(self):
        for table_function_entry in self.__table_function_etries:
            yield table_function_entry
