
def method_in_commit_has_property(table, commit_hash, method_name, property_name, property_value):
    for entry in table:
        if entry.hash == commit_hash and entry.method_long_name == method_name:
            return getattr(entry, property_name) == property_value
    return False


def method_in_commit_has_properties(table, commit_hash, method_name, properties):
    for entry in table:
        if entry.hash == commit_hash and entry.method_long_name == method_name:
            for key in properties.keys():
                if getattr(entry, key) != properties[key]:
                    return False
            return True
    return False
