from dataStructures.TableFunctionEntry import TableFunctionEntry


class RepositorySummary:
    def __init__(self):
        self.__commits = []
        self.__table_function_etries = []
        self.__number_of_changes_to_files = {}

    def add_commit(self, commit, method_statement_count, method_author_count, method_declaration_count,
                   method_condition_metrcis):
        self.__commits.append(commit)
        for modification in commit.modifications:
            for method in modification.methods:
                method_name = modification.filename + ":" + method.long_name
                statement_metrics = method_statement_count[method_name]
                author_metrics = method_author_count.get(method_name, 0)
                decl_metrics = method_declaration_count.get(method_name, 0)
                condition_metrics = method_condition_metrcis.get(method_name)
                self.__table_function_etries.append(
                    TableFunctionEntry(commit, modification, method, statement_metrics, author_metrics, decl_metrics,
                                       condition_metrics))

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
