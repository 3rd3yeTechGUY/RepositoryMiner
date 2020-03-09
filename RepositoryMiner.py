import csv
import re

from pydriller import RepositoryMining, GitRepository
from pydriller.domain.commit import ModificationType

from Utils.DiffParser import get_changed_lines_between, get_lines_between
from dataStructures.TableFunctionEntry import TableFunctionEntry

SUM_ADDED = "sum_statement_added"
MAX_ADDED = "max_statement_added"
AVG_ADDED = "average_statement_added"
NUM_MODIFIED = "method_histories"
SUM_DELETED = "sum_statement_deleted"
MAX_DELETED = "max_statement_deleted"
AVG_DELETED = "average_statement_deleted"
CHURN = "churn"
AVG_CHURN = "average_churn"
MAX_CHURN = "max_churn"
DECL = "decl_changes"
COND_CHANGES = "condition_changes"
ELSE_ADD = "else_added"
ELSE_DEL = "else_removed"
BUG_FIX = "is_bug_fix"
IS_BUG = "is_bug"

REGEX_CONDITION = r"(if\s*\(.+\))"
REGEX_ELSE_ADD = r"\+.*else\s*(if\s*\(.+\))*{"
REGEX_ELSE_DELETE = r"-.*else\s*(if\s*\(.+\))*{"

BUG_FIX_STRINGS = ["fix", "repair", "error", "avoid", "bug ", "issue ", "#", "exception"]


