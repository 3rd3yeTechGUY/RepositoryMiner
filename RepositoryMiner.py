from pydriller.metrics.process.method_statement_count import MethodStatementCount
from pydriller.metrics.process.method_author_count import MethodAuthorCount
from pydriller.metrics.process.method_declaration_count import MethodDeclarationCount
from pydriller.metrics.process.method_condition_count import MethodConditionCount

class RepositoryMiner:
    def __init__(self, repository, repository_summary):
        self.__repository = repository
        self.__repository_summary = repository_summary

    def create_repository_summary(self, path_to_repo):
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

            self.__repository_summary.add_commit(commit, method_statement_count, method_author_count, method_declaration_count, method_condition_count)

    def print_table(self):
        self.__repository_summary.print_table()