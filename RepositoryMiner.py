import csv
from pydriller import RepositoryMining
from pydriller.domain.commit import ModificationType



from dataStructures.TableFunctionEntry import TableFunctionEntry

SUM_ADDED = "sum_statement_added"


class RepositoryMiner:
    def __init__(self, repository, repository_summary):
        self.__repository = repository
        self.__repository_summary = repository_summary
        self.commits_added = 0
        self.methods = {}

    def create_repository_summary(self, path_to_repo):
        for method_dto in self.__get_methods(path_to_repo, None, None):
            metrics = self.__generate_metrics(method_dto)
            self.__repository_summary.add_method(method_dto, metrics)
            self.commits_added += 1
            print("{}: Commit {} added".format(self.commits_added, method_dto.commit.hash))

    def print_table(self):
        self.__repository_summary.print_table()

    def save_table_as_csv(self, file_name):
        with open(file_name, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(TableFunctionEntry.get_csv_header())
            for row in self.__repository_summary.get_table_entries():
                csv_writer.writerow(row.get_array_of_metrics())

    def __get_methods(self, path_to_repo, from_commit, to_commit):
        renamed_files = {}

        for commit in RepositoryMining(path_to_repo=path_to_repo,
                                       from_commit=from_commit,
                                       to_commit=to_commit,
                                       reversed_order=False).traverse_commits():

            for modified_file in commit.modifications:

                file_path = renamed_files.get(modified_file.new_path, modified_file.new_path)

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = file_path

                if modified_file.change_type == ModificationType.DELETE:
                    continue

                file_name = file_path.split("/")[-1]

                for method in modified_file.methods:
                    method_long_name = RepositoryMiner.__generate_method_long_name(file_name, method.long_name)
                    yield MethodDTO(modified_file, method, method_long_name, commit)

    @staticmethod
    def __generate_method_long_name(file_name, method_long_name):
        return file_name + ":" + method_long_name

    def __generate_metrics(self, method_dto):
        method_metrics = self.methods.get(method_dto.method_long_name, MethodMetric(method_dto.method_long_name))
        new_metrics = self.__update_metrics(method_metrics, method_dto)
        self.methods[method_dto.method_long_name] = method_metrics
        return new_metrics

    def __update_metrics(self, method_metrics, method_dto):
        try:
            old_metrics = method_metrics.metrics[-1]
        except IndexError:
            old_metrics = RepositoryMiner.__generate_empty_metrics()
        new_metrics = old_metrics.copy()
        new_metrics[SUM_ADDED] = old_metrics[SUM_ADDED] + method_dto.method.statements_added
        new_metrics["hash"] = method_dto.commit.hash
        new_metrics["name"] = method_dto.method_long_name
        method_metrics.metrics.append(new_metrics)
        return new_metrics

    @staticmethod
    def __generate_empty_metrics():
        return {SUM_ADDED: 0}


class MethodMetric:
    def __init__(self, method_name):
        self.method_name = method_name
        self.metrics = []


class MethodDTO:
    def __init__(self, modified_file, method, method_long_name, commit):
        self.modified_file = modified_file
        self.method = method
        self.method_long_name = method_long_name
        self.commit = commit
