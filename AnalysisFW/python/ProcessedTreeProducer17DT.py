# -*- coding: utf-8 -*-

import FWCore.ParameterSet.Config as cms
from os import *

from RecoJets.Configuration.RecoPFJets_cff import ak4PFJets, ak4PFJetsCHS
from RecoJets.Configuration.RecoGenJets_cff import ak4GenJets
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff import *
from PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi import selectedPatJets
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.patSequences_cff import *
from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from RecoJets.JetProducers.QGTagger_cfi import QGTagger
from JetMETCorrections.Type1MET.correctionTermsPfMetType0PFCandidate_cff import *
from JetMETCorrections.Type1MET.correctedMet_cff import pfMetT0pcTxy
from Configuration.AlCa.GlobalTag import GlobalTag


# -*- coding: utf-8 -*-
import FWCore.ParameterSet.Config as cms

process = cms.Process("Ntuplizer")
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#! Conditions
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('RecoJets.Configuration.GenJetParticles_cff')
process.load('RecoJets.Configuration.RecoGenJets_cff')
process.load('RecoJets.JetProducers.TrackJetParameters_cfi')
process.load('RecoJets.JetProducers.PileupJetIDParams_cfi')
process.load("PhysicsTools.PatAlgos.patSequences_cff")

process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets = cms.InputTag('ak4PFJetsCHS')
process.QGTagger.jetsLabel  = cms.string('QGL_AK4PFchs')

#process.GlobalTag.globaltag = "80X_dataRun2_ICHEP16_repro_v0"
#process.GlobalTag.globaltag = "80X_dataRun2_2016SeptRepro_v4"
#process.GlobalTag.globaltag = "80X_dataRun2_2016LegacyRepro_v4"
process.GlobalTag.globaltag = "94X_dataRun2_ReReco_EOY17_v2"

##-------------------- Import the JEC services -----------------------
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#! Services
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

process.load('FWCore.MessageLogger.MessageLogger_cfi')
#process.MessageLogger = cms.Service("MessageLogger",
#        destinations = cms.untracked.vstring(                           #1
#                'myOutputFile'                                          #2
#        ),
#        myOutputFile = cms.untracked.PSet(                              #3
#                threshold = cms.untracked.string( 'WARNING' )           #4
#        ),
#)                                                                       #5
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.load('CommonTools.UtilAlgos.TFileService_cfi')
process.TFileService.fileName=cms.string('DATA.root')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#! Input
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

inFiles = cms.untracked.vstring(
'root://cms-xrd-global.cern.ch//store/data/Run2017B/JetHT/AOD/17Nov2017-v1/20000/0025AD66-25CC-E711-B8FE-EC0D9A0B3320.root'
#'root://cms-xrd-global.cern.ch//store/data/Run2016G/JetHT/AOD/07Aug17-v1/110000/0017B3B5-F17C-E711-BC55-0242AC110004.root'
#'root://cms-xrd-global.cern.ch//store/data/Run2016G/JetHT/AOD/23Sep2016-v1/100000/0645BD20-F486-E611-A724-002590D0B054.root'
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(200))
process.source = cms.Source("PoolSource", fileNames = inFiles )

