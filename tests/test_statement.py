import unittest
from pydriller import RepositoryMining

from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary
from tests.utils import method_in_commit_has_property, method_in_commit_has_properties

STMT_ADD = "sum_stmt_added"
MAX_STMT_ADD = "max_stmt_added"


class MyTestCase(unittest.TestCase):
    def test_sum_statement_added(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="../test-repos/method-test", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("../test-repos/method-test", None, None)

        table = repo_summary.get_table()
        self.assertTrue(method_in_commit_has_property(table, "6473c2c63ce09cda65bb11cf1f1bf12f31c185a2",
                                                      "Foo.java:Foo::someFunction()", STMT_ADD, 3))
        self.assertTrue(method_in_commit_has_property(table, "2e533a7e1a0672ffd9f5c3b18dfadd4e34702bd1",
                                                      "Foo.java:Foo::someFunction()", STMT_ADD, 4))
        self.assertTrue(method_in_commit_has_property(table, "c155c3ee786f40dca1f4e9c59ab989d0b252df80",
                                                      "Foo.java:Foo::someFunction2()", STMT_ADD, 6))

    def test_max_stmt_added(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="../test-repos/method-test", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("../test-repos/method-test", None, None)

        table = repo_summary.get_table()
        self.assertTrue(method_in_commit_has_property(table, "6473c2c63ce09cda65bb11cf1f1bf12f31c185a2",
                                                      "Foo.java:Foo::someFunction()", MAX_STMT_ADD, 3))
        self.assertTrue(method_in_commit_has_property(table, "2e533a7e1a0672ffd9f5c3b18dfadd4e34702bd1",
                                                      "Foo.java:Foo::someFunction()", MAX_STMT_ADD, 3))
        self.assertTrue(method_in_commit_has_property(table, "c155c3ee786f40dca1f4e9c59ab989d0b252df80",
                                                      "Foo.java:Foo::someFunction2()", MAX_STMT_ADD, 3))

    def test_last_commit(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="../test-repos/method-test", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("../test-repos/method-test", None, None)

        table = repo_summary.get_table()

        EXPECTED_SIMPLE = {"sum_stmt_added": 6,
                           "max_stmt_added": 3,
                           "avg_stmt_added": 1.2,
                           "sum_stmt_deleted": 3,
                           "max_stmt_deleted": 1,
                           "avg_stmt_deleted": 0.6,
                           "method_histories": 5,
                           "churn": 3,
                           "max_churn": 3,
                           "avg_churn": 0.6}

        self.assertTrue(method_in_commit_has_properties(table, "c155c3ee786f40dca1f4e9c59ab989d0b252df80",
                                                        "Foo.java:Foo::someFunction()", EXPECTED_SIMPLE))
        self.assertTrue(method_in_commit_has_properties(table, "c155c3ee786f40dca1f4e9c59ab989d0b252df80",
                                                        "Foo.java:Foo::someFunction2()", EXPECTED_SIMPLE))
        self.assertTrue(method_in_commit_has_properties(table, "c155c3ee786f40dca1f4e9c59ab989d0b252df80",
                                                        "Foo.java:Foo::someFunction3()", EXPECTED_SIMPLE))


if __name__ == '__main__':
    unittest.main()
