from Utils.CSV import build_csv_from_array


class TableFunctionEntry:
    def __init__(self, method_dto, metrics):
        self.hash = method_dto.commit.hash
        self.method_long_name = method_dto.method_long_name
        self.file_name = method_dto.modified_file.filename
        self.fan_in = method_dto.method.fan_in
        self.fan_out = method_dto.method.fan_out
        self.local_variables = method_dto.method.nloc
        self.parameters = len(method_dto.method.parameters)
        self.comment_to_code_ratio = method_dto.method.comment_to_code_ration
        self.count_path = method_dto.method.path_count
        self.complexity = method_dto.method.complexity
        self.exec_statements = method_dto.method.exec_statements
        self.max_nesting = method_dto.method.top_nesting_level

        self.max_stmt_added = metrics["max_statement_added"]
        self.sum_stmt_added = metrics["sum_statement_added"]
        self.method_histories = metrics["method_histories"]
        self.stmt_added = metrics["sum_statement_added"]
        self.max_stmt_added = metrics["max_statement_added"]
        self.avg_stmt_added = metrics["average_statement_added"]
        self.sum_stmt_deleted = metrics["sum_statement_deleted"]
        self.max_stmt_deleted = metrics["max_statement_deleted"]
        self.avg_stmt_deleted = metrics["average_statement_deleted"]
        self.churn = metrics["churn"]
        self.max_churn = metrics["max_churn"]
        self.avg_churn = metrics["average_churn"]
        self.authors = len(metrics["authors"])
        self.decl_changes = metrics["decl_changes"]
        self.cond = metrics["condition_changes"]
        self.else_added = metrics["else_added"]
        self.else_deleted = metrics["else_removed"]
        self.is_bug_fix = metrics["is_bug_fix"]
        self.is_bug = metrics["is_bug"]

    def get_as_csv(self):
        return build_csv_from_array(self.get_array_of_metrics())

    def get_array_of_metrics(self):
        return [self.hash, self.file_name, self.method_long_name, self.fan_in, self.fan_out,
                self.local_variables,
                self.parameters, self.comment_to_code_ratio, self.count_path, self.complexity, self.exec_statements,
                self.max_nesting, self.method_histories, self.authors, self.stmt_added, self.max_stmt_added,
                self.avg_stmt_added, self.sum_stmt_deleted, self.max_stmt_deleted, self.avg_stmt_deleted, self.churn,
                self.max_churn, self.avg_churn, self.decl_changes, self.cond, self.else_added, self.else_deleted, self.is_bug]

    @staticmethod
    def get_csv_header():
        return ["Hash", "Filename", "Method_Name", "Fan_In", "Fan_Out", "Local_Variables", "Parameters",
                "Comment_to_Code_Ratio", "Path_Count", "Complexity", "Executable_Statements", "Maximal_Nesting",
                "Method_Histories", "Authors", "Statmenet Added", "Max Statement Added", "Average Statement Added",
                "Statement Deleted", "Maximum Statement Deleted", "Average Statement Deleted", "Churn", "Maximum Churn",
                "Average Churn", "Declaration Changes", "Conditions", "Else Added", "Else Deleted", "Is_Bug"]