triggers = cms.vstring( "HLT_PFJet40_v19", "HLT_PFJet60_v19", "HLT_PFJet450_v19", "HLT_PFJet500_v19"
                        "HLT_PFJet40_v18", "HLT_PFJet60_v18", "HLT_PFJet80_v18", "HLT_PFJet260_v18", "HLT_PFJet320_v18", "HLT_PFJet400_v18", "HLT_PFJet450_v18", "HLT_PFJet500_v18",
                        "HLT_PFJet40_v17", "HLT_PFJet60_v17", "HLT_PFJet80_v17", "HLT_PFJet140_v17", "HLT_PFJet200_v17", "HLT_PFJet260_v17", "HLT_PFJet320_v17", "HLT_PFJet400_v17", "HLT_PFJet450_v17", "HLT_PFJet500_v17",
                        "HLT_PFJet40_v16", "HLT_PFJet60_v16", "HLT_PFJet80_v16", "HLT_PFJet140_v16", "HLT_PFJet200_v16", "HLT_PFJet260_v16", "HLT_PFJet320_v16", "HLT_PFJet400_v16", "HLT_PFJet450_v16", "HLT_PFJet500_v16",
                        "HLT_PFJet40_v15", "HLT_PFJet60_v15", "HLT_PFJet80_v15", "HLT_PFJet140_v15", "HLT_PFJet200_v15", "HLT_PFJet260_v15", "HLT_PFJet320_v15", "HLT_PFJet400_v15", "HLT_PFJet450_v15", "HLT_PFJet500_v15",
                        "HLT_PFJet40_v14", "HLT_PFJet60_v14", "HLT_PFJet80_v14", "HLT_PFJet140_v14", "HLT_PFJet200_v14", "HLT_PFJet260_v14", "HLT_PFJet320_v14", "HLT_PFJet400_v14", "HLT_PFJet450_v14", "HLT_PFJet500_v14",
                        "HLT_PFJet40_v13", "HLT_PFJet60_v13", "HLT_PFJet80_v13", "HLT_PFJet140_v13", "HLT_PFJet200_v13", "HLT_PFJet260_v13", "HLT_PFJet320_v13", "HLT_PFJet400_v13", "HLT_PFJet450_v13", "HLT_PFJet500_v13",
                        "HLT_PFJet40_v12", "HLT_PFJet60_v12", "HLT_PFJet80_v12", "HLT_PFJet140_v12", "HLT_PFJet200_v12", "HLT_PFJet260_v12", "HLT_PFJet320_v12", "HLT_PFJet400_v12", "HLT_PFJet450_v12", "HLT_PFJet500_v12",
                        "HLT_PFJet40_v11", "HLT_PFJet60_v11", "HLT_PFJet80_v11", "HLT_PFJet140_v11", "HLT_PFJet200_v11", "HLT_PFJet260_v11", "HLT_PFJet320_v11", "HLT_PFJet400_v11", "HLT_PFJet450_v11", "HLT_PFJet500_v11",
                        "HLT_PFJet40_v10", "HLT_PFJet60_v10", "HLT_PFJet80_v10", "HLT_PFJet140_v10", "HLT_PFJet200_v10", "HLT_PFJet260_v10", "HLT_PFJet320_v10", "HLT_PFJet400_v10", "HLT_PFJet450_v10", "HLT_PFJet500_v10",
                        'HLT_PFJet40_v9','HLT_PFJet60_v9','HLT_PFJet80_v9','HLT_PFJet140_v9','HLT_PFJet200_v9','HLT_PFJet260_v9','HLT_PFJet320_v9','HLT_PFJet400_v9','HLT_PFJet450_v9','HLT_PFJet500_v9',
                        'HLT_PFJet40_v8','HLT_PFJet60_v8','HLT_PFJet80_v8','HLT_PFJet140_v8','HLT_PFJet200_v8','HLT_PFJet260_v8','HLT_PFJet320_v8','HLT_PFJet400_v8','HLT_PFJet450_v8','HLT_PFJet500_v8', 
                        'HLT_PFJet40_v7','HLT_PFJet60_v7','HLT_PFJet80_v7','HLT_PFJet140_v7','HLT_PFJet200_v7','HLT_PFJet260_v7','HLT_PFJet320_v7','HLT_PFJet400_v7','HLT_PFJet450_v7','HLT_PFJet500_v7',
                        'HLT_PFJet40_v6','HLT_PFJet60_v6','HLT_PFJet80_v6','HLT_PFJet140_v6','HLT_PFJet200_v6','HLT_PFJet260_v6','HLT_PFJet320_v6','HLT_PFJet400_v6','HLT_PFJet450_v6','HLT_PFJet500_v6',
                        'HLT_PFJet40_v5','HLT_PFJet60_v5','HLT_PFJet80_v5','HLT_PFJet140_v5','HLT_PFJet200_v5','HLT_PFJet260_v5','HLT_PFJet320_v5','HLT_PFJet400_v5','HLT_PFJet450_v5','HLT_PFJet500_v5',
                        'HLT_PFJet40_v4','HLT_PFJet60_v4', 'HLT_PFJet80_v4', 'HLT_PFJet140_v4','HLT_PFJet200_v4','HLT_PFJet260_v4','HLT_PFJet320_v4','HLT_PFJet400_v4','HLT_PFJet450_v4','HLT_PFJet500_v4'
)

