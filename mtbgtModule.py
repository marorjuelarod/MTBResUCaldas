import re
import os
import sys
import glob
import MTBGT_Tests as mtbgtt
import MTBGT_IO as mtbgtio

class MTBGTModule():
    def __init__(self, resultsFolder, map):
        self.resultsFolder = resultsFolder
        self.folder = f"{resultsFolder}/variants"
        self.map = map

        self.mtbgtReport = open(f"{resultsFolder}/executionReports/mtbgtreport.txt", 'w')
        self.mtbgtReport.write("REPORTE DE EJECUCIÓN: Reporte del análisis MTBGT\n\n")

        self.MTBGTAnalysis(self.folder, map)

        self.endMTBGTReport()

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

    
    def MTBGTAnalysis(self, folder, map):
        message = "INICIÓ EL ANÁLISIS MTBGT\n"
        self.mtbgtReport.write(f'{message}\n')
        print(message)

        #read in map file 
        try:
            mapf=open(map, 'r')
        except IOError:
            message = "\n\tArchivo map no encontrado"
            self.mtbgtReport.write(f'{message}\n')
            print(message)
            sys.exit()
        
        #read in map and create a dictionary of the codons to genome positions
        #each key is a position and the value is the codon_position (e.g. position 1 in the 450 codon is 450_1)
        mapdict={}
        genomePos=[]
        while 1:
            line=mapf.readline()
            if not line:
                break
            line=line.rstrip()
            if re.match("Codon",line):#on an info line so skip
                continue
            sections=line.split("\t")
            pos=sections[1]
            mapdict[pos]=sections[0]+"_0"
            mapdict[str(int(pos)+1)]=sections[0]+"_1"
            mapdict[str(int(pos)+2)]=sections[0]+"_2"
            genomePos.append(pos)
            genomePos.append(str(int(pos)+1))
            genomePos.append(str(int(pos)+2))
            codonpos=mapdict.keys() #get a list of all the genome positions, grouped as triplets
        mapf.close()

        carpetas = self.getFolders(folder)
        sampleGenomePos = []

        for carpeta in carpetas:
            message = f"Procesando -> {carpeta.name}"
            self.mtbgtReport.write(f'{message}\n')
            print(message)
            
            currentSample = mtbgtio.tabInput(genomePos,f'{carpeta.path}/tabFiles/')
            
            sampleGenomePos.append(currentSample)

            message = "\n\tProcesando Tests:"
            self.mtbgtReport.write(f'{message}\n')
            print(message)
            
            #run the modules as requested by the user
            tests={"H":1, "U":1, "X":1, "N":1, "S":1,}

            if tests["X"]==1:
                message = "\t\tCreating classic Xpert outputs"
                self.mtbgtReport.write(f'{message}\n')
                print(message)	
                
                mtbgtt.xpert(mapdict, currentSample, f'{carpeta.path}/tabFiles/GenomeInfo')
            if tests["U"]==1:
                message = "\t\tCreating Xpert Ultra outputs"
                self.mtbgtReport.write(f'{message}\n')
                print(message)
                
                mtbgtt.ultra(mapdict, currentSample, f'{carpeta.path}/tabFiles/GenomeInfo')
            if tests["H"]==1:
                message = "\t\tCreating Hain LPA outputs"
                self.mtbgtReport.write(f'{message}\n')
                print(message)
                
                mtbgtt.hain(mapdict, currentSample, f'{carpeta.path}/tabFiles/GenomeInfo')
            if tests["N"]==1:
                message = "\t\tCreating Nipro LPA outputs"
                self.mtbgtReport.write(f'{message}\n')
                print(message)

                mtbgtt.nipro(mapdict, currentSample, f'{carpeta.path}/tabFiles/GenomeInfo')
            if tests["S"]==1:
                message = "\t\tCreating rpoB Sanger sequencing outputs"
                self.mtbgtReport.write(f'{message}\n')
                print(message)	
                
                mtbgtt.sanger(mapdict, currentSample, f'{carpeta.path}/tabFiles/GenomeInfo')

            message = "\t\tRDT test conversion complete"
            self.mtbgtReport.write(f'{message}\n')
            print(message)

            #Create tables as requested by the user
            message = "\t\tCreating summary tables"
            self.mtbgtReport.write(f'{message}\n')
            print(message)
            

            mtbgtio.tables(tests, f'{carpeta.path}/tabFiles/GenomeInfo')

        message = "FINALIZÓ EL ANÁLISIS MTBGT\n"
        message += "------------------------------------------\n"
        self.mtbgtReport.write(f'{message}\n')
        print(message)

    def endMTBGTReport(self):
        self.mtbgtReport.write("\nFINAL DEL REPORTE\n")
        self.mtbgtReport.close()

