from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary
from pydriller import RepositoryMining


repo_summary = RepositorySummary()
repoMiner = RepositoryMiner(RepositoryMining(path_to_repo ="~/Projects/focus-android", from_commit=None, to_commit=None), repo_summary)
repoMiner.create_repository_summary("~/Projects/focus-android")
repoMiner.save_table_as_csv("first_try.csv")