## Modified version of jetToolBox from https://github.com/cms-jet/jetToolbox
## Options for PUMethod: Puppi, CS, SK, CHS
def jetToolbox( proc, jetType, jetSequence ):
  bTagDiscriminators = [#'trackCountingHighEffBJetTags',
                        #'trackCountingHighPurBJetTags',
                        #'pfTrackCountingHighEffBJetTags',
                        #'pfTrackCountingHighPurBJetTags',
                        #'softPFMuonByIP3dBJetTags',
                        #'softPFElectronByIP3dBJetTags',
                        #'softPFMuonBJetTags',
                        #'softPFElectronBJetTags',
                        #'simpleSecondaryVertexHighEffBJetTags',
                        #'simpleSecondaryVertexHighPurBJetTags',
                        #'pfSimpleSecondaryVertexHighEffBJetTags',
                        #'pfSimpleSecondaryVertexHighPurBJetTags',
                        #'combinedSecondaryVertexV2BJetTags',
                        #'pfDeepCSVJetTags:probc',
                        #'pfDeepCSVJetTags:probb',
                        #'pfDeepCSVJetTags:probbb',
                        #'pfDeepCSVJetTags:probcc',
                        #'pfDeepCSVJetTags:probudsg', 
                        #'pfDeepCMVAJetTags:probc',
                        #'pfDeepCMVAJetTags:probb',
                        #'pfDeepCMVAJetTags:probbb',
                        #'pfDeepCMVAJetTags:probcc', 
                        #'pfDeepCMVAJetTags:probudsg',
                        #'pfNegativeDeepCSVJetTags:probb',
                        #'pfNegativeDeepCSVJetTags:probc', 
                        #'pfNegativeDeepCSVJetTags:probcc',
                        #'pfNegativeDeepCSVJetTags:probbb',
                        #'pfNegativeDeepCSVJetTags:probudsg',
                        #'pfPositiveDeepCSVJetTags:probb',
                        #'pfPositiveDeepCSVJetTags:probc',
                        #'pfPositiveDeepCSVJetTags:probcc',
                        #'pfPositiveDeepCSVJetTags:probbb', 
                        #'pfPositiveDeepCSVJetTags:probudsg', 
                        #'pfNegativeDeepCMVAJetTags:probb',
                        #'pfNegativeDeepCMVAJetTags:probc',
                        #'pfNegativeDeepCMVAJetTags:probcc',
                        #'pfNegativeDeepCMVAJetTags:probbb',
                        #'pfNegativeDeepCMVAJetTags:probudsg',
                        #'pfPositiveDeepCMVAJetTags:probb',
                        #'pfPositiveDeepCMVAJetTags:probc',
                        #'pfPositiveDeepCMVAJetTags:probcc',
                        #'pfPositiveDeepCMVAJetTags:probbb',
                        #'pfPositiveDeepCMVAJetTags:probudsg',
                        #'deepFlavourJetTags:probb',
                        #'deepFlavourJetTags:probc',
                        #'deepFlavourJetTags:probudsg',
                        #'deepFlavourJetTags:probbb',
                        #'deepFlavourJetTags:probcc',
                        #'negativeDeepFlavourJetTags:probb',
                        #'negativeDeepFlavourJetTags:probc',
                        #'negativeDeepFlavourJetTags:probudsg',
                        #'negativeDeepFlavourJetTags:probbb',
                        #'negativeDeepFlavourJetTags:probcc',
                        #'positiveDeepFlavourJetTags:probb',
                        #'positiveDeepFlavourJetTags:probc',
                        #'positiveDeepFlavourJetTags:probudsg',
                        #'positiveDeepFlavourJetTags:probbb',
                        #'positiveDeepFlavourJetTags:probcc',
                        'pfTrackCountingHighEffBJetTags',
                        'pfTrackCountingHighPurBJetTags',
                        'pfJetProbabilityBJetTags',
                        'pfJetBProbabilityBJetTags',
                        'pfSimpleSecondaryVertexHighEffBJetTags',
                        'pfSimpleSecondaryVertexHighPurBJetTags',
                        'pfCombinedCvsLJetTags',
                        'pfCombinedCvsBJetTags',
                        'pfBoostedDoubleSecondaryVertexAK8BJetTags',
                        'pfCombinedSecondaryVertexV2BJetTags',
                        'pfPositiveCombinedSecondaryVertexV2BJetTags',  #implemented
                        'pfNegativeCombinedSecondaryVertexV2BJetTags',  #implemented
                        'pfCombinedInclusiveSecondaryVertexV2BJetTags', #implemented
                        'pfCombinedMVAV2BJetTags',                      #implemented
                        'pfJetProbabilityBJetTags']                     #implemented

  print '|---- jetToolbox: Initialyzing collection...'
  algorithm='AntiKt' # CambridgeAachen' , 'Kt'
  size = jetType[-1:] #[-1:] takes the last char from string 'akX'
  jetSize = float('0.'+jetType[-1:])
  jetALGO = jetType.upper()
  jetalgo = jetType.lower()
  PUMethod='CHS'
  jetNAME = jetALGO+'PF'+PUMethod 
  jetname = jetalgo+'PFJets'+PUMethod
  gjetname = jetalgo+'GenJetsNoNu'
  print 'Running processes with: '+jetNAME+' PF '+PUMethod+' jet algorithm with radius parameter '+str(jetSize)

  JEC = ( 'AK'+size+'PF'+PUMethod.lower(), ['L1FastJet', 'L2Relative', 'L3Absolute','L2L3Residual'] , 'None')
  print '|---- jetToolBox: Applying these corrections: '+str(JEC)
  
  #################################################################################
  ####### Toolbox start
  #################################################################################
  
  jetSeq = cms.Sequence()

  ####  Creating AK4PFJetsCHS
  process.load('CommonTools.ParticleFlow.pfNoPileUpJME_cff')
  setattr( proc, jetname, ak4PFJetsCHS.clone(src=cms.InputTag('pfNoPileUpJME'),doAreaFastjet=True,rParam=jetSize,jetAlgorithm=algorithm) )
  jetSeq += getattr(proc, jetname )

  ####  Creating PATjets
  addJetCollection( proc,
                    labelName = jetNAME,
                    jetSource = cms.InputTag(jetname),
                    algo = jetalgo,
                    btagDiscriminators = bTagDiscriminators,
                    rParam = jetSize,
                    jetCorrections =  JEC,
                    pfCandidates = cms.InputTag( 'particleFlow' ), # redundant (default)
                    svSource = cms.InputTag('inclusiveCandidateSecondaryVertices'), # redundant (default)
                    pvSource = cms.InputTag( 'offlinePrimaryVertices' ), # redundant (default)
                    getJetMCFlavour = False,
                    jetTrackAssociation = True)
  getattr(proc,'patJets'+jetNAME).addTagInfos = cms.bool(True)
  getattr(proc,'patJets'+jetNAME).addAssociatedTracks = cms.bool(True)

  setattr( proc, 'QGTagger'+jetNAME,QGTagger.clone( srcJets = cms.InputTag(jetname),jetsLabel = cms.string('QGL_AK4PFchs') ) )
  getattr( proc, 'patJets'+jetNAME).userData.userFloats.src += ['QGTagger'+jetNAME+':qgLikelihood']
  jetSeq += getattr(proc, 'QGTagger'+jetNAME )
  
  # This is already done in addJetCollection, but I worry that the changes done to patJets do not get updated to selectedPatJets
  setattr(proc, 'selectedPatJets'+jetNAME, selectedPatJets.clone( src = 'patJets'+jetNAME ))
  # return
  setattr(proc, jetSequence, jetSeq)

