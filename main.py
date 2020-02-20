
from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary
from pydriller.pydriller import RepositoryMining

repo_summary = RepositorySummary()
repoMiner = RepositoryMiner(RepositoryMining("~/Projects/gecko-dev"), repo_summary)
repoMiner.create_repository_summary()
repoMiner.print_table()
