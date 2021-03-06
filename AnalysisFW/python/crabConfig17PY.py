from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
#from WMCore.Configuration import Configuration
#config = Configuration()

#config.section_("General")
config.General.transferOutputs = True
config.General.transferLogs = False
config.General.workArea = 'runs'

#config.section_("JobType")
config.JobType.psetName = 'ProcessedTreeProducer17PY.py'
config.JobType.pluginName = 'Analysis'
#config.outputFiles = ['DATA_ProcessedTreeProducer_2.root']
#config.Data.runRange = '193093-193999'

##### Pythia 8 Flat
#config.General.requestName = 'QCD16_CUETP8M1_Flat15to7000_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 20

#config.General.requestName = 'QCD16_CP5_Flat15to7000_mc17real_v10-1-long'
#config.Data.inputDataset = '/QCD_Pt-15to7000_TuneCP5_Flat2017_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 20

#config.General.requestName = 'QCD16_CP5_Flat15to7000_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 20

## CUETP8M1 Campaign ##

##### Pythia 8 slices 15-30
#config.General.requestName = 'QCD16_CUETP8M1_Slice15to30_mc17real_v10-4'
#config.Data.inputDataset = '/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v4/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 30-50
#config.General.requestName = 'QCD16_CUETP8M1_Slice30to50_mc17real_v10-4'
#config.Data.inputDataset = '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v4/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 50-80
#config.General.requestName = 'QCD16_CUETP8M1_Slice50to80_mc17real_v10-5'
#config.Data.inputDataset = '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v5/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 80-120
#config.General.requestName = 'QCD16_CUETP8M1_Slice80to120_mc17real_v10-3'
#config.Data.inputDataset = '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v3/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 120-170
#config.General.requestName = 'QCD16_CUETP8M1_Slice120to170_mc17real_v10-4'
#config.Data.inputDataset = '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v4/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 170-300
#config.General.requestName = 'QCD16_CUETP8M1_Slice170to300_mc17real_v10-4'
#config.Data.inputDataset = '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v4/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 300-470
#config.General.requestName = 'QCD16_CUETP8M1_Slice300to470_mc17real_v10-4'
#config.Data.inputDataset = '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v4/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 470-600
#config.General.requestName = 'QCD16_CUETP8M1_Slice470to600_mc17real_v10-4'
#config.Data.inputDataset = '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v4/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 600-800
#config.General.requestName = 'QCD16_CUETP8M1_Slice600to800_mc17real_v10-5'
#config.Data.inputDataset = '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v5/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 800-1000
#config.General.requestName = 'QCD16_CUETP8M1_Slice800to1000_mc17real_v10-5'
#config.Data.inputDataset = '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v5/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 1000-1400
#config.General.requestName = 'QCD16_CUETP8M1_Slice1000to1400_mc17real_v10-5'
#config.Data.inputDataset = '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v5/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 1400-1800
#config.General.requestName = 'QCD16_CUETP8M1_Slice1400to1800_mc17real_v10-5'
#config.Data.inputDataset = '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v5/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 1800-2400
#config.General.requestName = 'QCD16_CUETP8M1_Slice1800to2400_mc17real_v10-5'
#config.Data.inputDataset = '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v5/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 2400-3200
#config.General.requestName = 'QCD16_CUETP8M1_Slice2400to3200_mc17real_v10-4'
#config.Data.inputDataset = '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v4/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 3200-Inf
#config.General.requestName = 'QCD16_CUETP8M1_Slice3200toInf_mc17real_v10-5'
#config.Data.inputDataset = '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v5/AODSIM'
#config.Data.unitsPerJob = 10

## CP5 Campaign ##

##### Pythia 8 slices 15-30
#config.General.requestName = 'QCD16_CP5_Slice15to30_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 30-50
#config.General.requestName = 'QCD16_CP5_Slice30to50_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_30to50_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 50-80
#config.General.requestName = 'QCD16_CP5_Slice50to80_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 80-120
#config.General.requestName = 'QCD16_CP5_Slice80to120_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 120-170
#config.General.requestName = 'QCD16_CP5_Slice120to170_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 170-300
#config.General.requestName = 'QCD16_CP5_Slice170to300_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 300-470
#config.General.requestName = 'QCD16_CP5_Slice300to470_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 470-600
#config.General.requestName = 'QCD16_CP5_Slice470to600_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 600-800
#config.General.requestName = 'QCD16_CP5_Slice600to800_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 800-1000
#config.General.requestName = 'QCD16_CP5_Slice800to1000_mc17real_v10-2'
#config.Data.inputDataset = '/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v2/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 1000-1400
#config.General.requestName = 'QCD16_CP5_Slice1000to1400_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 1400-1800
#config.General.requestName = 'QCD16_CP5_Slice1400to1800_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 1800-2400
#config.General.requestName = 'QCD16_CP5_Slice1800to2400_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 2400-3200
#config.General.requestName = 'QCD16_CP5_Slice2400to3200_mc17real_v10-1'
#config.Data.inputDataset = '/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
#config.Data.unitsPerJob = 10
##### Pythia 8 slices 3200-Inf
config.General.requestName = 'QCD16_CP5_Slice3200toInf_mc17real_v10-1'
config.Data.inputDataset = '/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIFall17DRPremix-94X_mc2017_realistic_v10-v1/AODSIM'
config.Data.unitsPerJob = 10

#config.section_("Data")
config.Data.splitting = 'LumiBased'
config.Data.inputDBS = 'global'
#NJOBS = 1000
#config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.outLFNDirBase = '/store/user/hsiikone'
config.Data.publication = False
#config.Data.outputDatasetTag = 'RunH_ReReReco_SMPJtuple'

#config.section_("Site")
config.Site.storageSite = 'T2_FI_HIP'

