from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

# Choose py/hw
MC='hw'
# Choose ak4/ak8
Mode='ak8'
Tag=''
if Mode=='ak8':
  Tag='_AK8'

config.General.transferOutputs = True
config.General.transferLogs = False
config.General.workArea = 'runs'

config.JobType.pluginName = 'Analysis'

config.Data.splitting = 'FileBased'
config.Data.inputDBS = 'global'
config.Data.outLFNDirBase = '/store/user/hsiikone'
config.Data.publication = False

config.Site.storageSite = 'T2_FI_HIP'

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.General.workArea = 'crab_projects'

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    if MC=='hw':
      config.JobType.psetName = 'cfg/'+Mode+'16hw.py'

      # Herwig++ Flat
      config.General.requestName = 'QCD16'+Tag+'_HS1_Flat_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)
    elif MC=='py':
      config.JobType.psetName = 'cfg/'+Mode+'16py.py'

      ##### Pythia 8 Flat
      config.General.requestName = 'QCD16'+Tag+'_P8M1_Flat_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_magnetOn_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)

      ##### Pythia 8 slices 15-30
      config.General.requestName = 'QCD16'+Tag+'_P8M1_15to30_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 25
      submit(config)

      ##### Pythia 8 slices 30-50
      config.General.requestName = 'QCD16'+Tag+'_P8M1_30to50_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)

      ##### Pythia 8 slices 50-80
      config.General.requestName = 'QCD16'+Tag+'_P8M1_50to80_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)

      ##### Pythia 8 slices 80-120
      config.General.requestName = 'QCD16'+Tag+'_P8M1_80to120_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)
      # extension 2 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_80to120_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)

      ##### Pythia 8 slices 120-170
      config.General.requestName = 'QCD16'+Tag+'_P8M1_120to170_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)
      # extension 1 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_120to170_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
      config.Data.unitsPerJob = 5
      submit(config)

      ##### Pythia 8 slices 170-300
      config.General.requestName = 'QCD16'+Tag+'_P8M1_170to300_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)
      # extension 1 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_170to300_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)

      ##### Pythia 8 slices 300-470
      config.General.requestName = 'QCD16'+Tag+'_P8M1_300to470_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 20
      submit(config)
      # extension 1 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_300to470_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
      config.Data.unitsPerJob = 20
      submit(config)

      ##### Pythia 8 slices 470-600
      config.General.requestName = 'QCD16'+Tag+'_P8M1_470to600_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 5
      submit(config)

      ##### Pythia 8 slices 600-800
      config.General.requestName = 'QCD16'+Tag+'_P8M1_600to800_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)
      # extension 1 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_600to800_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)

      ##### Pythia 8 slices 800-1000
      config.General.requestName = 'QCD16'+Tag+'_P8M1_800to1000_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)
      # extension 1 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_800to1000_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
      config.Data.unitsPerJob = 20
      submit(config)

      ##### Pythia 8 slices 1000-1400
      config.General.requestName = 'QCD16'+Tag+'_P8M1_1000to1400_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 5
      submit(config)
      # extension 1 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_1000to1400_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)

      ##### Pythia 8 slices 1400-1800
      config.General.requestName = 'QCD16'+Tag+'_P8M1_1400to1800_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)
      # extension 1 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_1400to1800_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
      config.Data.unitsPerJob = 5

      ##### Pythia 8 slices 1800-2400
      config.General.requestName = 'QCD16'+Tag+'_P8M1_1800to2400_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)
      # extension 1 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_1800to2400_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
      config.Data.unitsPerJob = 5
      submit(config)

      ##### Pythia 8 slices 2400-3200
      config.General.requestName = 'QCD16'+Tag+'_P8M1_2400to3200_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)
      # extension 1 v 1
      config.General.requestName = 'QCD16'+Tag+'_P8M1_2400to3200_TIV_v6_ext'
      config.Data.inputDataset = '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM'
      config.Data.unitsPerJob = 10
      submit(config)

      ##### Pythia 8 slices 3200-Inf
      config.General.requestName = 'QCD16'+Tag+'_P8M1_3200toInf_TIV_v6'
      config.Data.inputDataset = '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM'
      config.Data.unitsPerJob = 5
      submit(config)

