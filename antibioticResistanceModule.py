import os
import sys
import pandas as pd

class AntibioticResistanceModule():
    def __init__(self, resultsFolder, folder):
        self.resultsFolder = resultsFolder
        self.folder = folder

        self.arReport = open(f"{resultsFolder}/executionReports/arreport.txt", 'w')
        self.arReport.write("REPORTE DE EJECUCIÓN: Reporte de resistencia antibiótica\n\n")

        self.antibioticResistanceAnalysis(folder)

        self.endARReport()
    
    def getFolders(self, path):
        """Obtiene una lista de carpetas que se encuentran en un directorio dado.

        Parametros
        ----------
        path : str
            La ruta o el directorio del cual se quiere obtener las carpetas internas

        Retorna
        -------
        carpetas
            una lista de carpetas o directorios
        """
        with os.scandir(path) as content:
            folders = [folder for folder in content if folder.is_dir()]
        return folders


    def getXlsxFiles(self, path):
        """Obtiene una lista de documentos con formato .xlsx (excel) que se encuentran en un directorio dado.

        Parámetros
        ----------
        path : str
            La ruta del directorio del cual se quiere obtener los archivos o documentos excel internos.

        Retorna
        -------
        documentos
            una lista de documentos con formato .xlsx
        """
        try:
            with os.scandir(path) as content:
                files = [file for file in content if file.is_file(
                ) and file.name.endswith('.xlsx')]
            return files
        except OSError as e:
            raise
    
    def readXlsx(self, path):
        """Lee documentos .xlsx (excel) 

        Parametros
        ----------
        path : str
            La ruta absoluta del documento excel a leer

        Retorna
        -------
        contenido
            Un arreglo con la información por cada columna del excel
        """

        df = pd.read_excel(path, sheet_name='Hoja1')
        keys = df.to_dict().keys()
        values = df.to_dict().values()
        titles = [i for i in keys]
        dictColumns = [i.values() for i in values]
        columns = []
        for column in dictColumns:
            columns.append([j for j in column])
        if titles != [] and columns != []:
            return [titles, columns]
        else:
            return None

    def find_TACH_TGN(self, array):
        """Obtiene el valor del TACH y TGN de entre la información de una posición del genoma

        Parámetros
        ----------
        array
            Arreglo con la información correspondiente a una posición del genoma

        Retorna
        -------
        TACH_TGN
            Retorna un arreglo con el TACH Y TGN
        """

        TACH_TGN = [0, 0]
        for a in array:
            if 'TACH' in a:
                TACH_TGN[0] = a[a.index('=')+1:]
            elif 'TGN' in a:
                TACH_TGN[1] = a[a.index('=')+1:]

            if TACH_TGN[0] != 0 and TACH_TGN[1] != 0:
                return TACH_TGN
        return TACH_TGN
    
    def find_TACH_TGN2(self, array):
        """Obtiene el valor del TACH y TGN de entre la información de una posición del genoma

        Parámetros
        ----------
        array
            Arreglo con la información correspondiente a una posición del genoma

        Retorna
        -------
        TACH_TGN
            Retorna un arreglo con el TACH Y TGN
        """
        print(array)
        TACH_TGN = [0, 0]
        if array[10] != "" and "DNAN" not in array[10].upper():
            TACH_TGN[0] = self.changeNomenclature(array[10])
        if array[3] != "" and "DNAN" not in array[3].upper():
            TACH_TGN[1] = array[3]
        
        return TACH_TGN

    def changeNomenclature(self, tach):
        nomenclature = {
            'ala': 'A',
            'arg': 'R',
            'asn': 'N',
            'asp': 'D',
            'cys': 'C',
            'gln': 'Q',
            'glu': 'E',
            'gly': 'G',
            'his': 'H',
            'ile': 'I',
            'leu': 'L',
            'lys': 'K',
            'met': 'M',
            'phe': 'F',
            'phe': 'P',
            'ser': 'S',
            'thr': 'T',
            'trp': 'W',
            'tyr': 'Y',
            'val': 'V'
            }
        
        aa1 = ""
        aa2 = ""
        num = ""

        i = 0
        if('.' in tach):
            while(tach[i] != '.'):
                i += 1
            i += 1

        while((not tach[i].isdigit()) and i < len(tach)):
            aa1 += tach[i]
            i += 1
        
        while(tach[i].isdigit() and i < len(tach)):
            num += str(tach[i])
            i += 1
        i_aa2 = i
        
        while(i < len(tach)):
            if (not tach[i].isdigit()):
                aa2 += tach[i]
                i += 1
            else:
                i = len(tach)
        
        # print("tach: " + tach)
        # print(f"{aa1} - {num} - {aa2}")
        # print(f"{aa1[0]} - {num} - {aa2[0]}")
        # print(f"{aa1[0:3]} - {num} - {aa2[0:3]}")

        if(aa1.isalpha() and aa2.isalpha() and num.isnumeric()):
            return nomenclature[aa1[0:3].lower()] + num + nomenclature[aa2[0:3].lower()]
        else:
            if("*" in aa1):
                aa1 = "*"
            else:
                print("\t\tError definiendo el primer aminoácido" + "\n")
                return ""
            if("*" in aa2):
                aa2 = "*"
            else:
                print("\t\tError definiendo el segundo aminoácido" + "\n")
                return ""
            return aa1 + num + aa2



    def getTGNDict(self):
        TGN_isoniazida = ['fabG1', 'furA', 'inbR', 'inhA', 'kasA', 'katG', 'mmaA3', 'mshA', 'mshB', 'mshC', 'mymA',
                        'nat', 'nhoA', 'ndh', 'nudC', 'sigI', 'oxyR', 'ahpC']
        TGN_rifampicina = ['ponA1', 'rpoB', 'rpoA', 'rpoC']
        TGN_ethambutol = ['aftA', 'embA', 'embB',
                        'embC', 'embR', 'ubiA', 'Rv3806c']
        TGN_pirazinamida = ['clpC1', 'gpsI', 'mas', 'panD', 'pncA', 'Rv2042c', 'ppsA', 'ppsB', 'ppsC', 'ppsD', 'proZ',
                            'rpsA', 'Rv0191', 'Rv1667c', 'cyp139', 'Rv2731', 'Rv3008', 'Rv3169']
        TGN_quinolonas = ['eccB5', 'eccC5', 'gyrA', 'gyrB']
        TGN_aminoglicosidos = ['eis', 'gidB', 'rpsL',
                            'rrl', 'rrs', 'tap', 'tlyA', 'whiB7']
        TGN_linezolid = ['rrl', 'rplC']
        TGN_cicloserina = ['rrl', 'rplC']
        TGN_pas = ['thyA', 'ribD', 'folC']
        TGN_ethionamida = ['ethA', 'mshA', 'ndh', 'inhA', 'ethR',
                        'fabG1', 'mmaA3', 'mshC', 'mymA', 'nudC', 'Rv0565c']
        TGN_clofazimina = ['rv0678', 'pepQ', 'rv1979c', 'rv2535c', 'ndh']
        TGN_bedaquilina = ['rv0678', 'pepQ', 'atpE']
        TGN_delamanid = ['ddn', 'fbiA', 'fbiB', 'fbiC', 'fgd1']

        TGN_dic = {}
        TGN_dic['isoniazida'] = TGN_isoniazida
        TGN_dic['rifampicina'] = TGN_rifampicina
        TGN_dic['ethambutol'] = TGN_ethambutol
        TGN_dic['pirazinamida'] = TGN_pirazinamida
        TGN_dic['quinolonas'] = TGN_quinolonas
        TGN_dic['aminoglicosidos'] = TGN_aminoglicosidos
        TGN_dic['linezolid'] = TGN_linezolid
        TGN_dic['cicloserina'] = TGN_cicloserina
        TGN_dic['pas'] = TGN_pas
        TGN_dic['ethionamida'] = TGN_ethionamida
        TGN_dic['clofazimina'] = TGN_clofazimina
        TGN_dic['bedaquilina'] = TGN_bedaquilina
        TGN_dic['delamanid'] = TGN_delamanid

        return TGN_dic

    def antibioticResistanceAnalysis(self, path):
        """Realiza análisis de resistencia antibiótica para cada una de las muestras que se encuentran en la carpeta
        ingresada

        Parámetros
        ----------
        path : str
            La ruta del directorio donde se encuentran las carpetas de las muestras por país
        """
        VCF_version2 = False

        message = "INICIÓ EL ANÁLISIS DE RESISTENCIA ANTIBIÓTICA\n"
        self.arReport.write(f'{message}\n')
        print(message)

        TACH_isoniacida = ['S315I', 'S315N', 'S315T']
        TACH_rifampicina = ['L511P', 'Q513K', 'Q513L', 'Q513P', 'D516V', 'D516Y', 'S522L', 'S522Q', 'H526C', 'H526D',
                            'H526L', 'H526N', 'H526R', 'H526Y', 'S531L', 'S531W', 'L533P']
        TACH_fluoroquinolonas = ['A90V', 'S91P',
                                'D94A', 'D94G', 'D94H', 'D94N', 'D94Y']
        TGN_dic = self.getTGNDict()
        

        TGN_total = []
        for v in TGN_dic.values():
            TGN_total.extend([i.upper() for i in v])
            # TGN_total.extend(v)

        pos_index = 1
        ref_index = 3
        alt_index = 4
        info_index = 7

        folders = self.getFolders(path)

        for folder in folders:
            message = f"Procesando -> país: {folder.name}"
            self.arReport.write(f'{message}\n')
            print(message)

            arDirectoryName = f"{self.resultsFolder}/variants/{folder.name}/antibioticResistanceReports"

            try:
                xlsxFiles = self.getXlsxFiles(f"{self.resultsFolder}/variants/{folder.name}/xlsxFiles")
            except OSError as e:
                if(e.strerror == "No se puede crear un archivo que ya existe"):
                    message = "\tEl directorio se encuentra creado. Se sobreescribiran los datos"
                    self.arReport.write(f'{message}\n')
                    print(message)
                elif(e.strerror == "El sistema no puede encontrar la ruta especificada"):
                    message = "\tLa carpeta de documentos .xlsx no fue creada correctamente"
                    self.arReport.write(f'{message}\n')
                    print(message)
                    sys.exit()
                else:
                    message = f"\tError en la lectura de archivos .: {e.strerror}"
                    self.arReport.write(f'{message}\n')
                    print(message)
                    sys.exit()

            try:
                os.mkdir(arDirectoryName)
            except OSError as e:
                message = f"\tError en la creación de el directorio de resistecia antibiótica en la carpeta {folder.name}"
                self.arReport.write(f'{message}\n')
                print(message)

            for file in xlsxFiles:
                message = f"\tDocumento: {file.name}"
                self.arReport.write(f'{message}\n')
                print(message)

                fileName = file.name[0:-5]
                otherGenes = {}

                report = open(f"{arDirectoryName}/informe_resistencia_" + fileName + ".txt", "w")
                report.write(f"INFORME RESISTENCIA ANTIBIÓTICA:{fileName}{os.linesep}")
                report.write(f"\n{os.linesep}")

                xlsxFile = self.readXlsx(file.path)
                if xlsxFile:
                    info = xlsxFile[1][info_index]
                    info = [i.upper() for i in info]
                    pos = xlsxFile[1][pos_index]
                    ref = xlsxFile[1][ref_index]
                    alt = xlsxFile[1][alt_index]

                    res_isoniacida = False
                    res_rifampicina = False
                    res_fluoroquinolonas = False

                    for i in range(len(info)):
                        if VCF_version2:
                            array = info[i].split('|')
                            TACH_TGN = self.find_TACH_TGN2(array)

                            if TACH_TGN[0] in TACH_isoniacida:
                                res_isoniacida = True
                                reportMessage = "Según la prueba ANYPLEX la muestra " + fileName + \
                                    " es resistente a la isoniacida con la siguiente mutación: \n"
                                reportMessage += "POS=" + str(pos[i]) + "; REF=" + ref[i] + "; ALT=" + \
                                    alt[i] + "; TACH=" + TACH_TGN[0] + \
                                    "; TGN=" + TACH_TGN[1] + "\n"

                                report.write(reportMessage + os.linesep)

                                #print(carpeta.name + ":" + fileName + " - POS: " + str(pos[i]) + " - TACH: " + TACH_TGN[0] + " - TGN: " + TACH_TGN[1])
                            if TACH_TGN[0] in TACH_rifampicina:
                                res_rifampicina = True
                                reportMessage = "Según la prueba ANYPLEX la muestra " + fileName + \
                                    " es resistente a la rifampicina con la siguiente mutación: \n"
                                reportMessage += "POS=" + str(pos[i]) + "; REF=" + ref[i] + "; ALT=" + \
                                    alt[i] + "; TACH=" + TACH_TGN[0] + \
                                    "; TGN=" + TACH_TGN[1] + "\n"

                                report.write(reportMessage + os.linesep)

                            if TACH_TGN[0] in TACH_fluoroquinolonas:
                                res_fluoroquinolonas = True
                                reportMessage = "Según la prueba ANYPLEX la muestra " + fileName + \
                                    " es resistente a la fluoroquinolonas con la siguiente mutación: \n"
                                reportMessage += "POS=" + str(pos[i]) + "; REF=" + ref[i] + "; ALT=" + \
                                    alt[i] + "; TACH=" + TACH_TGN[0] + \
                                    "; TGN=" + TACH_TGN[1] + "\n"

                                report.write(reportMessage + os.linesep)

                            if TACH_TGN[1] in TGN_total:
                                if TACH_TGN[1] not in otherGenes.keys():
                                    otherGenes[TACH_TGN[1]] = [
                                        [str(pos[i]), ref[i], alt[i],  TACH_TGN[0]]]
                                else:
                                    otherGenes[TACH_TGN[1]].append(
                                        [str(pos[i]), ref[i], alt[i],  TACH_TGN[0]])


                        elif 'TACH' in info[i] and 'TGN' in info[i]:
                            array = info[i].split(';')
                            """ TACH_pos = encuentra_pos(arreglo, 'TACH')
                            TGN_pos = encuentra_pos(arreglo, 'TGN') """

                            TACH_TGN = self.find_TACH_TGN(array)
                            #print("1: " + TACH_TGN[0] + " - 2: " + TACH_TGN[1])

                            if TACH_TGN[0] in TACH_isoniacida:
                                res_isoniacida = True
                                reportMessage = "Según la prueba ANYPLEX la muestra " + fileName + \
                                    " es resistente a la isoniacida con la siguiente mutación: \n"
                                reportMessage += "POS=" + str(pos[i]) + "; REF=" + ref[i] + "; ALT=" + \
                                    alt[i] + "; TACH=" + TACH_TGN[0] + \
                                    "; TGN=" + TACH_TGN[1] + "\n"

                                report.write(reportMessage + os.linesep)

                                #print(carpeta.name + ":" + fileName + " - POS: " + str(pos[i]) + " - TACH: " + TACH_TGN[0] + " - TGN: " + TACH_TGN[1])
                            if TACH_TGN[0] in TACH_rifampicina:
                                res_rifampicina = True
                                reportMessage = "Según la prueba ANYPLEX la muestra " + fileName + \
                                    " es resistente a la rifampicina con la siguiente mutación: \n"
                                reportMessage += "POS=" + str(pos[i]) + "; REF=" + ref[i] + "; ALT=" + \
                                    alt[i] + "; TACH=" + TACH_TGN[0] + \
                                    "; TGN=" + TACH_TGN[1] + "\n"

                                report.write(reportMessage + os.linesep)

                            if TACH_TGN[0] in TACH_fluoroquinolonas:
                                res_fluoroquinolonas = True
                                reportMessage = "Según la prueba ANYPLEX la muestra " + fileName + \
                                    " es resistente a la fluoroquinolonas con la siguiente mutación: \n"
                                reportMessage += "POS=" + str(pos[i]) + "; REF=" + ref[i] + "; ALT=" + \
                                    alt[i] + "; TACH=" + TACH_TGN[0] + \
                                    "; TGN=" + TACH_TGN[1] + "\n"

                                report.write(reportMessage + os.linesep)

                            if TACH_TGN[1] in TGN_total:
                                if TACH_TGN[1] not in otherGenes.keys():
                                    otherGenes[TACH_TGN[1]] = [
                                        [str(pos[i]), ref[i], alt[i],  TACH_TGN[0]]]
                                else:
                                    otherGenes[TACH_TGN[1]].append(
                                        [str(pos[i]), ref[i], alt[i],  TACH_TGN[0]])

                    if not res_isoniacida:
                        reportMessage = "¡Según la prueba ANYPLEX la muestra " + \
                            fileName + " es sensible a la isoniacida!\n"
                        report.write(reportMessage + os.linesep)
                    if not res_rifampicina:
                        reportMessage = "¡Según la prueba ANYPLEX la muestra " + \
                            fileName + " es sensible a la rifampicina!\n"
                        report.write(reportMessage + os.linesep)
                    if not res_fluoroquinolonas:
                        reportMessage = "¡Según la prueba ANYPLEX la muestra " + \
                            fileName + " es sensible a la fluoroquinolonas!\n"
                        report.write(reportMessage + os.linesep)

                    reportMessage = " -------------------------------------------------------------------------------------------------------------------------- \n"
                    reportMessage += " -------------------------------------------------------------------------------------------------------------------------- \n"
                    report.write(reportMessage + os.linesep)

                    if not res_isoniacida and not res_rifampicina and not res_fluoroquinolonas:
                        reportMessage = "¡La muestra " + fileName + " es: TUBERCULOSIS SENSIBLE!\n"
                        report.write(reportMessage + os.linesep)
                    if res_isoniacida:
                        reportMessage = "¡La muestra " + fileName + " es: TUBERCULOSIS MDR!\n"
                        report.write(reportMessage + os.linesep)
                    if res_isoniacida and res_fluoroquinolonas:
                        reportMessage = "¡La muestra " + fileName + " es: TUBERCULOSIS XDR!\n"
                        report.write(reportMessage + os.linesep)

                    for antk in TGN_dic.keys():
                        reportMessage = antk.upper() + ":"
                        reportMessage += " -------------------------------------------------------------------------------------------------------------------------- "
                        report.write(reportMessage + os.linesep)
                        reportMessage = ""
                        for g in TGN_dic[antk]:
                            #print("gen g: " + g + " - otros genes: " + str(otherGenes.keys()))
                            g = g.upper()
                            if g in otherGenes.keys():
                                reportMessage = "Se encontró una mutación en el gen " + g + ":\n"
                                for o in otherGenes[g]:
                                    reportMessage += "POS=" + \
                                        o[0] + "; REF=" + o[1] + "; ALT=" + \
                                        o[2] + "; TACH=" + o[3] + "\n"
                                report.write(reportMessage + os.linesep)
                            """ else:
                                reportMessage = "NO se encontró una mutación en el gen " + g + "\n"
                                informe.write(reportMessage + os.linesep) """
                        report.write("\n" + os.linesep)
                else:
                    message = "\t\tEste documento está vacío"
                    self.arReport.write(f'{message}\n')
                    print(message)

            report.close()
        message = "FINALIZÓ EL ANÁLISIS DE RESISTENCIA ANTIBIÓTICA\n"
        message += "------------------------------------------\n"
        self.arReport.write(f'{message}\n')
        print(message)

    def endARReport(self):
        self.arReport.write("\nFINAL DEL REPORTE\n")
        self.arReport.close()
