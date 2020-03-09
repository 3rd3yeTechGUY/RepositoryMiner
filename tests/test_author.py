import unittest
from pydriller import RepositoryMining

from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary
from tests.utils import method_in_commit_has_property


class TestAuthorCount(unittest.TestCase):
    def test_author_count(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="../test-repos/method-test3", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("../test-repos/method-test3", None, None)

        table = repo_summary.get_table()
        self.assertTrue(method_in_commit_has_property(table, "d992d74a535b4479a86df99cc041b55e38065b2e",
                                                      "Foo.java:Foo::methodOnlyChangedOne()", "authors", 1))
        self.assertTrue(method_in_commit_has_property(table, "bd3291339c9f826bb406288e4ebbc714dd8ae0e9",
                                                      "Foo.java:Foo::methodChangedByTwo()", "authors", 2))
        self.assertTrue(method_in_commit_has_property(table, "6b1293522a60be806c3fc6fd27edf24ebed3655c",
                                                      "Foo.java:Foo::methodChangedByThree()", "authors", 3))
        self.assertTrue(method_in_commit_has_property(table, "03196e778184de0bd53dd4f838861082ae7c245b",
                                                      "Foo.java:Foo::methodChangedByTwoWithSameNameButDifferentEmail()", "authors", 2))
        self.assertTrue(method_in_commit_has_property(table, "dafb1d9ee5e654474a38786587ad7ba8d49b90df",
                                                      "Foo.java:Foo::methodChangedBySameAuthorTwice()", "authors", 2))
        self.assertTrue(method_in_commit_has_property(table, "dafb1d9ee5e654474a38786587ad7ba8d49b90df",
                                                      "Foo.java:Foo::methodChangedByTwoDifferentTwice()", "authors", 2))


if __name__ == '__main__':
    unittest.main()