class RepositoryMiner:
    def __init__(self, repository, repository_summary):
        self.__repository = repository
        self.__repository_summary = repository_summary
        self.commits_added = 0
        self.methods = {}

    def create_repository_summary(self, path_to_repo, from_commit, to_commit):
        bug_introducing_commit_hashes = {}
        for method_dto in self.__get_methods(path_to_repo, from_commit, to_commit):
            try:
                if self.__is_message_bugfix(method_dto.commit.msg):
                    bug_introducing = GitRepository(path_to_repo).get_commits_last_modified_lines(method_dto.commit)
                    for file in bug_introducing:
                        previous = bug_introducing_commit_hashes.get(file, set())
                        for commits in bug_introducing[file]:
                            previous.add(commits)
                        bug_introducing_commit_hashes[file] = previous
                metrics = self.__generate_metrics(method_dto)
                self.__repository_summary.add_method(method_dto, metrics)
                self.commits_added += 1
                print("{}: Commit {} added".format(self.commits_added, method_dto.commit.hash))
            except NoChangeException:
                print("No Change")
            except Exception as err:
                print(err)
        print("Adding Bugs")
        for table_entry in self.__repository_summary.get_table_entries():
            if table_entry.hash in bug_introducing_commit_hashes.get(table_entry.file_name, set()):
                print("Bug in commit {} found".format(table_entry.hash))
                table_entry.is_bug = True

    def print_table(self):
        self.__repository_summary.print_table()

    def save_table_as_csv(self, file_name):
        with open(file_name, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(TableFunctionEntry.get_csv_header())
            for row in self.__repository_summary.get_table_entries():
                csv_writer.writerow(row.get_array_of_metrics())

    def __get_methods(self, path_to_repo, from_commit, to_commit):
        renamed_files = {}

        for commit in RepositoryMining(path_to_repo=path_to_repo,
                                       from_commit=from_commit,
                                       to_commit=to_commit,
                                       reversed_order=False).traverse_commits():
            for modified_file in commit.modifications:
                if modified_file.change_type == ModificationType.DELETE:
                    continue
                is_bug_introducing = False

                file_path = renamed_files.get(modified_file.new_path, modified_file.new_path)
                if ".java" not in modified_file.new_path:
                    print("Left out non Java file: ", file_path)
                    continue

                if modified_file.change_type == ModificationType.RENAME:
                    renamed_files[modified_file.old_path] = file_path

                file_name = file_path.split("/")[-1]

                for method in modified_file.methods:
                    method_long_name = RepositoryMiner.__generate_method_long_name(file_name, method.long_name)
                    yield MethodDTO(modified_file, method, method_long_name, commit, is_bug_introducing)

    def __get_bug_introducing_commits(self, path_to_repo, from_commit, to_commit):
        bug_introducing_commit_hashes = {}
        for commit in RepositoryMining(path_to_repo=path_to_repo,
                                       from_commit=from_commit,
                                       to_commit=to_commit,
                                       reversed_order=False).traverse_commits():
            if self.__is_message_bugfix(commit.msg):
                bug_introducing = GitRepository(path_to_repo).get_commits_last_modified_lines(commit)
                for file in bug_introducing:
                    previous = bug_introducing_commit_hashes.get(file, set())
                    for commits in bug_introducing[file]:
                        previous.add(commits)
                    bug_introducing_commit_hashes[file] = previous
        return bug_introducing_commit_hashes

    @staticmethod
    def __generate_method_long_name(file_name, method_long_name):
        return file_name + ":" + method_long_name

    def __generate_metrics(self, method_dto):
        method_metrics = self.methods.get(method_dto.method_long_name, MethodMetric(method_dto))
        method_metrics = self.__update_metrics(method_metrics, method_dto)
        self.methods[method_dto.method_long_name] = method_metrics
        return method_metrics.metrics[-1]

    def __update_metrics(self, method_metrics, method_dto):
        try:
            old_metrics = method_metrics.metrics[-1]
        except IndexError:
            old_metrics = RepositoryMiner.__generate_empty_metrics(method_metrics)
        new_metrics = old_metrics.copy()
        self.__add_declaration_count(method_dto, new_metrics, old_metrics)
        if new_metrics["old_decl_line"] != "":
            method_metrics = self.__find_method_by_decl_line(new_metrics["old_decl_line"])
            try:
                old_metrics = method_metrics.metrics[-1]
            except IndexError:
                old_metrics = RepositoryMiner.__generate_empty_metrics(method_metrics)
            tmp_new_decl = new_metrics["new_decl_line"]
            new_metrics = old_metrics.copy()
            new_metrics["new_decl_line"] = tmp_new_decl
            new_metrics[DECL] += 1
        if new_metrics["new_decl_line"]:
            method_metrics.decl_line = new_metrics["new_decl_line"]
        self.__add_bug_metetrics(method_dto, new_metrics)
        self.__add_stmt_metrics(method_dto, new_metrics, old_metrics)
        self.__add_author_metrics(method_dto, new_metrics, old_metrics)
        self.__add_condition_statements(method_dto, new_metrics, old_metrics)
        if RepositoryMiner.__has_changed(new_metrics, old_metrics):
            new_metrics["hash"] = method_dto.commit.hash
            new_metrics["name"] = method_dto.method_long_name
            method_metrics.metrics.append(new_metrics)
            return method_metrics
        else:
            raise NoChangeException("There was no change")

    def __add_bug_metetrics(self, method_dto, new_metrics):
        new_metrics[BUG_FIX] = self.__is_message_bugfix(method_dto.commit.msg.lower())
        new_metrics[IS_BUG] = method_dto.is_bug_introducing

    def __is_message_bugfix(self, msg):
        return any(x in msg.lower() for x in BUG_FIX_STRINGS)

    def __add_declaration_count(self, method_dto, new_metrics, old_metrics):
        add_line = ""
        del_line = ""
        declaration_lines = get_changed_lines_between(method_dto.modified_file.diff, method_dto.method.start_line,
                                                      method_dto.method.start_line)
        if len(declaration_lines) == 0:
            return
        for line in declaration_lines[:2]:
            if line[1][0] == "+":
                add_line = line[1]
            else:
                del_line = line[1]
        new_metrics["new_decl_line"] = add_line[1:]
        new_metrics["old_decl_line"] = del_line[1:]
        new_metrics[DECL] = old_metrics[DECL] + 1

    @staticmethod
    def __generate_empty_metrics(method_metrics):
        return {SUM_ADDED: 0,
                MAX_ADDED: 0,
                NUM_MODIFIED: 0,
                SUM_DELETED: 0,
                MAX_DELETED: 0,
                MAX_CHURN: 0,
                "authors": set(),
                CHURN: 0,
                AVG_ADDED: 0,
                AVG_DELETED: 0,
                AVG_CHURN: 0,
                DECL: 0,
                COND_CHANGES: 0,
                ELSE_DEL: 0,
                ELSE_ADD: 0,
                "old_decl_line": method_metrics.decl_line,
                "new_decl_line": "",
                }

    def __add_author_metrics(self, method_dto, new_metrics, old_metrics):
        if method_dto.method.statements_deleted or method_dto.method.statements_added:
            new_metrics["authors"].add(method_dto.commit.author)

    def __add_stmt_metrics(self, method_dto, new_metrics, old_metrics):
        new_metrics[SUM_ADDED] = old_metrics[SUM_ADDED] + method_dto.method.statements_added
        new_metrics[SUM_DELETED] = old_metrics[SUM_DELETED] + method_dto.method.statements_deleted
        if old_metrics[MAX_ADDED] < method_dto.method.statements_added:
            new_metrics[MAX_ADDED] = method_dto.method.statements_added
        if old_metrics[MAX_DELETED] < method_dto.method.statements_deleted:
            new_metrics[MAX_DELETED] = method_dto.method.statements_deleted
        if method_dto.method.statements_added or method_dto.method.statements_deleted:
            new_metrics[NUM_MODIFIED] = old_metrics[NUM_MODIFIED] + 1
        if method_dto.method.statements_added - method_dto.method.statements_deleted > old_metrics[MAX_CHURN]:
            new_metrics[MAX_CHURN] = method_dto.method.statements_added - method_dto.method.statements_deleted
        new_metrics[CHURN] = new_metrics[SUM_ADDED] - new_metrics[SUM_DELETED]
        RepositoryMiner.__add_stmt_averages(new_metrics)

    @staticmethod
    def __add_stmt_averages(metrics):
        if metrics[NUM_MODIFIED] == 0:
            metrics[AVG_ADDED] = 0
            metrics[AVG_DELETED] = 0
            metrics[AVG_CHURN] = 0
        else:
            metrics[AVG_ADDED] = metrics[SUM_ADDED] / metrics[NUM_MODIFIED]
            metrics[AVG_DELETED] = metrics[SUM_DELETED] / metrics[NUM_MODIFIED]
            metrics[AVG_CHURN] = metrics[CHURN] / metrics[NUM_MODIFIED]
        return metrics

    @staticmethod
    def __has_changed(new_metrics, old_metrics):
        for key in new_metrics.keys():
            if old_metrics[key] != new_metrics[key]:
                return True
        return False

    def __find_method_by_decl_line(self, decl_line):
        for method_key in self.methods.keys():
            if self.methods[method_key].decl_line == decl_line:
                return self.methods[method_key]

    def __add_condition_statements(self, method_dto, new_metrics, old_metrics):
        method_diff = get_changed_lines_between(method_dto.modified_file.diff, method_dto.method.start_line,
                                                method_dto.method.end_line)
        changed_conditions = []
        else_added = []
        else_removed = []
        for line in method_diff:
            RepositoryMiner.__check_line(line, REGEX_CONDITION, changed_conditions)
            RepositoryMiner.__check_line(line, REGEX_ELSE_DELETE, else_removed)
            RepositoryMiner.__check_line(line, REGEX_ELSE_ADD, else_added)

        new_metrics[COND_CHANGES] = old_metrics[COND_CHANGES] + len(changed_conditions)
        new_metrics[ELSE_ADD] = old_metrics[ELSE_ADD] + len(else_added)
        new_metrics[ELSE_DEL] = old_metrics[ELSE_DEL] + len(else_removed)

    @staticmethod
    def __check_line(line, regular_expression, tracking):
        if re.findall(regular_expression, line[1]):
            tracking.append(line[0])


class MethodMetric:
    def __init__(self, method_dto):
        self.method_name = method_dto.method_long_name
        self.metrics = []
        self.decl_line = get_lines_between(method_dto.modified_file.source_code, method_dto.method.start_line, method_dto.method.start_line)[0]

    def change_decl(self, add_line):
        self.metrics[DECL] += 1
        if add_line != "":
            self.decl_line = add_line


class MethodDTO:
    def __init__(self, modified_file, method, method_long_name, commit, is_bug_introducing):
        self.modified_file = modified_file
        self.method = method
        self.method_long_name = method_long_name
        self.commit = commit
        self.is_bug_introducing = is_bug_introducing

class MethodDS:
    def __init__(self, method, last_decl_line, method_long_name):
        self.method = method
        self.decl_changes = 0
        self.last_decl_line = last_decl_line
        self.method_long_name = method_long_name

    def change_decl(self, add_line, del_line):
        self.decl_changes += 1
        if del_line == "":
            self.last_decl_line = add_line[1:]
        else:
            self.last_decl_line = del_line[1:]


class NoChangeException(Exception):
    def __init__(self, message):
        self.message = message
