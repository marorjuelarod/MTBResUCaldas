import os
import sys
import pandas as pd
from pandas import ExcelWriter



class MutationSensibilityModule():
    def __init__(self, resultsFolder, folder, resFile):
        self.resultsFolder = resultsFolder
        self.folder = folder

        self.msReport = open(f"{resultsFolder}/executionReports/msreport.txt", 'w')
        self.msReport.write("REPORTE DE EJECUCIÓN: Reporte de mutaciones y sensibilidad\n\n")

        self.analisis_resistencia(folder, resFile, "")

        self.endMSReport()
    
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


    def cleanRepeated(self, TGN_TACH, ANTI, GENE, DESC):
        """obtiene los TACH, TGN, LOS GENES, Y ANTIBIÓTICOS sin repetición

        Parámetros
        ----------
        TGN_TACH : list
            Lista de TGN y de TACH
        ANTI :  list
            Lista de antibióticos
        GENE : list
            Lista de genes

        Retorna
        -------
        Matriz
            TACH, TGN, LOS GENES, Y ANTIBIÓTICOS sin repetición
        """

        TGN_TACH_ANTI = []
        new_TGN_TACH = []
        new_ANTI = []
        new_DESC = []
        for i, j, k in zip(TGN_TACH, ANTI, DESC):
            if [i, j] not in TGN_TACH_ANTI:
                TGN_TACH_ANTI.append([i, j])
                new_TGN_TACH.append(i)
                new_ANTI.append(j)
                new_DESC.append(k)
        new_gene = []
        for i in GENE:
            if i not in new_gene:
                new_gene.append(i)
        return [new_TGN_TACH, new_ANTI, new_gene, new_DESC]

    def cleanAntiRepeated(self, antis):
        """Obtiene una lista de antibióticos sin repetir

        Parametros
        ----------
        antis: list
            lista de antibióticos

        Retorna
        -------
        lista
            una lista de antibióticos sin repetir
        """
        antiList = []
        for anti in antis:
            if anti not in antiList:
                antiList.append(anti)
        return antiList


    def readResFile(self, xlsxPath):
        """Lee el archivo de excel de referencia y obtiene los TACH, TGN, LOS GENES, Y ANTIBIÓTICOS
        sin repetición

            Parámetros
            ----------
            xlsxPath : str
                La ruta o el directorio del excel de referencia

            Retorna
            -------
            TACH, TGN, LOS GENES, Y ANTIBIÓTICOS
        """
        message = "Leyendo archivo excel de referencia ..."
        self.msReport.write(f'{message}\n')
        print(message)

        df = pd.read_excel(xlsxPath, sheet_name="Mutaciones_resistencia")
        keys = df.to_dict().keys()
        values = df.to_dict().values()
        TGN = [i.upper() for i in list(values)[0].values()]
        TACH = [i.upper() for i in list(values)[1].values()]

        TGN_TACH = []
        for i, j in zip(TGN, TACH):
            TGN_TACH.append([i, j])

        ANTI = [i.upper() for i in list(values)[2].values()]
        GENE = [str(i).upper() for i in list(values)[3].values() if str(i).upper() != "NAN"]
        DESC = [i.upper() for i in list(values)[4].values()]

        if TGN != [] and TACH != [] and ANTI != [] and DESC != []:
            message = "\tEl archivo fue correctamente leído\n"
            self.msReport.write(f'{message}\n')
            print(message)
            return self.cleanRepeated(TGN_TACH, ANTI, GENE, DESC)
        else:
            message = "\tEl archivo no fue correctamente leído. Es posible que tenga uno o más campos vacíos\n"
            self.msReport.write(f'{message}\n')
            print(message)
            return None

    def filesWriting(self, antibiotics, countriesDict, country=None, path=None):
        message = "\tPreparandose para la creación de documentos .xlsx ..."
        self.msReport.write(f'{message}\n')
        print(message)

        resTable = {}
        resTable["PAIS"] = []
        resTable["MUESTRA"] = []

        senTable = {}
        senTable["PAIS"] = []
        senTable["MUESTRA"] = []
        
        mutTable = {}
        mutTable["PAIS"] = []
        mutTable["MUESTRA"] = []
        mutTable["MUTACIONES"] = []
        titulos_m = ["PAIS", "MUESTRA", "MUTACIONES"]

        titles = ["PAIS", "MUESTRA"]

        for antibiotic in antibiotics:
            resTable[antibiotic] = []
            senTable[antibiotic] = []
            titles.append(antibiotic)

        for countryK, sampleDictV in countriesDict.items():
            if country:
                if country == countryK:
                    auxDict = countriesDict[countryK]
                    for sample, [sensDictV, resDictV, mutListV] in auxDict.items():
                        resTable["PAIS"].append(country)
                        resTable["MUESTRA"].append(sample)
                        
                        senTable["PAIS"].append(country)
                        senTable["MUESTRA"].append(sample)
                        
                        mutTable["PAIS"].append(country)
                        mutTable["MUESTRA"].append(sample)
                        mutTable["MUTACIONES"].append(";".join(mutListV))

                        for antibiotic in antibiotics:
                            if antibiotic in sensDictV.keys():
                                senTable[antibiotic].append(sensDictV[antibiotic])
                            else:
                                senTable[antibiotic].append("NA")
                            
                            if antibiotic in resDictV.keys():
                                resTable[antibiotic].append(resDictV[antibiotic])
                            else:
                                resTable[antibiotic].append("NA")
            else:
                for sample, [sensDictV, resDictV, mutListV] in sampleDictV.items():
                    resTable["PAIS"].append(countryK)
                    resTable["MUESTRA"].append(sample)
                    
                    senTable["PAIS"].append(countryK)
                    senTable["MUESTRA"].append(sample)

                    mutTable["PAIS"].append(countryK)
                    mutTable["MUESTRA"].append(sample)
                    mutTable["MUTACIONES"].append(";".join(mutListV))
                    
                    for antibiotic in antibiotics:
                        if antibiotic in sensDictV.keys():
                            senTable[antibiotic].append(sensDictV[antibiotic])
                        else:
                            senTable[antibiotic].append("NA")
                        
                        if antibiotic in resDictV.keys():
                            resTable[antibiotic].append(resDictV[antibiotic])
                        else:
                            resTable[antibiotic].append("NA")


        message = "\t\tCreando tabla de genes resistentes ..."
        self.msReport.write(f'{message}\n')
        print(message)

        xlsxName = 'registro_mutaciones.xlsx'
        if path:
            xlsxWritePath = path + "/" + xlsxName
        else:
            xlsxWritePath = f"{self.resultsFolder}/{xlsxName}"

        df = pd.DataFrame(resTable, columns = titles)
        writer = ExcelWriter(xlsxWritePath)
        df.to_excel(writer, 'Hoja1', index = False)
        writer.save()

        message = "\t\tCreando tabla de sensibilidad ..."
        self.msReport.write(f'{message}\n')
        print(message)

        xlsxName = 'registro_sensibilidad.xlsx'
        if path:
            xlsxWritePath = path + "/" + xlsxName
        else:
            xlsxWritePath = f"{self.resultsFolder}/{xlsxName}"

        df = pd.DataFrame(senTable, columns = titles)
        writer = ExcelWriter(xlsxWritePath)
        df.to_excel(writer, 'Hoja1', index = False)
        writer.save()

        message = "\t\tCreando tabla de solo mutaciones ..."
        self.msReport.write(f'{message}\n')
        print(message)

        xlsxName = 'registro_solo_mutaciones.xlsx'
        if path:
            xlsxWritePath = path + "/" + xlsxName
        else:
            xlsxWritePath = f"{self.resultsFolder}/{xlsxName}"

        df = pd.DataFrame(mutTable, columns = titulos_m)
        writer = ExcelWriter(xlsxWritePath)
        df.to_excel(writer, 'Hoja1', index = False)
        writer.save()

    def anomaliesReport(self, anomaliesDict, country, path):
        """Genera un informe con las anomalías que se tuvieron 

        Parámetros
        ----------
        anomaliesDict
            Diccionario con información de anomalías por país
        country
            país del cual se quiere generar el reporte de anomalías
        path
            ruta donde se desea guardar el reporte
        """
        reportMessage = "PAÍS: " + country + "\n"
        samplesDict = anomaliesDict[country]
        for sample, anomalies in samplesDict.items():
            reportMessage += "MUESTRA: " + sample + "\n"
            for anomaly in anomalies:
                reportMessage += "TGN: " + anomaly[0] + " - TACH: " + anomaly[1] + "\n"
            reportMessage += "\n----------------------------------------\n\n"
        
        report = open(path + "/informe_anomalias.txt", "w")
        report.write(reportMessage)
        report.close()

    def encuentra_TGN_TACH(self, arreglo):
        """Encuentra la sección de un arreglo correspondiente al TGN y al TACH

        Parámetros
        ----------
        arreglo
            arreglo con diferentes propiedades de un gen

        Retorna
        -------
            Valor del TACH y del TGN
        """
        TGN_TACH = [0, 0]
        for a in arreglo:
            if 'TACH' in a:
                TGN_TACH[1] = a[a.index('=')+1:]
            elif 'TGN' in a:
                TGN_TACH[0] = a[a.index('=')+1:]
            
            if TGN_TACH[0] != 0 and TGN_TACH[1] != 0:
                return TGN_TACH
        return None


    def analisis_resistencia(self, nombre_carpeta, nombre_excel, nombre_hoja):
        message = "INICIÓ EL ANÁLISIS DE MUTACIÓN-SENSIBILIDAD\n"
        self.msReport.write(f'{message}\n')
        print(message)

        referencias = self.readResFile(nombre_excel)
        antibioticos = self.cleanAntiRepeated(referencias[1])
        genes = referencias[2]
        descriptions = referencias[3]

        """ genes2 = []
        [genes2.append(i[0]) for i in referencias[0] if i[0] not in genes2]
        gen_verificacion = [False for i in range(len(genes2))] """

        carpetas = self.getFolders(nombre_carpeta)

        info_index = 7
        dic_paises = {}
        anomalias_pais = {}

        globalMedicalSignificanceReport = open(f"{self.resultsFolder}/medicalSignificanceReport.txt", "w")
        globalMedicalSignificanceReport.write(f"REPORTE DE SIGNIFICANCIA CLÍNICA GLOBAL\n\n")

        for carpeta in carpetas:
            print("Procesando -> pais: " + carpeta.name)
            
            documentos_excel = self.getXlsxFiles(f"{self.resultsFolder}/variants/{carpeta.name}/xlsxFiles")

            anomalias_muestra = {}
            anomalias_pais[carpeta.name] = anomalias_muestra

            dic_muestra = {}
            dic_paises[carpeta.name] = dic_muestra

            globalMedicalSignificanceReport.write(f"{carpeta.name}:\n")

            medicalSignificanceReport = open(f"{self.resultsFolder}/variants/{carpeta.name}/medicalSignificanceReport.txt", "w")
            medicalSignificanceReport.write(f"REPORTE DE SIGNIFICANCIA CLÍNICA: {carpeta.name}\n\n")

            for documento in documentos_excel:
                escribeMuestra = False
                escribeSeparador = False

                nombre_archivo = documento.name[0:-5]
                documento_excel = self.readXlsx(documento.path)

                lista_anomalias = []
                anomalias_muestra[nombre_archivo] = lista_anomalias

                dic_sensibilidad = {}
                dic_mutaciones = {}
                lista_mutaciones = []
                dic_muestra[nombre_archivo] = [
                    dic_sensibilidad, dic_mutaciones, lista_mutaciones]
                
                if documento_excel:
                    info = documento_excel[1][info_index]
                    info = [i.upper().split(';') for i in info]

                    print("\tleyendo muestra " + nombre_archivo)
                    for i in info:
                        TGN_TACH = self.encuentra_TGN_TACH(i)
                        if TGN_TACH:
                            if TGN_TACH in referencias[0]:
                                #gen_verificacion[genes2.index(TGN_TACH[0])] = True
                                ref_index = referencias[0].index(TGN_TACH)
                                anti = referencias[1][ref_index]
                                description = referencias[3][ref_index]

                                if not escribeMuestra:
                                    escribeMuestra = True
                                    globalMedicalSignificanceReport.write(f"\t{nombre_archivo}\n")
                                    medicalSignificanceReport.write(f"Muestra: {nombre_archivo}\n")

                                globalMedicalSignificanceReport.write(f"\t\tGen -> {TGN_TACH[0]} \t- \tMutación -> {TGN_TACH[1]} \t - \t{description}\n")
                                medicalSignificanceReport.write(f"\tGen -> {TGN_TACH[0]} \t- \tMutación -> {TGN_TACH[1]} \t - \t{description}\n")
                                escribeSeparador = True

                                if anti not in dic_mutaciones.keys():
                                    dic_mutaciones[anti] = "TGN=" + \
                                        TGN_TACH[0] + " TACH=" + TGN_TACH[1]
                                else:
                                    dic_mutaciones[anti] += "; TGN=" + \
                                        TGN_TACH[0] + " TACH=" + TGN_TACH[1]
                                lista_mutaciones.append(
                                    "TGN=" + TGN_TACH[0] + " TACH=" + TGN_TACH[1])
                            elif TGN_TACH[0] in genes:  # genes2
                                lista_anomalias.append(TGN_TACH)

                    for antibiotico in antibioticos:
                        if antibiotico in dic_mutaciones.keys():
                            dic_sensibilidad[antibiotico] = "Resistente"
                        else:
                            dic_sensibilidad[antibiotico] = "Sensible"
                else:
                    print("\n\n\tnombre: " + nombre_archivo + " no se pudo leer")
                
                if escribeSeparador:
                    globalMedicalSignificanceReport.write("\n\t----------\n\n")
                    medicalSignificanceReport.write("\n----------\n\n")
                

            self.filesWriting(antibioticos, dic_paises,
                                country=carpeta.name, path=f"{self.resultsFolder}/variants/{carpeta.name}")
            # self.anomaliesReport(anomalias_pais, carpeta.name, f"{self.resultsFolder}/variants/{carpeta.name}")

            medicalSignificanceReport.close()
            globalMedicalSignificanceReport.write("\n..................................................\n\n")

        """ print(genes2)
        print("--------")
        print(gen_verificacion) """

        self.filesWriting(antibioticos, dic_paises)

        message = "FINALIZÓ EL ANÁLISIS DE MUTACIÓN-SENSIBILIDAD\n"
        message += "------------------------------------------\n"
        self.msReport.write(f'{message}\n')
        print(message)

        globalMedicalSignificanceReport.close()

    
    
    def endMSReport(self):
        self.msReport.write("\nFINAL DEL REPORTE\n")
        self.msReport.close()
