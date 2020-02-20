from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary
from pydriller import RepositoryMining


repo_summary = RepositorySummary()
repoMiner = RepositoryMiner(RepositoryMining("~/Projects/focus-android"), repo_summary)
repoMiner.create_repository_summary("~/Projects/focus-android")
repoMiner.print_table()
