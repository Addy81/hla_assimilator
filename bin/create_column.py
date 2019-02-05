# Copy split column and rename it to with an HR_ prefix
for column in data.columns:
    column_check = re.search('_Split', column)
    col_index = data.columns.get_loc(column)
    new_column_name = "HR_" + column
    if column_check:
        data.insert((col_index + 1), new_column_name, data[column])

# when there's the first Cw present - assume homozygous so fill the Second Split column


def add_column(dtf,pattern,new_pattern):
    for column in dtf.columns:
        column_match = re.match(pattern,column)
        col_index = dtf.columns.get_loc(column)
        new_column_name = "HR_" + column
        if column_match: 
            dtf.insert((col_index + 1), new_column_name,dtf[column])


def add_special_column (dtf,pattern,new_pattern):
    column_patterns = ['Recip_First', 'Recip_Second', 'Donor_First', 'Donor_Second']
    for c_pat in column_patterns:
        match_pattern = "HR_" + c_pat + pattern
        
        for column in dtf.columns:
            column_match =re.match(match_pattern)
            col_index= dtf.columns.get_loc(match_pattern)

            if column_match:
                new_column = "HR_" + c_pat + new_pattern
                dtf.insert((col_index+1),new_column,np.nan)

add_special_column(data,'_DR_Split','_DRB3/4/5')     
add_special_column(data,'_DQ_Split','_DQA')            





print ("Adding some extra columns.")
column_patterns = ['Recip_First', 'Recip_Second', 'Donor_First', 'Donor_Second']

for c_pat in column_patterns:
    for column in data.columns:
        dr_pattern = 'HR_' + c_pat + '_DR_Split'
        column_match = re.match(dr_pattern, column)
        col_index = data.columns.get_loc(dr_pattern)
        if column_match:
            new_dr_column = 'HR_' + c_pat + '_DRB3/4/5'
            data.insert((col_index+1),new_dr_column,np.nan)

for c_pat in column_patterns:
    for column in data.columns:
        dqa_pattern = 'HR_' + c_pat + '_DQ_Split'
        column_match = re.match(dqa_pattern, column)
        col_index = data.columns.get_loc(dqa_pattern)
        if column_match:
            new_dq_column = 'HR_' + c_pat + '_DQA'
            data.insert((col_index + 1), new_dq_column, np.nan)

# create a list containing all class II rules
classII = []
rule_row_num = rules.shape[0]
count = 1
for row in range(rule_row_num):
    row_sublist = [count]
    count += 1
    for column in rules.columns:
        row_sublist.append(rules.loc[row][column])
    classII.append(row_sublist)

def create_rules(rules):
    classII = []
    rule_row_num = rules.shape[0]
    count = 1
    for row in range(rule_row_num):
        row_sublist = [count]
        count += 1
        for column in rules.columns:
            row_sublist.append(rules.loc[row][column])
        classII.append(row_sublist)
    
    return classII
