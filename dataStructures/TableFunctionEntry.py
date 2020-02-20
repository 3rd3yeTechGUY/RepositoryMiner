class TableFunctionEntry:
    def __init__(self, commit, modification, method,
                 ):
        self.__commit = commit
        self.__modification = modification
        self.__method = method
        self.__file_name = self.__modification.filename

    def get_as_csv(self):
        return "{},{},{},{},{},{},{},{}".format(self.get_commit_hash(), self.__file_name, self.get_method_name(),
                                             self.get_file_changes_upto_now(), self.get_fan_in(), self.get_fan_out(),
                                             self.get_complexity(), self.get_parameters())

    def get_fan_in(self):
        return self.__method.fan_in

    def get_fan_out(self):
        return self.__method.fan_out

    def get_complexity(self):
        return self.__method.complexity

    def get_parameters(self):
        return self.__method.parameters

    def get_file_changes_upto_now(self):
        return self.__file_changes_upto_now_to_file

    def get_commit_hash(self):
        return self.__commit.hash

    def get_method(self):
        return self.__method

    def get_method_name(self):
        return self.__method.name

    def get_file_name(self):
        return self.__modification.filename

    def get_file_changes_upto_now_to_file(self):
        return self.__file_changes_upto_now_to_file

    def get_lines_added_in_file_normalized(self):
        return self.__normalize(self.get_lines_added_in_file_absolute())

    def get_lines_added_in_file_absolute(self):
        return self.__modification.added

    def get_lines_deleted_in_file_absolute(self):
        return self.__modification.removed

    def get_lines_deleted_in_file_normalized(self):
        return self.__normalize(self.get_lines_deleted_in_file_absolute())

    def get_lines_of_file_before(self):
        return self.__modification.nloc;

    def get_percentage_lines_authored_in_project(self):
        # TODO implement percentage lines authored
        return -1

    def get_number_of_unique_changes(self):
        return -1
        # TODO implement number of unique changes

    def __normalize(self, number):
        # TODO Add implementation of Normalize
        return number;
