import unittest
from pydriller import RepositoryMining

from RepositoryMiner import RepositoryMiner
from dataStructures.Repository_summary import RepositorySummary
from tests.utils import method_in_commit_has_property, method_in_commit_has_properties

NO_COND = {"cond": 0, "else_added": 0, "else_deleted": 0}
NEVER_CHANGE = {"cond": 1, "else_added": 0, "else_deleted": 0}
ONCE_CHANGE = {"cond": 3, "else_added": 0, "else_deleted": 0}
TWICE_CHANGE = {"cond": 5, "else_added": 0, "else_deleted": 0}
TWO_DIFF_CONDITION_ADD = {"cond": 2, "else_added": 0, "else_deleted": 0}
ONE_ADD_ONE_REMOVE = {"cond": 2, "else_added": 1, "else_deleted": 1}
ONE_ELSE_NEVER_CHANGED = {"cond": 1, "else_added": 1, "else_deleted": 0}
ONE_DEL_AFTER = {"cond": 1, "else_added": 1, "else_deleted": 1}
TWO_ELSE_ONE_DELETED = {"cond": 2, "else_added": 2, "else_deleted": 1}
FOUR_ELSE_NO_DEL = {"cond": 4, "else_added": 4, "else_deleted": 0}
FOUR_ELSE_DEL = {"cond": 7, "else_added": 4, "else_deleted": 4}
TOW_ELSEIF = {"cond": 4, "else_added": 2, "else_deleted": 1}


class TestAuthorCount(unittest.TestCase):
    def test_author_count(self):
        repo_summary = RepositorySummary()
        repoMiner = RepositoryMiner(
            RepositoryMining(path_to_repo="../test-repos/method-test5", from_commit=None, to_commit=None), repo_summary)
        repoMiner.create_repository_summary("../test-repos/method-test5", None, None)

        table = repo_summary.get_table()
        self.assertTrue(method_in_commit_has_properties(table, "d8df83f6437a33ded055527b43115ca8f3bc14eb", "Foo.java:Foo::noConditionInMethod()", NO_COND))
        self.assertTrue(method_in_commit_has_properties(table, "d8df83f6437a33ded055527b43115ca8f3bc14eb", "Foo.java:Foo::neverAConditionChange()", NEVER_CHANGE))
        self.assertTrue(method_in_commit_has_properties(table, "1353faee0fc24aa4c4c3e090003b98f7843c6ab0", "Foo.java:Foo::conditionChangedOnce()", ONCE_CHANGE))
        self.assertTrue(method_in_commit_has_properties(table, "aaf2f93fa56cb71e0d6970f8f2d961e6d0128ee4", "Foo.java:Foo::conditionChangedTwice()", TWICE_CHANGE))
        self.assertTrue(method_in_commit_has_properties(table, "3881c503d85a2232a49c95096ca21b84e746fa01", "Foo.java:Foo::twoDifferentConditionStatementsAdded()", TWO_DIFF_CONDITION_ADD))
        self.assertTrue(method_in_commit_has_properties(table, "f29dfb7b552b1194d237098deb766e40f1ac009c", "Foo.java:Foo::oneConditionAddedAndRemovedAfter()", ONE_ADD_ONE_REMOVE))
        self.assertTrue(method_in_commit_has_properties(table, "2965bf66ca6e60988997a2d3680e2543f19ec50e", "Foo.java:Foo::oneElseNeverChanged()", ONE_ELSE_NEVER_CHANGED))
        self.assertTrue(method_in_commit_has_properties(table, "06dfd8d033338b5308a9e71f37df0e75462958d4", "Foo.java:Foo::oneDeletedAfter()", ONE_DEL_AFTER))
        self.assertTrue(method_in_commit_has_properties(table, "7948cbcbf381db5eb36c39029b1a7389e355b3db", "Foo.java:Foo::twoElseOneDeleted()", TWO_ELSE_ONE_DELETED))
        self.assertTrue(method_in_commit_has_properties(table, "0ff25aee20224f71cf0565bcb6f5da5de7514791", "Foo.java:Foo::fourElseAddedNoDeleted()", FOUR_ELSE_NO_DEL))
        self.assertTrue(method_in_commit_has_properties(table, "a5298525a6f98c2e8d090ea5ae73d3676449b97b", "Foo.java:Foo::fourElseAddedAndDeleted()", FOUR_ELSE_DEL))
        self.assertTrue(method_in_commit_has_properties(table, "0093c5ef33d5c8156865cac1faa8e55877046725", "Foo.java:Foo::twoElseIfAddedOneDeleted( int a)", TOW_ELSEIF))

if __name__ == '__main__':
    unittest.main()
