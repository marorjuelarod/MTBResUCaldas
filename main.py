import ioModule as io
import preprocessingModule as pp
import antibioticResistanceModule as ar
import mutationSensibilityModule as ms
import mtbgtModule as mtbgt

if __name__ == '__main__':
    resultsFolder = "./results"
    ioModule = io.IOModule(resultsFolder)
    args = ioModule.args
    ppMod = pp.PreprocessingModule(resultsFolder, args['folder'])
    arMod = ar.AntibioticResistanceModule(resultsFolder, args['folder'])
    msMod = ms.MutationSensibilityModule(resultsFolder, args['folder'], args['resFile'])
    mtbgtMod = mtbgt.MTBGTModule(resultsFolder, args['map'])

