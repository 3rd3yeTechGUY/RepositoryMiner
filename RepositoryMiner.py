import csv

from pydriller.metrics.process.method_statement_count import MethodStatementCount
from pydriller.metrics.process.method_author_count import MethodAuthorCount
from pydriller.metrics.process.method_declaration_count import MethodDeclarationCount
from pydriller.metrics.process.method_condition_count import MethodConditionCount

from dataStructures.TableFunctionEntry import TableFunctionEntry


class RepositoryMiner:
    def __init__(self, repository, repository_summary):
        self.__repository = repository
        self.__repository_summary = repository_summary
        self.commits_added = 0

    def create_repository_summary(self, path_to_repo):
        try:
            for commit in self.__repository.traverse_commits():
                method_statement_count = MethodStatementCount(path_to_repo=path_to_repo,
                                                              from_commit=None,
                                                              to_commit=commit.hash).count()
                method_author_count = MethodAuthorCount(path_to_repo=path_to_repo,
                                                        from_commit=None,
                                                        to_commit=commit.hash).count()
                method_declaration_count = MethodDeclarationCount(path_to_repo=path_to_repo,
                                                                  from_commit=None,
                                                                  to_commit=commit.hash).count()
                method_condition_count = MethodConditionCount(path_to_repo=path_to_repo,
                                                              from_commit=None,
                                                              to_commit=commit.hash).count()

                self.__repository_summary.add_commit(commit, method_statement_count, method_author_count,
                                                     method_declaration_count, method_condition_count)
                self.commits_added += 1
                print("{}: Commit {} added".format(self.commits_added, commit.hash));
        except:
            print("Error happend")
            self.print_table()
            print("The table upto this point has been printed")

    def print_table(self):
        self.__repository_summary.print_table()

    def save_table_as_csv(self, file_name):
        with open(file_name, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(TableFunctionEntry.get_csv_header())
            for row in self.__repository_summary.get_table_entries():
                csv_writer.writerow(row.get_array_of_metrics())