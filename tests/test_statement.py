import unittest
from pydriller import RepositoryMining

from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary


class MyTestCase(unittest.TestCase):
    def test_simple(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="~/Projects/focus-android", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("~/Projects/focus-android")

        table = repo_summary.get_table()
        self.assertTrue(method_in_commit_has_property(table, "6473c2c63ce09cda65bb11cf1f1bf12f31c185a2",
                                              "Foo.java:Foo::someFunction()", "sum_statement_added", 3))


if __name__ == '__main__':
    unittest.main()


def method_in_commit_has_property(table, commit_hash, method_name, property_name, property_value):
    for entry in table:
        if entry.hash == commit_hash and entry.method_long_name == method_name:
            return getattr(entry, property_name) == property_value
    return False