jetToolbox( process, 'ak4', 'ak4JetSubs' )

# PAT Layer 1
process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")
process.load("PhysicsTools.PatAlgos.patSequences_cff")

process.ak4 =  cms.EDAnalyzer( 'ProcessedTreeProducerBTag',
                               ## jet collections ###########################
                               pfjetschs                 = cms.InputTag('selectedPatJetsAK4PFCHS'),
                               pfpujetid                 = cms.string('AK4PFpileupJetIdEvaluator:fullDiscriminant'),
                               pfchsjetpuid              = cms.string('AK4PFCHSpileupJetIdEvaluator:fullDiscriminant'),
                               ## MET collection ####
                               pfmet                     = cms.InputTag('patMETs'),
                               ## database entry for the uncertainties ######
                               PFPayloadNameCHS          = cms.string('AK4PFchs'),
                               jecUncSrcCHS              = cms.string(''),
                               jecUncSrcNames            = cms.vstring(''),
                               ## set the conditions for good Vtx counting ##
                               offlineVertices           = cms.InputTag('offlinePrimaryVertices'),
                               beamSpot                  = cms.InputTag('offlineBeamSpot'),
                               goodVtxNdof               = cms.double(4),
                               goodVtxZ                  = cms.double(24),
                               ## rho #######################################
                               srcCaloRho                = cms.InputTag('fixedGridRhoFastjetAllCalo'),
                               srcPFRho                  = cms.InputTag('fixedGridRhoFastjetAll'),
                               srcPULabel                = cms.untracked.InputTag('addPileupInfo','addPileupInfo'),
                               ## preselection cuts #########################
                               maxY                      = cms.double(5.0),
                               minPFPt                   = cms.double(10.0),
                               minPFPtThirdJet           = cms.double(5.0),
                               minNPFJets                = cms.int32(1),
                               minGenPt                  = cms.untracked.double(20.0),
                               minJJMass                 = cms.double(-1),
                               isMCarlo                  = cms.untracked.bool(False),
                               useGenInfo                = cms.untracked.bool(False),
                               AK4                       = cms.untracked.bool(True),
                               ## trigger ###################################
                               printTriggerMenu          = cms.untracked.bool(True),
                               processName               = cms.string('HLT'),
                               triggerName               = triggers, 
                               triggerResults            = cms.InputTag("TriggerResults","","HLT"),
                               triggerEvent              = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
                               ## jec services ##############################
                               HBHENoiseFilterResultLabel = cms.InputTag("HBHENoiseFilterResultProducer", "HBHENoiseFilterResult"),
                               HBHENoiseFilterResultNoMinZLabel = cms.InputTag("HBHENoiseFilterResultProducerNoMinZ", "HBHENoiseFilterResult"), 
                               ## gen services (dummy) ######################
                               EventInfo                 = cms.InputTag("generator"),
                               GenParticles              = cms.InputTag("genparticles"),
                               jetFlavourInfos           = cms.InputTag("genJetFlavourInfos"),
                               jetFlavourInfosPhysicsDef = cms.InputTag("genJetFlavourInfosPhysicsDef") ) 

