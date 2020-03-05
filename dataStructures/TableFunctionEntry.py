from Utils.CSV import build_csv_from_array


class TableFunctionEntry:
    def __init__(self, method_dto, metrics):
        self.hash = method_dto.commit.hash
        self.method_long_name = method_dto.method_long_name
        self.file_name = method_dto.modified_file.filename
        self.sum_statement_added = metrics["sum_statement_added"]

        # self.fan_in = method.fan_in
        # self.fan_out = method.fan_out
        # self.local_variables = method.nloc
        # self.parameters = len(method.parameters)
        # self.comment_to_code_ratio = method.comment_to_code_ration
        # self.count_path = method.path_count
        # self.complexity = method.complexity
        # self.exec_statements = method.exec_statements
        # self.max_nesting = method.top_nesting_level
        # self.method_histories = stmt_count["method_histories"]
        # self.authors = author_metrics
        # self.stmt_added = stmt_count["sum_statement_added"]
        # self.max_stmt_added = stmt_count["max_statement_added"]
        # self.avg_stmt_added = stmt_count["average_statement_added"]
        # self.stmt_deleted = stmt_count["sum_statement_deleted"]
        # self.max_stmt_deleted = stmt_count["max_statement_deleted"]
        # self.avg_stmt_deleted = stmt_count["average_statement_deleted"]
        # self.churn = stmt_count["churn"]
        # self.max_churn = stmt_count["max_churn"]
        # self.avg_churn = stmt_count["average_churn"]
        # self.decl = decl_metrics
        # self.cond = condition_metrics["condition_changes"]
        # self.else_added = condition_metrics["else_added"]
        # self.else_deleted = condition_metrics["else_removed"]

    def get_as_csv(self):
        return build_csv_from_array(self.get_array_of_metrics())

    def get_array_of_metrics(self):
        return [self.hash, self.file_name, self.method_long_name, self.fan_in, self.fan_out,
                self.local_variables,
                self.parameters, self.comment_to_code_ratio, self.count_path, self.complexity, self.exec_statements,
                self.max_nesting, self.method_histories, self.authors, self.stmt_added, self.max_stmt_added,
                self.avg_stmt_added, self.stmt_deleted, self.max_stmt_deleted, self.avg_stmt_deleted, self.churn,
                self.max_churn, self.avg_churn, self.decl, self.cond, self.else_added, self.else_deleted]

    @staticmethod
    def get_csv_header():
        return ["Hash", "Filename", "Method Name", "Fan In", "Fan Out", "Local Variables", "Parameters",
                "Comment to Code Ratio", "Path Count", "Complexity", "Executable Statements", "Maximal Nesting",
                "Method Histories", "Authors", "Statmenet Added", "Max Statement Added", "Average Statement Added",
                "Statement Deleted", "Maximum Statement Deleted", "Average Statement Deleted", "Churn", "Maximum Churn",
                "Average Churn", "Declaration Changes", "Conditions", "Else Added", "Else Deleted"]
