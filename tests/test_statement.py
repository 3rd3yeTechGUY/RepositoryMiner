import unittest
from pydriller import RepositoryMining

from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary


class MyTestCase(unittest.TestCase):
    def test_sum_statement_added(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="../test-repos/method-test", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("../test-repos/method-test")

        table = repo_summary.get_table()
        self.assertTrue(method_in_commit_has_property(table, "6473c2c63ce09cda65bb11cf1f1bf12f31c185a2",
                                                      "Foo.java:Foo::someFunction()", "sum_statement_added", 3))
        self.assertTrue(method_in_commit_has_property(table, "2e533a7e1a0672ffd9f5c3b18dfadd4e34702bd1",
                                                      "Foo.java:Foo::someFunction()", "sum_statement_added", 4))
        self.assertTrue(method_in_commit_has_property(table, "fcd8f8eae9c6d249621271d14376dabdedf843bb",
                                                      "Foo.java:Foo::someFunction3()", "sum_statement_added", 5))
        self.assertTrue(method_in_commit_has_property(table, "e472519835e6f593eb5e169ff22601971f6cf1f6",
                                                      "Foo.java:Foo::someFunction2()", "sum_statement_added", 5))
        self.assertTrue(method_in_commit_has_property(table, "c155c3ee786f40dca1f4e9c59ab989d0b252df80",
                                                      "Foo.java:Foo::someFunction2()", "sum_statement_added", 6))


if __name__ == '__main__':
    unittest.main()


def method_in_commit_has_property(table, commit_hash, method_name, property_name, property_value):
    for entry in table:
        if entry.hash == commit_hash and entry.method_long_name == method_name:
            return getattr(entry, property_name) == property_value
    return False
