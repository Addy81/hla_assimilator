
def c_assimilation(to_replace, general_rule, exc1, exc2=(None, None),exc3=(None, None)):
    for patient in ['Recip', 'Donor']:
        for variable in ['First', 'Second']:
            rows = data.shape[0]
            for row in range(rows):
                c_col = "HR_" + patient + '_' + variable + '_C_Split'
                b1_col = "HR_" + patient + '_First_B_Split'
                b2_col = "HR_" + patient + '_Second_B_Split'

                c = data.loc[row, c_col]
                b1 = data.iloc[row][b1_col]
                b2 = data.iloc[row][b2_col]

                if pd.isnull(data.loc[row, c_col]):
                    pass
                elif c == to_replace and ((b1 == exc1[0]) or (b2 == exc1[0])):
                    data.loc[row, c_col] = re.sub(to_replace, exc1[1], c)
                elif c == to_replace and ((b1 == exc2[0]) or (b2 == exc2[0])):
                    data.loc[row, c_col] = re.sub(to_replace, exc2[1], c)
                elif c == to_replace and ((b1 == exc3[0]) or (b2 == exc3[0])):
                    data.loc[row, c_col] = re.sub(to_replace, exc2[1], c)
                else:
                    data.loc[row, c_col] = re.sub(to_replace, general_rule, c)


# Function that replaces Cw alleles based on the B allele correlation
# format of function is
# to_replace - CwX : the low res allele to be substituted
# general_rule : C*xx:xx :the most common high-res allele
# exc1,exc2,exc3: tuple that contains the associated B allele with the special C to replace. (B*xx:xx,C*xx:xx)


c_assimilation(to_replace='Cw10', general_rule='C*03:02', exc1=('B*40:01', 'C*03:04'), exc2=('B*15:01', 'C*03:04'))
c_assimilation(to_replace='Cw8', general_rule='C*08:01', exc1=('B*14:01', 'C*08:02'), exc2=('B*14:02', 'C*08:02'))
c_assimilation(to_replace='Cw16', general_rule='C*16:01', exc1=('B*44:03', 'C*16:02'), exc2=('B*55:01', 'C*16:02'))
c_assimilation(to_replace='Cw7', general_rule='C*07:01', exc1=('B*07:02', 'C*07:02'))