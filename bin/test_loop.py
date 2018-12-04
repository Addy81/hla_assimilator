for row in range(rows):
    DR1 = data.loc[row, "HR_Recip_First_DR_Split"]
    DR2 = data.loc[row, "HR_Recip_Second_DR_Split"]
    DQ1 = data.loc[row, "HR_Recip_First_DQ_Split"]
    DQ2 = data.loc[row, "HR_Recip_Second_DQ_Split"]

    dq_options = [data.loc[row, "HR_Recip_First_DQ_Split"], data.loc[row, "HR_Recip_Second_DQ_Split"]]
    print(DR1, DR2)
    print(dq_options)
    print(len(dq_options))

    while len(dq_options) > 0:
        print(len(dq_options))

        if dq_options[0] in options.get(DR1):
            for rule in classII:
                if rule[0] == DR1 and rule[4] == DQ1:
                    data.loc[row, "HR_Recip_First_DR_Split"] = rule[1]
                    data.loc[row, "HR_Recip_First_DRB3/4/5"] = rule[3]
                    data.loc[row, "HR_Recip_First_DQ_Split"] = rule[5]
                    data.loc[row, "HR_Recip_First_DQA"] = rule[6]
                    del dq_options[0]
                    print(dq_options)
                    print(len(dq_options))

                    if dq_options[0] in options.get(DR2):
                        if rule[0] == DR2 and rule[4] == DQ2:
                            data.loc[row, "HR_Recip_Second_DR_Split"] = rule[1]
                            data.loc[row, "HR_Recip_Second_DRB3/4/5"] = rule[3]
                            data.loc[row, "HR_Recip_Second_DQ_Split"] = rule[5]
                            data.loc[row, "HR_Recip_Second_DQA"] = rule[6]
                            del dq_options[0]
        elif len(dq_options) == 2 :
            if dq_options[1] in options.get(DR1):
                for rule in classII:
                    if rule[0] == DR1 and rule[4] == DQ2:
                        data.loc[row, "HR_Recip_First_DR_Split"] = rule[1]
                        data.loc[row, "HR_Recip_First_DRB3/4/5"] = rule[3]
                        data.loc[row, "HR_Recip_Second_DQ_Split"] = rule[5]
                        data.loc[row, "HR_Recip_Second_DQA"] = rule[6]
                        del dq_options[1]

                        if dq_options[0] in options.get(DR2):
                            for rule in classII:
                                if rule[0] == DR2 and rule[4] == DQ1:
                                    data.loc[row, "HR_Recip_Second_DR_Split"] = rule[1]
                                    data.loc[row, "HR_Recip_Second_DRB3/4/5"] = rule[3]
                                    data.loc[row, "HR_Recip_First_DQ_Split"] = rule[5]
                                    data.loc[row, "HR_Recip_First_DQA"] = rule[6]
                                    del dq_options[0]