############# hlt filter #########################
process.hltFilter = cms.EDFilter( 'HLTHighLevel',
                                  TriggerResultsTag  = cms.InputTag('TriggerResults','','HLT'),
                                  HLTPaths  = triggers,
                                  eventSetupPathsKey = cms.string(''),
                                  andOr              = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
                                  throw              = cms.bool(False) )

##MET Filters
process.load('RecoMET.METFilters.CSCTightHaloFilter_cfi')
process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
process.load('CommonTools.RecoAlgos.HBHENoiseFilter_cfi')
process.HBHENoiseFilterResultProducerNoMinZ = process.HBHENoiseFilterResultProducer.clone(minZeros = cms.int32(99999))
process.load('RecoMET.METFilters.trackingFailureFilter_cfi')
process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')
process.load('RecoMET.METFilters.primaryVertexFilter_cfi')
process.load('RecoMET.METFilters.ecalBadCalibFilter_cfi')
process.load('RecoMET.METFilters.eeBadScFilter_cfi')
process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
process.load('RecoMET.METFilters.globalTightHalo2016Filter_cfi')

process.goodVertices = cms.EDFilter( "VertexSelector",
                                     filter = cms.bool(False),
                                     src = cms.InputTag("offlinePrimaryVertices"),
                                     cut = cms.string("!isFake && ndof >= 4 && abs(z) <= 24 && position.rho <= 2") )

