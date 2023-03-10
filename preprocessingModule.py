#!/usr/bin/env python
import os
import re
import sys
import tabManagement as tab
import pandas as pd
from pandas import ExcelWriter

class PreprocessingModule():
    def __init__(self, resultsFolder, folder):
        self.resultsFolder = resultsFolder
        self.folder = folder
        
        reportMessage = self.createVariantsResultsFolder()

        self.ppReport = open(f"{resultsFolder}/executionReports/ppreport.txt", 'w')
        self.ppReport.write("REPORTE DE EJECUCIÓN: Reporte de preprocesamiento\n\n")
        self.ppReport.write(reportMessage)

        self.createXLSXFiles(folder)
        self.createTABFiles(folder)

        self.endPPReport()
    
    def createVariantsResultsFolder(self):
        message = "Creando carpeta de resultados de preprocesamiento de variantes ..."
        reportMessage = f'{message}\n'
        print(message)
        try:
            os.mkdir(f"{self.resultsFolder}/variants")
            reportMessage += "\tSe creó la carpeta exitosamente\n"
            return reportMessage
        except OSError as e:
            if(e.strerror == "No se puede crear un archivo que ya existe"):
                message = "\tEl directorio de resultados ya existe. se sobreescribirán los datos"
                reportMessage += f'{message}\n'
                print(message)
            else:
                message = f"\tError en la creación del directorio de resultados: {e.strerror}"
                reportMessage += f'{message}\n'
                print(message)
                self.endIOReport()
                sys.exit()
            return reportMessage


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

    def getVCFFiles(self, path):
        """Obtiene una lista de archivos con formato .vcf que se encuentran en un directorio dado.

        Parametros
        ----------
        path : str
            La ruta o el directorio del cual se quiere obtener los archivos internos.

        Retorna
        -------
        archivos
            una lista de archivos con formato .vcf
        """
        with os.scandir(path) as content:
            files = [file for file in content if file.is_file(
            ) and file.name.endswith('.vcf')]
        return files


    def createXLSXFiles(self, path):
        """Crea documentos con formato .xlsx (excel) para cada muestra en subcarpetas para cada país donde 
        se almacenan las posiciones de ADN con filtro "PASS"

        Parametros
        ----------
        path : str
            La ruta del directorio donde se encuentran las carpetas de las muestras por país
        """
        message = "INICIÓ EL FILTRADO DE MUESTRAS Y CREACIÓN DE DOCUMENTOS .xlsx\n"
        self.ppReport.write(f'{message}\n')
        print(message)

        vcfFiles = []
        folders = self.getFolders(path)

        for folder in folders:
            message = f"Procesando -> país: {folder.name}"
            self.ppReport.write(f'{message}\n')
            print(message)

            try:
                os.mkdir(f"{self.resultsFolder}/variants/{folder.name}")
                os.mkdir(f"{self.resultsFolder}/variants/{folder.name}/xlsxFiles")
            except OSError as e:
                if(e.strerror == "No se puede crear un archivo que ya existe"):
                    message = "\tUno de los directorios en la ruta del directorio donde se almacenaran los documentos .xlsx ya existe. Se sobreescribiran los datos"
                    self.ppReport.write(f'{message}\n')
                    print(message)
                else:
                    message = f"\tError en la creación del directorio de documentos .xlsx: {e.strerror}"
                    self.ppReport.write(f'{message}\n')
                    print(message)

            vcfFiles = self.getVCFFiles(folder.path)
            for vcfFile in vcfFiles:
                message = f"\tArchivo: {vcfFile.name}"
                self.ppReport.write(f'{message}\n')
                print(message)

                file = open(vcfFile.path, 'r')
                table = {}
                data = []
                titles = []
                for line in file:
                    if (line[0:2] != "##"):
                        if (line[0:1] == '#'):
                            titles = re.split("\t", line[1:len(line)-1])
                        else:
                            array = re.split("\t", line[0:len(line)])
                            if array[6].lower() == "pass":
                                if array[-1][-1] == '\n':
                                    array[-1] = array[-1][0:-1]
                                data.append(array)
                k = 0
                for title in titles:
                    column = []
                    for row in data:
                        column.append(row[k])
                    table[title] = column
                    k += 1

                if "_" in vcfFile.name:
                    xlsxName = f"{vcfFile.name[0:vcfFile.name.find('_')]}.xlsx"
                else:
                    xlsxName = f"{vcfFile.name[0:-4]}.xlsx"

                xlsxFolderPath = f"{self.resultsFolder}/variants/{folder.name}/xlsxFiles"
                pathXlsx = f"{xlsxFolderPath}/{xlsxName}"
                df = pd.DataFrame(table, columns=titles)
                writer = ExcelWriter(pathXlsx)
                df.to_excel(writer, 'Hoja1', index=False)
                writer.save()
            print()
        message = "FINALIZÓ EL FILTRADO DE MUESTRAS Y CREACIÓN DE DOCUMENTOS .xlsx\n"
        message += "------------------------------------------\n"
        self.ppReport.write(f'{message}\n')
        print(message)
    
    def createTABFiles(self, path):
        vcfFiles = []
        folders = self.getFolders(path)

        message = "INICIÓ DE CREACIÓN DE DOCUMENTOS .tab\n"
        self.ppReport.write(f'{message}\n')
        print(message)

        for folder in folders:
            message = f"Procesando -> país: {folder.name}"
            self.ppReport.write(f'{message}\n')
            print(message)

            try:
                os.mkdir(f"{self.resultsFolder}/variants/{folder.name}")
            except OSError as e:
                if(e.strerror == "No se puede crear un archivo que ya existe"):
                    message = "\tUno de los directorios en la ruta del directorio donde se almacenaran los documentos .tab ya existe. Se sobreescribiran los datos"
                    self.ppReport.write(f'{message}\n')
                    print(message)
                else:
                    message = f"\tError en la creación del directorio de documentos .tab: {e.strerror}"
                    self.ppReport.write(f'{message}\n')
                    print(message)

            try:
                os.mkdir(f"{self.resultsFolder}/variants/{folder.name}/tabFiles")
            except OSError as e:
                if(e.strerror == "No se puede crear un archivo que ya existe"):
                    message = "\tUno de los directorios en la ruta del directorio donde se almacenaran los documentos .tab ya existe. Se sobreescribiran los datos"
                    self.ppReport.write(f'{message}\n')
                    print(message)
                else:
                    message = f"\tError en la creación del directorio de documentos .tab: {e.strerror}"
                    self.ppReport.write(f'{message}\n')
                    print(message)

            vcfFiles = self.getVCFFiles(folder.path)
            for vcfFile in vcfFiles:
                message = f"\tArchivo: {vcfFile.name}"
                self.ppReport.write(f'{message}\n')
                print(message)

                file = open(vcfFile.path, 'r')
                data = []
                titles = []
                for line in file:
                    if (line[0:2] != "##"):
                        if (line[0:1] == '#'):
                            titles = re.split("\t", line[1:len(line)-1])
                        else:
                            array = re.split("\t", line[0:len(line)])
                            if array[6].lower() == "pass":
                                if array[-1][-1] == '\n':
                                    array[-1] = array[-1][0:-1]
                                data.append(array)

                if "_" in vcfFile.name:
                    tabName = f"{vcfFile.name[0:vcfFile.name.find('_')]}.tab"
                else:
                    tabName = f"{vcfFile.name[0:-4]}.tab"
                tabFilePath = f'{self.resultsFolder}/variants/{folder.name}/tabFiles/{tabName}'
                tabFile = open(tabFilePath, "w")
                for info in tab.getTABData(data, self.ppReport):
                    tabFile.write( "\t".join( info ) )
                    tabFile.write( "\n" )
                tabFile.close()
            print()
        message = "FINALIZÓ LA CREACIÓN DE DOCUMENTOS .tab\n"
        message += "------------------------------------------\n"
        self.ppReport.write(f'{message}\n')
        print(message)


    def endPPReport(self):
        self.ppReport.write("\nFINAL DEL REPORTE\n")
        self.ppReport.close()
