import unittest
from pydriller import RepositoryMining

from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary
from tests.utils import method_in_commit_has_property

DECL = "decl_changes"


class TestMethodDeclaration(unittest.TestCase):
    def test_declaration_change(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="../test-repos/method-test4", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("../test-repos/method-test4", None, None)

        table = repo_summary.get_table()
        self.assertTrue(method_in_commit_has_property(table, "11c9b69821df256de46ad6d497bed021bb14269b",
                                                      "Foo.java:Foo::methodNameChangedOnce1()", DECL, 2))
        self.assertTrue(method_in_commit_has_property(table, "50f9a5f4094085b360f80dcb3068c7339590c928",
                                                      "Foo.java:Foo::methodNameAndRetrurnTypeChangeOnceTogether1()", DECL, 2))
        self.assertTrue(method_in_commit_has_property(table, "11cf4dcebe1971f480924fd9f670508dc23a704a",
                                                      "Foo.java:Foo::methodDeclarationNeverChanged()", DECL, 1))

        self.assertTrue(method_in_commit_has_property(table, "6987405bfee4de50d2316f817e41b4ad669af66f",
                                                      "Foo.java:Foo::methodNameAndRetrurnTypeChangeOnceSeperate1()", DECL, 3))

        self.assertTrue(method_in_commit_has_property(table, "52ae7f81f5cb8b06b01b33ac2e301dc9e5d6cf60",
                                                      "Foo.java:Foo::methodVisibilityChangedOnce()", DECL, 2))

        self.assertTrue(method_in_commit_has_property(table, "bed7e7dab4f3ee5136077ee8a72bbd0f3904f56d",
                                                      "Foo.java:Foo::methodChangedThreeTimes3()", DECL, 4))


if __name__ == '__main__':
    unittest.main()

