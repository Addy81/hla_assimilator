"""
def parse_rules(rules_file):
    parses rules from excel into functional lists
    rules = pd.read_excel(rules_file)
    classII = []
    rule_rows = rules.shape[0]
    for row in range(rule_rows):
        row_sublist = []
        for column in rules.columns:
            row_sublist.append(rules.loc[row][column])
        classII.append(row_sublist)

    for item in classII:
        print(item)

    return classII

parse_rules(rules_path)

"""