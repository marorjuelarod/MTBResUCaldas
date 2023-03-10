def getTABData(vcfData, executionReport):
    tabData = []
    data = []
    tabTitles = ["#Pos", "Insindex", "Ref", "Type", "Allel", "CovFor", "CovRev", "Qual20", "Freq", "Cov", "Subst", "Gene", "GeneName", "Product", "ResistanceSNP", "PhyloSNP", "InterestingRegion"]
    tabData.append(tabTitles)

    for register in vcfData:
        type = getType(register, executionReport) #Obtiene columna Type
        if(type != "Ins"):
            pos = getPos(register) #Obtiene columna #Pos
            insindex = getInsindex(type, executionReport) #Obtiene columna Insindex

            ref = getRef(register) #Obtiene columna Ref
            allel = getAllel(register, type, executionReport) #Obtiene columna Allel
            covFor = getCovFor(register, executionReport) #Obtiene columna CovFor
            covRev = getCovRev(register, executionReport) #Obtiene columna CovRev

            qual20 = getQual20(register) #Obtiene columna Qual20
            freq = getFreq(register, executionReport) #Obtiene columna Freq
            cov = getCov(register, executionReport) #Obtiene columna Cov

            if(type != "SNP"):
                subst = ""
            else:
                subst = getSubst(register, executionReport) #Obtiene columna Subst

            gene = getGene(register, executionReport) #Obtiene columna Gene
            
            geneName = getGeneName(register, executionReport) #Obtiene columna GeneName
            product = getProduct(register, executionReport) #Obtiene columna Product

            data = [pos, insindex, ref, type, allel, covFor, covRev, qual20, freq, cov, subst, gene, geneName, product]
            tabData.append(data)
        else:
            for i, base in enumerate(register[4]):
                pos = getPos(register) #Obtiene columna #Pos
                insindex = str(i + 1)

                ref = getRef(register) #Obtiene columna Ref
                allel = base
                covFor = getCovFor(register, executionReport) #Obtiene columna CovFor
                covRev = getCovRev(register, executionReport) #Obtiene columna CovRev

                qual20 = getQual20(register) #Obtiene columna Qual20
                freq = getFreq(register, executionReport) #Obtiene columna Freq
                cov = getCov(register, executionReport) #Obtiene columna Cov
                subst = getSubst(register, executionReport) #Obtiene columna Subst
                gene = getGene(register, executionReport) #Obtiene columna Gene
                
                geneName = getGeneName(register, executionReport) #Obtiene columna GeneName
                product = getProduct(register, executionReport) #Obtiene columna Product

                data = [pos, insindex, ref, type, allel, covFor, covRev, qual20, freq, cov, subst, gene, geneName, product]
                tabData.append(data)
    return tabData

def getPos(register):
    return register[1]

def getInsindex(type, executionReport):
    if(type == "SNP" or type == "Del"):
        return "0"
    else:
        executionReport.write("\t\tError definiendo insIndex" + "\n")
        # print("\t\tError definiendo insIndex")
        return ""
    
def getRef(register):
    return register[3][0]

def getType(register, executionReport):
    ref = register[3]
    alt = register[4]
    if(len(ref) == 1 and len(alt) == 1):
        return "SNP"
    elif(len(ref) > len(alt)):
        return "Del"
    elif(len(ref) < len(alt)):
        return "Ins"
    else:
        executionReport.write("\t\tError definiendo el type" + "\n")
        # print("\t\tError definiendo el type")
        return ""

def getAllel(register, type, executionReport):
    if(type == "SNP"):
        return register[4]
    elif(type == "Del"):
        return "GAP"
    else:
        executionReport.write("\t\tError definiendo Allel" + "\n")
        # print("\t\tError definiendo Allel")
        return ""

def getCovFor(register, executionReport):
    return getDP(register, executionReport)

def getCovRev(register, executionReport):
    return getDP(register, executionReport)

