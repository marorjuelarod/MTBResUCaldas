#!/usr/bin/env python
import os
import sys
import argparse

class IOModule():
    def __init__(self, resultsFolder):
        self.resultsFolder = resultsFolder
        initialArgs = self.inputInfo()

        reportMessage = self.createResultsFolder()
        reportMessage += self.initIOReport()
        self.ioReport = open(f"{resultsFolder}/executionReports/ioreport.txt", 'w')
        self.ioReport.write("REPORTE DE EJECUCIÓN: Reporte de valores ingresados\n\n")
        self.ioReport.write(reportMessage)

        self.args = self.validateInput(initialArgs)

        self.endIOReport()

    def inputInfo(self):
        #parse the inputs
        parser = argparse.ArgumentParser()
        parser.add_argument('--folder', required=False, default="variants", help='Folder containing the countries folders with vcf files to be processed (default is "variants" supplied with script)')
        parser.add_argument('--resFile', required=False, default="Mutaciones_resistencia_programa.xlsx", help='File containing the relationship between genes and antibiotic resistance (default is "Mutaciones_resistencia_programa.xlsx" supplied with script)')
        parser.add_argument('--map', required=False, default="default_mapfile.txt", help='File listing the relationship between codon and genome position (default is "default_mapfile.txt" supplied with script)')
        parser.add_argument('--tests', required=False, default="all", help='The different tests to run (see helpfile)')
        parser.add_argument('--summary', required=False, default="Y", help='Option to create an tab delimited overview tables file')

        return parser.parse_args()

    def validateInput(self, args):
        message = '\nValidando argumentos de entrada ...'
        self.ioReport.write(f'{message}\n')
        print(message)

        folder = self.validateFolder(args.folder)
        resFile = self.validateResFile(args.resFile)
        map = self.validateMap(args.map)
        tests = self.validateTests(args.tests)
        summary = self.validateSummary(args.summary)
        validatedArgs = {'folder': folder, 'resFile': resFile, 'map': map, 'tests': tests, 'summary': summary}
        return validatedArgs

    def validateFolder(self, folder):
        if(os.path.isdir(folder)):
            message = f'\tCarpeta válida: {folder}'
            self.ioReport.write(f'{message}\n')
            print(message)
            return folder
        else:
            message = f'\tCarpeta inválida: {folder}'
            self.ioReport.write(f'{message}\n')
            print(message)
            self.endIOReport()
            sys.exit()

    def validateResFile(self, resFile):
        if(os.path.isfile(resFile)):
            message = f'\tArchivo de relación de resistencia gen-antibiótico válido: {resFile}'
            self.ioReport.write(f'{message}\n')
            print(message)
            return resFile
        else:
            message = f'\tArchivo de relación de resistencia gen-antibiótico inválido: {resFile}'
            self.ioReport.write(f'{message}\n')
            print(message)
            self.endIOReport()
            sys.exit()

    def validateMap(self, map):
        if(os.path.isfile(map)):
            message = f'\tArchivo de relación de codon-genoma válido: {map}'
            self.ioReport.write(f'{message}\n')
            print(message)
            return map
        else:
            message = f'\tArchivo de relación de codon-genoma inválido: {map}'
            self.ioReport.write(f'{message}\n')
            print(message)
            self.endIOReport()
            sys.exit()
            
    def validateTests(self, tests):
        if(tests.upper() == "" or tests.upper() == None):
            message = '\tRealiza todos los tests'
            self.ioReport.write(f'{message}\n')
            return "ALL"
        else:
            testLetters=list(tests.upper())
            returnTests = ""
            for letter in testLetters:
                if(letter == "H" or letter == "U" or letter == "X" or letter == "N" or letter == "S"):
                    returnTests += letter
            if(returnTests == ""):
                message = '\tRealiza todos los tests'
                self.ioReport.write(f'{message}\n')
                returnTests = "ALL"
            else:
                message = f'\tRealiza los tests: {returnTests}'
                self.ioReport.write(f'{message}\n')
            return returnTests

    def validateSummary(self, summary):
        if(summary.upper() == "Y" or summary.upper() == "YES"):
            message = '\tRealiza resumen de archivos .tab'
            self.ioReport.write(f'{message}\n')
            return 'Y'
        else:
            message = '\tNo realiza resumen de archivos .tab'
            self.ioReport.write(f'{message}\n')
            return 'N'

    def createResultsFolder(self):
        message = "Creando carpeta de resultados ..."
        reportMessage = f'{message}\n'
        print(message)
        try:
            os.mkdir(f"{self.resultsFolder}")
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

    def initIOReport(self):
        message = "Creando carpeta de reportes de ejecución ..."
        reportMessage = f'{message}\n'
        print(message)
        try:
            os.mkdir(f"{self.resultsFolder}/executionReports")
            reportMessage += "\tSe creó la carpeta exitosamente\n"
            return reportMessage
        except OSError as e:
            if(e.strerror == "No se puede crear un archivo que ya existe"):
                message = "\tEl directorio de reportes de ejecución ya existe. Se sobreescribirán los datos"
                reportMessage += f'{message}\n'
                print(message)
            else:
                message = f"\tError en la creación del directorio de reportes de ejecución: {e.strerror}"
                reportMessage += f'{message}\n'
                print(message)
                self.endIOReport()
                sys.exit()
            return reportMessage

    def endIOReport(self):
        self.ioReport.write("\nFINAL DEL REPORTE\n")
        self.ioReport.close()

