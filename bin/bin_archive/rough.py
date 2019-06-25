"C*08:01", "C*15:17", "C*18:01", "C*27:05","C*41:01","C*49:01", "C*51:01", "C*57:01", "C*58:01"


"C*07:02","C*13:01","C*35:05","C*38:02","C*39:06","C*40:01","C*67:01"



    options = {
        "DR1": ["DQ5","DQ7"],
        "DR103": ["DQ5", "DQ7"],
        "DR4": ["DQ2","DQ7", "DQ8", "DQ4"],
        "DR7": ["DQ2", "DQ9","DQ5","DQ7"],
        "DR8": ["DQ4", "DQ7", "DQ6","DQ2","DQ8"],
        "DR9": ["DQ2", "DQ9"],
        "DR10": ["DQ5","DQ6"],
        "DR11": ["DQ2","DQ5","DQ6","DQ7","DQ8"],
        "DR12": ["DQ5", "DQ7"],
        "DR13": ["DQ2", "DQ6", "DQ7","DQ5"],
        "DR14": ["DQ5","DQ6", "DQ7"],
        "DR15": ["DQ6", "DQ5","DQ2","DQ7"],
        "DR16": ["DQ5","DQ7"],
        "DR17": ["DQ2","DQ6"],
        "DR18": ["DQ4"]
    }

   def assimilate_classII(data,patient,classII):
    """ Function that substitutes low-res with high-res class II alleles"""

    rows = data.shape[0]

    for row in range(rows)
        code1 = data.loc[row, patient + "_First_Sub"]
        code2 = data.loc[row, patient + "_Second_Sub"]
        R1 = data.loc[row, "HR_" + patient + "_First_DR_Split"]
        R2 = data.loc[row, "HR_" + patient + "_Second_DR_Split"]
        Q1 = data.loc[row, "HR_" + patient + "_First_DQ_Split"]
        Q2 = data.loc[row, "HR_" + patient + "_Second_DQ_Split"]
        #print(code1,code2)

        if type(code1) != str or type(code2) != str:
            continue
        elif code1.startswith("a"):
            code1 = int(code1.lstrip("a"))
            code2 = int(code2.lstrip("a"))
            for rule in classII:
                if rule[0] == code1:
                    data.loc[row, "HR_" + patient + "_First_DR_Split"] = rule[2]
                    data.loc[row, "HR_" + patient + "_First_DRB3/4/5"] = rule[4]
                    data.loc[row, "HR_" + patient + "_First_DQ_Split"] = rule[6]
                    data.loc[row, "HR_" + patient + "_First_DQA"] = rule[7]
                if rule[0] == code2:
                    data.loc[row, "HR_" + patient + "_Second_DR_Split"] = rule[2]
                    data.loc[row, "HR_" + patient + "_Second_DRB3/4/5"] = rule[4]
                    data.loc[row, "HR_" + patient + "_Second_DQ_Split"] = rule[6]
                    data.loc[row, "HR_" + patient + "_Second_DQA"] = rule[7]
        elif code1.startswith("b"):
            code1 = int(code1.lstrip("b"))
            code2 = int(code2.lstrip("b"))
            for rule in classII:
                if rule[0] == code1:
                    data.loc[row, "HR_" + patient + "_First_DR_Split"] = rule[2]
                    data.loc[row, "HR_" + patient + "_First_DRB3/4/5"] = rule[4]
                    data.loc[row, "HR_" + patient + "_Second_DQ_Split"] = rule[6]
                    data.loc[row, "HR_" + patient + "_Second_DQA"] = rule[7]
                if rule[0] == code2:
                    data.loc[row, "HR_" + patient + "_Second_DR_Split"] = rule[2]
                    data.loc[row, "HR_" + patient + "_Second_DRB3/4/5"] = rule[4]
                    data.loc[row, "HR_" + patient + "_First_DQ_Split"] = rule[6]
                    data.loc[row, "HR_" + patient + "_First_DQA"] = rule[7]

def broad2split(data,patient):
    """ Function that substitutes low-res with high-res class II alleles"""

    rows = data.shape[0]


    for row in range(rows):
        R1 = data.loc[row, "HR_" + patient + "_First_DR_Split"]
        R2 = data.loc[row, "HR_" + patient + "_Second_DR_Split"]
        Q1 = data.loc[row, "HR_" + patient + "_First_DQ_Split"]
        Q2 = data.loc[row, "HR_" + patient + "_Second_DQ_Split"]

        if R1 == "DR3":
            data.loc[row, "HR_" + patient + "_First_DR_Split"] = "DR17"

        if R2 == "DR3":
            data.loc[row, "HR_" + patient + "_Second_DR_Split"] = "DR17"

        if Q1 == "DQ1":
            if (R1== "DR1") or (R2 == "DR1"):
                data.loc[row, "HR_" + patient + "_First_DQ_Split"] = "DQ5"
            elif (R1== "DR16") or (R2 == "DR16"):
                data.loc[row, "HR_" + patient + "_First_DQ_Split"] = "DQ5"
            elif (R1 == "DR15") or (R2 == "DR15"):
                data.loc[row, "HR_" + patient + "_First_DQ_Split"] = "DQ6"
            elif (R1 == "DR13") or (R2 == "DR13"):
                data.loc[row, "HR_" + patient + "_First_DQ_Split"] = "DQ6"

        if Q2 == "DQ1":
            if (R1== "DR1") or (R2 == "DR1"):
                data.loc[row, "HR_" + patient + "_Second_DQ_Split"] = "DQ5"
            elif (R1== "DR16") or (R2 == "DR16"):
                data.loc[row, "HR_" + patient + "_Second_DQ_Split"] = "DQ5"
            elif (R1 == "DR15") or (R2 == "DR15"):
                data.loc[row, "HR_" + patient + "_Second_DQ_Split"] = "DQ6"
            elif (R1 == "DR13") or (R2 == "DR13"):
                data.loc[row, "HR_" + patient + "_Second_DQ_Split"] = "DQ6"