def getQual20(register):
    return register[5]

def getFreq(register, executionReport):
    return getGQ(register, executionReport)

def getCov(register, executionReport):
    return getDP(register, executionReport)

def getSubst(register, executionReport):
    return getTACH(register, executionReport)
    
def getGene(register, executionReport):
    return getTGN(register, executionReport)

def getGeneName(register, executionReport):
    return getTGN(register, executionReport)

def getProduct(register, executionReport):
    return getTA(register, executionReport)


def getDP(register, executionReport):
    infoArray = register[7].split(';')
    for info in infoArray:
        if "DP" in info.upper():
            return info[3:]
    executionReport.write("\t\tError definiendo el DP" + "\n")
    # print("\t\tError definiendo el DP")
    return ""

def getGQ(register, executionReport):
    format = register[8].split(":")
    values = register[9].split(":")
    for i, variable in enumerate(format):
        if ("GQ" == variable.upper()):
            return values[i]
    executionReport.write("\t\tError definiendo el GQ" + "\n")
    # print("\t\tError definiendo el GQ")
    return ""

def getTACH(register, executionReport):
    infoArray = register[7].split(';')
    for info in infoArray:
        if "TACH" in info.upper():
            return changeNomenclature(info[5:], executionReport)
    executionReport.write("\t\tError definiendo el TACH" + "\n")
    # print("\t\tError definiendo el TACH")
    return ""

def getTGN(register, executionReport):
    infoArray = register[7].split(';')
    for info in infoArray:
        if "TGN" in info.upper():
            if "DNAN" in info.upper():
                executionReport.write("\t\tError definiendo el TGN: Se encontró dnaN" + "\n")
                # print("\t\tError definiendo el TGN: Se encontró dnaN")
                return ""
            return info[4:]
    executionReport.write("\t\tError definiendo el TGN" + "\n")
    # print("\t\tError definiendo el TGN")
    return ""

def getTA(register, executionReport):
    infoArray = register[7].split(';')
    for info in infoArray:
        if "TA" in info.upper():
            return info[3:]
    executionReport.write("\t\tError definiendo el TA" + "\n")
    # print("\t\tError definiendo el TA")
    return ""


def changeNomenclature(tach, executionReport):
    nomenclature = {
        'A': 'Ala',
        'R': 'Arg',
        'N': 'Asn',
        'D': 'Asp',
        'C': 'Cys',
        'Q': 'Gln',
        'E': 'Glu',
        'G': 'Gly',
        'H': 'His',
        'I': 'Ile',
        'L': 'Leu',
        'K': 'Lys',
        'M': 'Met',
        'F': 'Phe',
        'P': 'Phe',
        'S': 'Ser',
        'T': 'Thr',
        'W': 'Trp',
        'Y': 'Tyr',
        'V': 'Val'
        }
    
    aa1 = ""
    aa2 = ""
    num = ""

    i = 0
    while((not tach[i].isdigit()) and i < len(tach)):
        aa1 += tach[i]
        i += 1
    
    while(tach[i].isdigit() and i < len(tach)):
        num += str(tach[i])
        i += 1
    
    i = len(tach) - 1
    while((not tach[i].isdigit()) and i >= 0):
        aa2 += tach[i]
        i -= 1

    if(aa1.isalpha() and aa2.isalpha() and num.isnumeric()):
        return nomenclature[aa1[0].upper()] + num + nomenclature[aa2[-1].upper()]
    else:
        if("*" in aa1):
            aa1 = "*"
        else:
            executionReport.write("\t\tError definiendo el primer aminoácido" + "\n")
            # print("\t\tError definiendo el primer aminoácido")
            return ""
        if("*" in aa2):
            aa2 = "*"
        else:
            executionReport.write("\t\tError definiendo el segundo aminoácido" + "\n")
            # print("\t\tError definiendo el segundo aminoácido")
            return ""
        return aa1 + num + aa2