process.allFilterPaths=cms.Sequence( process.goodVertices*
                                     process.trackingFailureFilter*
                                     process.hltFilter*
                                     process.HBHENoiseFilterResultProducer*
                                     process.HBHENoiseFilterResultProducerNoMinZ*
                                     process.HBHENoiseFilter*
                                     process.HBHENoiseIsoFilter*
                                     process.primaryVertexFilter*
                                     process.EcalDeadCellTriggerPrimitiveFilter*
                                     process.ecalBadCalibFilter*
                                     process.eeBadScFilter*
                                     process.BadPFMuonFilter*
                                     process.BadChargedCandidateFilter*
                                     process.globalTightHalo2016Filter )

##Type1 patMET Producer
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0PFCandidate_cff")
process.load("JetMETCorrections.Type1MET.correctedMet_cff")
process.load('PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi')
process.patMETs.addGenMET = cms.bool(False)
## Choose to use Type0 MET instead
process.patMETs.metSource = cms.InputTag("pfMetT0pc")

process.allMetPaths=cms.Sequence( process.correctionTermsPfMetType0PFCandidate*
                                  process.pfMetT0pc*
                                  process.patMETs )

process.allBTagPaths=cms.Sequence( process.pfImpactParameterTagInfosAK4PFCHS*
                                   process.pfImpactParameterAK8TagInfosAK4PFCHS*
                                   process.pfSecondaryVertexTagInfosAK4PFCHS*
                                   process.pfInclusiveSecondaryVertexFinderCvsLTagInfosAK4PFCHS*
                                   process.softPFMuonsTagInfosAK4PFCHS*
                                   process.softPFElectronsTagInfosAK4PFCHS*
                                   process.pfSecondaryVertexNegativeTagInfosAK4PFCHS*
                                   process.pfInclusiveSecondaryVertexFinderTagInfosAK4PFCHS*
                                   process.pfInclusiveSecondaryVertexFinderAK8TagInfosAK4PFCHS*
                                   process.pfBoostedDoubleSVAK8TagInfosAK4PFCHS*
                                   process.pfCombinedMVAV2BJetTagsAK4PFCHS*
                                   process.pfCombinedInclusiveSecondaryVertexV2BJetTagsAK4PFCHS*
                                   process.pfNegativeCombinedSecondaryVertexV2BJetTagsAK4PFCHS*
                                   process.pfPositiveCombinedSecondaryVertexV2BJetTagsAK4PFCHS*
                                   process.pfCombinedSecondaryVertexV2BJetTagsAK4PFCHS*
                                   process.pfBoostedDoubleSecondaryVertexAK8BJetTagsAK4PFCHS*
                                   process.pfCombinedCvsBJetTagsAK4PFCHS*
                                   process.pfCombinedCvsLJetTagsAK4PFCHS*
                                   process.pfSimpleSecondaryVertexHighPurBJetTagsAK4PFCHS*
                                   process.pfSimpleSecondaryVertexHighEffBJetTagsAK4PFCHS*
                                   process.pfJetBProbabilityBJetTagsAK4PFCHS*
                                   process.pfJetProbabilityBJetTagsAK4PFCHS*
                                   process.pfTrackCountingHighPurBJetTagsAK4PFCHS*
                                   process.pfTrackCountingHighEffBJetTagsAK4PFCHS )

process.allJetPaths=cms.Sequence( process.patJetChargeAK4PFCHS*
                                  process.patJetCorrFactorsAK4PFCHS*
                                  process.patJetsAK4PFCHS*
                                  process.selectedPatJetsAK4PFCHS )

process.content = cms.EDAnalyzer("EventContentAnalyzer")

#Try scheduled processs
process.path = cms.Path( process.allFilterPaths*
                         process.allMetPaths*
                         process.QGTaggerAK4PFCHS*
                         process.QGTagger*
                         process.jetTracksAssociatorAtVertexAK4PFCHS*
                         process.allBTagPaths*
                         process.allJetPaths*
                         process.ak4 )

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#! Output and Log
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.options.allowUnscheduled = cms.untracked.bool(True)
