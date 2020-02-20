class RepositoryMiner:
    def __init__(self, repository, repository_summary):
        self.__repository = repository
        self.__repository_summary = repository_summary

    def create_repository_summary(self):
        for commit in self.__repository.traverse_commits():
            self.__repository_summary.add_commit(commit)

    def print_table(self):
        self.__repository_summary.print_table()