import unittest
from pydriller import RepositoryMining

from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary
from tests.utils import method_in_commit_has_property


class TestAuthorCount(unittest.TestCase):
    def test_is_bug(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="../test-repos/bug-test", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("../test-repos/bug-test", None, None)

        table = repo_summary.get_table()
        self.assertTrue(method_in_commit_has_property(table, "5447e9ea765dc239c2b36b8460d772a7ace84d01","Foo.java:Foo::someFunction()", "is_bug", False))
        self.assertTrue(method_in_commit_has_property(table, "5447e9ea765dc239c2b36b8460d772a7ace84d01","Foo.java:Foo::someFunction2()", "is_bug", False))
        self.assertTrue(method_in_commit_has_property(table, "5447e9ea765dc239c2b36b8460d772a7ace84d01","Foo.java:Foo::someFunction3()", "is_bug", False))
        self.assertTrue(method_in_commit_has_property(table, "404af96f857d98b619354724ed2d929d5ed665ff","Foo.java:Foo::someFunction3()", "is_bug", True))
        self.assertTrue(method_in_commit_has_property(table, "898c16bda929a7e8c2c16727abf506ff6b871856","Foo.java:Foo::someFunction2()", "is_bug", True))
        self.assertTrue(method_in_commit_has_property(table, "5e1a403401b5add14073e6e20bf601935fa86c50","Foo.java:Foo::someFunction3()", "is_bug", False))
        self.assertTrue(method_in_commit_has_property(table, "69ae7a00f07ab9e446895a4754f8e096c18508c6","Foo.java:Foo::someFunction2()", "is_bug", False))

    def test_bug_fix(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="../test-repos/bug-test", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("../test-repos/bug-test", None, None)

        table = repo_summary.get_table()
        self.assertTrue(method_in_commit_has_property(table, "5447e9ea765dc239c2b36b8460d772a7ace84d01",
                                                      "Foo.java:Foo::someFunction()", "is_bug_fix", False))
        self.assertTrue(method_in_commit_has_property(table, "5447e9ea765dc239c2b36b8460d772a7ace84d01",
                                                      "Foo.java:Foo::someFunction2()", "is_bug_fix", False))
        self.assertTrue(method_in_commit_has_property(table, "5447e9ea765dc239c2b36b8460d772a7ace84d01",
                                                      "Foo.java:Foo::someFunction3()", "is_bug_fix", False))
        self.assertTrue(method_in_commit_has_property(table, "404af96f857d98b619354724ed2d929d5ed665ff",
                                                      "Foo.java:Foo::someFunction3()", "is_bug_fix", False))
        self.assertTrue(method_in_commit_has_property(table, "898c16bda929a7e8c2c16727abf506ff6b871856",
                                                      "Foo.java:Foo::someFunction2()", "is_bug_fix", False))
        self.assertTrue(method_in_commit_has_property(table, "5e1a403401b5add14073e6e20bf601935fa86c50",
                                                      "Foo.java:Foo::someFunction3()", "is_bug_fix", True))
        self.assertTrue(method_in_commit_has_property(table, "69ae7a00f07ab9e446895a4754f8e096c18508c6",
                                                      "Foo.java:Foo::someFunction2()", "is_bug_fix", True))


if __name__ == '__main__':
    unittest.main()

