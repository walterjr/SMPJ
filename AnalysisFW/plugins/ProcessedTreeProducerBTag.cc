#include <iostream>
#include <sstream>
#include <istream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cmath>
#include <functional>
#include "TTree.h"
#include <vector>
#include <cassert>
#include <TLorentzVector.h>

#include "SMPJ/AnalysisFW/plugins/ProcessedTreeProducerBTag.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/JetExtendedAssociation.h"
#include "DataFormats/JetReco/interface/JetID.h"
#include "DataFormats/METReco/interface/HcalNoiseSummary.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"

#include "PhysicsTools/PatUtils/interface/bJetSelector.h"
#include "PhysicsTools/PatExamples/interface/BTagPerformance.h"
#include "PhysicsTools/PatExamples/interface/PatBTagCommonHistos.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Common/interface/ValueMap.h"

//hadron-level definition
#include "SimDataFormats/JetMatching/interface/JetFlavourInfo.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourInfoMatching.h"
#include "DataFormats/Math/interface/deltaR.h"

ProcessedTreeProducerBTag::ProcessedTreeProducerBTag(edm::ParameterSet const& cfg):
  mOfflineVertices(mayConsume<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("offlineVertices"))),
  mBeamSpot(mayConsume<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamSpot"))),
  mSrcCaloRho(mayConsume<double>(cfg.getParameter<edm::InputTag>("srcCaloRho"))),
  mSrcPFRho(mayConsume<double>(cfg.getParameter<edm::InputTag>("srcPFRho"))),
  mPFMET(mayConsume<pat::METCollection>(cfg.getParameter<edm::InputTag>("pfmet"))),
  mGenJetsName(mayConsume<GenJetCollection>(cfg.getUntrackedParameter<edm::InputTag>("genjets",edm::InputTag("")))),
  triggerResultsTag_(mayConsume<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("triggerResults"))),
  triggerEventTag_(mayConsume<trigger::TriggerEvent>(cfg.getParameter<edm::InputTag>("triggerEvent"))),
  mHBHENoiseFilterResultLabel(mayConsume<bool>(cfg.getParameter<edm::InputTag>("HBHENoiseFilterResultLabel"))),
  mHBHENoiseFilterResultNoMinZLabel(mayConsume<bool>(cfg.getParameter<edm::InputTag>("HBHENoiseFilterResultNoMinZLabel"))),
  mSrcPU(mayConsume<std::vector<PileupSummaryInfo> >(cfg.getUntrackedParameter<edm::InputTag>("srcPULabel"))),
  hltPrescale_(cfg, consumesCollector(), *this)
{
  mPFPayloadNameCHS  = cfg.getParameter<std::string>               ("PFPayloadNameCHS");
  pfchsjetpuid       = cfg.getParameter<std::string>               ("pfchsjetpuid");
  mGoodVtxNdof       = cfg.getParameter<double>                    ("goodVtxNdof");
  mGoodVtxZ          = cfg.getParameter<double>                    ("goodVtxZ");
  mMinPFPt           = cfg.getParameter<double>                    ("minPFPt");
  mMinPFPtThirdJet   = cfg.getParameter<double>                    ("minPFPtThirdJet");
  mMinJJMass         = cfg.getParameter<double>                    ("minJJMass");
  mMaxY              = cfg.getParameter<double>                    ("maxY");
  mMinNPFJets        = cfg.getParameter<int>                       ("minNPFJets");
  mPrintTriggerMenu  = cfg.getUntrackedParameter<bool>             ("printTriggerMenu",false);
  mIsMCarlo          = cfg.getUntrackedParameter<bool>             ("isMCarlo",false);
  mAK4               = cfg.getUntrackedParameter<bool>             ("AK4",false);
  mUseGenInfo        = cfg.getUntrackedParameter<bool>             ("useGenInfo",false);
  mMinGenPt          = cfg.getUntrackedParameter<double>           ("minGenPt",20);
  processName_       = cfg.getParameter<std::string>               ("processName");
  triggerNames_      = cfg.getParameter<std::vector<std::string> > ("triggerName");
  mPFJECUncSrcCHS    = cfg.getParameter<std::string>               ("jecUncSrcCHS");
  mPFJECUncSrcNames  = cfg.getParameter<std::vector<std::string> > ("jecUncSrcNames");
  mPFJetsNameCHS = consumes<edm::View<pat::Jet> >(cfg.getParameter<edm::InputTag>("pfjetschs"));
  mhEventInfo = consumes<GenEventInfoProduct>(cfg.getParameter<edm::InputTag>("EventInfo"));
  mgenParticles = consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("GenParticles"));
  qgToken = consumes<edm::ValueMap<float>>(edm::InputTag("QGTagger", "qgLikelihood"));
  jetFlavourInfosToken_ = consumes<reco::JetFlavourInfoMatchingCollection>( cfg.getParameter<edm::InputTag>("jetFlavourInfos"));
  jetFlavourInfosTokenPhysicsDef_ = consumes<reco::JetFlavourInfoMatchingCollection>( cfg.getParameter<edm::InputTag>("jetFlavourInfosPhysicsDef"));
}
//////////////////////////////////////////////////////////////////////////////////////////
void ProcessedTreeProducerBTag::beginJob()
{
  mTree = fs->make<TTree>("ProcessedTree","ProcessedTree");
  mEvent = new QCDEvent();
  mTree->Branch("events","QCDEvent",&mEvent);
  mTriggerNamesHisto = fs->make<TH1F>("TriggerNames","TriggerNames",1,0,1);
  mTriggerNamesHisto->SetBit(TH1::kUserContour);
  for(unsigned i=0;i<triggerNames_.size();i++) mTriggerNamesHisto->Fill(triggerNames_[i].c_str(),1);
  mTriggerPassHisto = fs->make<TH1F>("TriggerPass","TriggerPass",1,0,1);
  mTriggerPassHisto->SetBit(TH1::kUserContour);
  isPFJecUncSetCHS_ = false;
}
//////////////////////////////////////////////////////////////////////////////////////////
void ProcessedTreeProducerBTag::endJob() {}
//////////////////////////////////////////////////////////////////////////////////////////
void ProcessedTreeProducerBTag::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
{
  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,processName_,changed) && hltPrescale_.init(iRun, iSetup, processName_, changed) ) {
    if (changed) {
      // check if trigger names in (new) config
      cout<<"New trigger menu found !!!"<<endl;
      triggerIndex_.clear();
      const unsigned int n(hltConfig_.size());
      for(unsigned itrig=0;itrig<triggerNames_.size();itrig++) {
        triggerIndex_.push_back(hltConfig_.triggerIndex(triggerNames_[itrig]));
        cout<<triggerNames_[itrig]<<" "<<triggerIndex_[itrig]<<" ";
        if (triggerIndex_[itrig] >= n)
          cout<<"does not exist in the current menu"<<endl;
        else
          cout<<"exists"<<endl;
      }
      cout << "Available TriggerNames are: " << endl;
      if (mPrintTriggerMenu)
        hltConfig_.dump("Triggers");
    }
  }
  else {
    cout << "ProcessedTreeProducerBTag::analyze:"
         << " config extraction failure with process name "
         << processName_ << endl;
  }
}
//////////////////////////////////////////////////////////////////////////////////////////
void ProcessedTreeProducerBTag::analyze(edm::Event const& event, edm::EventSetup const& iSetup)
{
  vector<QCDPFJet>      mPFJets;
  vector<QCDPFJet>      mPFJetsCHS;
  vector<LorentzVector> mGenJets;
  vector<float> GenFlavour;
  vector<float> GenPartonFlavourPhysicsDef;
  vector<float> GenHadronFlavour;
  QCDEventHdr mEvtHdr;
  QCDMET mPFMet;

  //-------------- Basic Event Info ------------------------------
  mEvtHdr.setRun(event.id().run());
  mEvtHdr.setEvt(event.id().event());
  mEvtHdr.setLumi(event.luminosityBlock());
  mEvtHdr.setBunch(event.bunchCrossing());
  //-------------- Beam Spot --------------------------------------
  Handle<reco::BeamSpot> beamSpot;
  event.getByToken(mBeamSpot,beamSpot);
  if (beamSpot.isValid())
    mEvtHdr.setBS(beamSpot->x0(),beamSpot->y0(),beamSpot->z0());
  else
    mEvtHdr.setBS(-999,-999,-999);


  //-------------- HCAL Noise Summary -----------------------------
  Handle<bool> noiseSummary;
  Handle<bool> noiseSummary_NoMinZ;

  if (!mIsMCarlo) {
    event.getByToken(mHBHENoiseFilterResultLabel, noiseSummary);
    mEvtHdr.setHCALNoise(*noiseSummary);

    event.getByToken(mHBHENoiseFilterResultNoMinZLabel, noiseSummary_NoMinZ);
    mEvtHdr.setHCALNoiseNoMinZ(*noiseSummary_NoMinZ);
  } else{ 
    mEvtHdr.setHCALNoise(true);
    mEvtHdr.setHCALNoiseNoMinZ(true);
  }
  //-------------- Trigger Info -----------------------------------
  event.getByToken(triggerResultsTag_,triggerResultsHandle_);
  if (!triggerResultsHandle_.isValid()) {
    cout << "ProcessedTreeProducerBTag::analyze: Error in getting TriggerResults product from Event!" << endl;
    return;
  }
  event.getByToken(triggerEventTag_,triggerEventHandle_);
  if (!triggerEventHandle_.isValid()) {
    cout << "ProcessedTreeProducerBTag::analyze: Error in getting TriggerEvent product from Event!" << endl;
    return;
  }
  vector<int> L1Prescales,HLTPrescales,Fired;
  vector<vector<LorentzVector> > mL1Objects,mHLTObjects;
  // sanity check
  assert(triggerResultsHandle_->size() == hltConfig_.size());
  //------ loop over all trigger names ---------
  for(unsigned itrig=0;itrig<triggerNames_.size() && !mIsMCarlo;itrig++) {
    bool accept(false);
    int preL1(-1);
    int preHLT(-1);
    int tmpFired(-1);
    vector<LorentzVector> vvL1,vvHLT;
    if (triggerIndex_[itrig] < hltConfig_.size()) {
      accept = triggerResultsHandle_->accept(triggerIndex_[itrig]);
      
      std::pair<std::vector<std::pair<std::string,int> >,int> detailedPrescaleInfo = hltPrescale_.prescaleValuesInDetail(event, iSetup, triggerNames_[itrig]);	 
      preHLT = detailedPrescaleInfo.second ;

      // save l1 prescale values in standalone vector
      std::vector <int> l1prescalevals;
      for( size_t varind = 0; varind < detailedPrescaleInfo.first.size(); varind++ )
        l1prescalevals.push_back(detailedPrescaleInfo.first.at(varind).second);
   
      //find and save minimum l1 prescale of any ORed L1 that seeds the HLT
      std::vector<int>::iterator result = std::min_element(std::begin(l1prescalevals), std::end(l1prescalevals));
      size_t minind = std::distance(std::begin(l1prescalevals), result);
      // sometimes there are no L1s associated with a HLT. In that case, this branch stores -1 for the l1prescale
      preL1 = minind < l1prescalevals.size() ? l1prescalevals.at(minind) : -1 ;//commented for 76X
      
      ///end in detail
      if (!accept)
        tmpFired = 0;
      else {
        mTriggerPassHisto->Fill(triggerNames_[itrig].c_str(),1);
        tmpFired = 1;
      }

      //--------- modules on this trigger path--------------
      const vector<string>& moduleLabels(hltConfig_.moduleLabels(triggerIndex_[itrig]));
      const unsigned int moduleIndex(triggerResultsHandle_->index(triggerIndex_[itrig]));
      bool foundL1(false);
      for(unsigned int j=0; j<=moduleIndex; ++j) {
        const string& moduleLabel(moduleLabels[j]);
        const string  moduleType(hltConfig_.moduleType(moduleLabel));
        //--------check whether the module is packed up in TriggerEvent product
        const unsigned int filterIndex(triggerEventHandle_->filterIndex(InputTag(moduleLabel,"",processName_)));
        if (filterIndex<triggerEventHandle_->sizeFilters()) {
          const Vids& VIDS (triggerEventHandle_->filterIds(filterIndex));
          const Keys& KEYS(triggerEventHandle_->filterKeys(filterIndex));
          const size_type nI(VIDS.size());
          const size_type nK(KEYS.size());
          assert(nI==nK);
          const size_type n(max(nI,nK));
          const TriggerObjectCollection& TOC(triggerEventHandle_->getObjects());
          if (foundL1) {
            for(size_type i=0; i!=n; ++i) {
              const TriggerObject& TO(TOC[KEYS[i]]);
              TLorentzVector P4;
              P4.SetPtEtaPhiM(TO.pt(),TO.eta(),TO.phi(),TO.mass());
              LorentzVector qcdhltobj(P4.Px(),P4.Py(),P4.Pz(),P4.E());
              vvHLT.push_back(qcdhltobj);
              //cout<<TO.pt()<<endl;
            }
          } else {
            for(size_type i=0; i!=n; ++i) {
              const TriggerObject& TO(TOC[KEYS[i]]);
              TLorentzVector P4;
              P4.SetPtEtaPhiM(TO.pt(),TO.eta(),TO.phi(),TO.mass());
              LorentzVector qcdl1obj(P4.Px(),P4.Py(),P4.Pz(),P4.E());
              vvL1.push_back(qcdl1obj);
              //cout<<TO.pt()<<endl;
            }
            foundL1 = true;
          }
        }
      }// loop over modules
    }// if the trigger exists in the menu
    //cout<<triggerNames_[itrig]<<" "<<triggerIndex_[itrig]<<" "<<accept<<" "<<tmpFired<<endl;
    Fired.push_back(tmpFired);
    L1Prescales.push_back(preL1);
    HLTPrescales.push_back(preHLT);
    mL1Objects.push_back(vvL1);
    mHLTObjects.push_back(vvHLT);
  }// loop over trigger names
  mEvent->setTrigDecision(Fired);
  mEvent->setPrescales(L1Prescales,HLTPrescales);
  mEvent->setL1Obj(mL1Objects);
  mEvent->setHLTObj(mHLTObjects);

  //-------------- Vertex Info -----------------------------------
  Handle<reco::VertexCollection> recVtxs;
  event.getByToken(mOfflineVertices,recVtxs);
  //------------- reject events without reco vertices ------------
  int VtxGood(0);
  bool isPVgood(false);
  float PVx(0),PVy(0),PVz(0),PVndof(0);
  for(VertexCollection::const_iterator i_vtx = recVtxs->begin(); i_vtx != recVtxs->end(); i_vtx++) {
    int index = i_vtx-recVtxs->begin();
    if (index == 0) {
      PVx    = i_vtx->x();
      PVy    = i_vtx->y();
      PVz    = i_vtx->z();
      PVndof = i_vtx->ndof();
    }
    if (!(i_vtx->isFake()) && i_vtx->ndof() >= mGoodVtxNdof && fabs(i_vtx->z()) <= mGoodVtxZ) {
      if (index == 0) {
        isPVgood = true;
      }
      VtxGood++;
    }
  }
  mEvtHdr.setVertices(recVtxs->size(),VtxGood);
  mEvtHdr.setPV(isPVgood,PVndof,PVx,PVy,PVz);
  //-------------- Rho ------------------------------------------------
  Handle<double> rhoCalo;
  event.getByToken(mSrcCaloRho,rhoCalo);
  Handle<double> rhoPF;
  event.getByToken(mSrcPFRho,rhoPF);
  mEvtHdr.setRho(*rhoCalo,*rhoPF);
  //-------------- Generator Info -------------------------------------
  Handle<GenEventInfoProduct> hEventInfo;
  //-------------- Simulated PU Info ----------------------------------
  Handle<std::vector<PileupSummaryInfo> > PupInfo;
  if (mIsMCarlo && mUseGenInfo) {
    event.getByToken(mhEventInfo, hEventInfo);
    if (hEventInfo->hasBinningValues())
      mEvtHdr.setPthat(hEventInfo->binningValues()[0]);
    else
      mEvtHdr.setPthat(0);

    mEvtHdr.setWeight(hEventInfo->weight());
    event.getByToken(mSrcPU, PupInfo);
    std::vector<PileupSummaryInfo>::const_iterator PUI;
    int nbx = PupInfo->size();
    int ootpuEarly(0),ootpuLate(0),intpu(0);
    float Tnpv = -1.; // new variable for computing pileup weight factor for the event

    for(PUI = PupInfo->begin(); PUI != PupInfo->end(); ++PUI) {
      if (PUI->getBunchCrossing() < 0)
        ootpuEarly += PUI->getPU_NumInteractions();      
      else if (PUI->getBunchCrossing() > 0)
        ootpuLate += PUI->getPU_NumInteractions();
      else {
        intpu += PUI->getPU_NumInteractions();
        Tnpv = PUI->getTrueNumInteractions();
       }
    }
    mEvtHdr.setPU(nbx,ootpuEarly,ootpuLate,intpu);
    mEvtHdr.setTrPu(Tnpv);
  } else {
    mEvtHdr.setPthat(0);
    mEvtHdr.setWeight(0);
    mEvtHdr.setPU(0,0,0,0);
    mEvtHdr.setTrPu(0);
  }

  //---------------- Jets ---------------------------------------------
  Handle<GenJetCollection>  genjets;
  if (mIsMCarlo) {
    event.getByToken(mGenJetsName,genjets);
    for(GenJetCollection::const_iterator i_gen = genjets->begin(); i_gen != genjets->end(); i_gen++) {
      if (i_gen->pt() > mMinGenPt && fabs(i_gen->y()) < mMaxY) {
        mGenJets.push_back(i_gen->p4());

        //ADD FLAVOUR AT GEN LEVEL
        int FlavourGen = getMatchedPartonGen(event,i_gen);
        //if(FlavourGen<-100) cout<<FlavourGen<<" "<<i_gen->pt()<<" "<<i_gen->eta()<<" "<<i_gen->phi()<<endl;
        GenFlavour.push_back(FlavourGen);
        cout << "Genjet " << int(i_gen-genjets->begin()) << " partonflav " << getMatchedPartonGen(event,i_gen) << endl;
      }
    }

    edm::Handle<reco::JetFlavourInfoMatchingCollection> theJetFlavourInfos;
    event.getByToken(jetFlavourInfosToken_, theJetFlavourInfos );
    
    int counter = 0;
    for ( reco::JetFlavourInfoMatchingCollection::const_iterator j  = theJetFlavourInfos->begin();j != theJetFlavourInfos->end();++j ) {
      reco::JetFlavourInfo aInfo = (*j).second;
      int FlavourGenHadron = aInfo.getHadronFlavour();
      GenHadronFlavour.push_back(FlavourGenHadron);
      cout << "Genjet " << counter << " partonflav " << aInfo.getPartonFlavour() << " hadronflav " << aInfo.getHadronFlavour() << endl;
      ++counter;
    }

    //Physics Definition Gen Level
    edm::Handle<reco::JetFlavourInfoMatchingCollection> theJetFlavourInfosPhysicsDef;
    event.getByToken(jetFlavourInfosTokenPhysicsDef_, theJetFlavourInfosPhysicsDef );

    counter = 0;
    cout << "Physdef" << endl;    
    for ( reco::JetFlavourInfoMatchingCollection::const_iterator j  = theJetFlavourInfosPhysicsDef->begin();j != theJetFlavourInfosPhysicsDef->end();++j ) {
      reco::JetFlavourInfo aInfo = (*j).second;
      int FlavourGenHadronPhysicsDef = aInfo.getPartonFlavour();
      GenPartonFlavourPhysicsDef.push_back(FlavourGenHadronPhysicsDef);
      cout << "Genjet " << counter << " partonflav " << aInfo.getPartonFlavour() << " hadronflav " << aInfo.getHadronFlavour() << endl;
    }
  }
  
  // -------- CHS Uncertainty part ----------------//
  edm::ESHandle<JetCorrectorParametersCollection> PFJetCorParCollCHS;
  if (mPFPayloadNameCHS != "" && !isPFJecUncSetCHS_){
    iSetup.get<JetCorrectionsRecord>().get(mPFPayloadNameCHS,PFJetCorParCollCHS);
    JetCorrectorParameters const& PFJetCorParCHS = (*PFJetCorParCollCHS)["Uncertainty"];
    mPFUncCHS = new JetCorrectionUncertainty(PFJetCorParCHS);
    if (mPFJECUncSrcCHS != "") {
      for(unsigned isrc=0;isrc<mPFJECUncSrcNames.size();isrc++) {
        JetCorrectorParameters *parchs = new JetCorrectorParameters(mPFJECUncSrcCHS,mPFJECUncSrcNames[isrc]);
        JetCorrectionUncertainty *tmpUncCHS = new JetCorrectionUncertainty(*parchs);
        mPFUncSrcCHS.push_back(tmpUncCHS);
      } // for(unsigned isrc=0;isrc<mPFJECUncSrcNames.size();isrc++)
    } // if (mPFJECUncSrcCHS != "")
    isPFJecUncSetCHS_ = true;
  } // if (mPFPayloadNameCHS != "" && !isPFJecUncSetCHS_)


  //----------- PFJets  CHS part -------------------------
  edm::Handle<edm::ValueMap<float>> qgHandle; 
  event.getByToken(qgToken, qgHandle);
 
  edm::Handle<edm::View<pat::Jet> > patjetschs;
  event.getByToken(mPFJetsNameCHS,patjetschs);

  //for (auto i_pfjet=patjetschs->begin(); i_pfjet!=patjetschs->end(); ++i_pfjet) {
  //  edm::RefToBase<pat::Jet> jetRef(edm::Ref<edm::View<pat::Jet> >(patjetschs, i_pfjet - patjetschs->begin()));
  //  float qgLikelihood = (*qgHandle)[jetRef];
  //  cout<<qgLikelihood<<endl;
  //}

  // A store for track-vertex association
  map<reco::TrackRef,int> trk2vtx;
  //---- loop over all vertices ----------------------------
  for(unsigned ivtx = 0; ivtx < recVtxs->size(); ivtx++) {
    //---- loop over the tracks associated with the vertex ---
    if (!((*recVtxs)[ivtx].isFake()) && (*recVtxs)[ivtx].ndof() >= mGoodVtxNdof && fabs((*recVtxs)[ivtx].z()) <= mGoodVtxZ) {
      for (auto i_vtxTrk = (*recVtxs)[ivtx].tracks_begin(); i_vtxTrk != (*recVtxs)[ivtx].tracks_end(); ++i_vtxTrk) {
        //---- match the chsjet track to the track from the vertex ----
        reco::TrackRef trkRef(i_vtxTrk->castTo<reco::TrackRef>());
        trk2vtx[trkRef] = ivtx;
      }
    }
  }
    
  for (auto i_pfjetchs=patjetschs->begin(); i_pfjetchs!=patjetschs->end(); ++i_pfjetchs) { 
    if (!i_pfjetchs->isPFJet()) continue;

    //---- preselection -----------------
    int jetNo = i_pfjetchs-patjetschs->begin();
    if (fabs(i_pfjetchs->y()) > mMaxY or (i_pfjetchs->pt() < (jetNo<=3 ? mMinPFPtThirdJet : mMinPFPt))) continue;
    
    QCDPFJet qcdpfjetchs;
    double scaleCHS = 1./i_pfjetchs->jecFactor(0); // --- the value of the JEC factor
          
    //---- vertex association -----------
    float sumTrkPtCHS(0.0);
    //---- Practical parameters for CHS jets
    float sumTrkPtBetaPrimeCHS(0.0),sumTrkPtBetaCHS(0.0),sumTrkPtBetaStarCHS(0.0);
    
    // Dunno how useful these are in chs jets...
    int mpuTrk(0), mlvTrk(0); // # of pile-up tracks & lead-vertex tracks ## Juska
    int mjtTrk(0); // multiplicity of _all_ tracks in jet (also vtx-unassociated!) ## Juska
  
    auto PFCHSCandidates = i_pfjetchs->getPFConstituents();
    //---- loop over the tracks of the jet (take the track associated to jet constituent) ----
    if (trk2vtx.size()>0) {
      vector<reco::TrackRef> usedtrk;
      for (auto &cand : PFCHSCandidates) {
        auto trkRef = cand->trackRef();
        if (trkRef.isNonnull() and trkRef.isAvailable()) { 
          usedtrk.push_back(trkRef);
          auto trkPt = trkRef->pt();
          auto trkPdgId = abs(cand->pdgId());
          if (trkPdgId>10 and trkPdgId<20) { // Electrons and muons
            // Same logic as in PFCandidate::bestTrack(): for electrons gsfTracks are better
            if (trkPdgId==11) { 
              auto elTrkRef = cand->gsfTrackRef();
              if (elTrkRef.isNonnull() and elTrkRef.isAvailable()) trkPt = elTrkRef->pt();
            }
          }
          sumTrkPtCHS += trkPt;
          mjtTrk++; //Juska

          // Search for the vertex associated with this track
          auto vtxit = trk2vtx.find(trkRef);
          if (vtxit!=trk2vtx.end()) {
            int currvtx = vtxit->second;
            if (currvtx == 0) {
              sumTrkPtBetaCHS += trkPt;
              mlvTrk++; //Juska
            } else {
              sumTrkPtBetaStarCHS += trkPt;
              mpuTrk++; //Juska
            }
          } // if: track has vertex
        } // if: valid track
      } // for: all chs jet particles

      // A routine for hunting the betastar removed by chs (betaprime)
      auto vTrksCHS(i_pfjetchs->associatedTracks());
      for (auto i_trkchs = vTrksCHS.begin(); i_trkchs != vTrksCHS.end(); i_trkchs++) {
        // Skip tracks associated with chs jets
        if (std::find(usedtrk.begin(),usedtrk.end(),*i_trkchs)==usedtrk.end()) {
          // Take tracks associated with a vertex other than zero
          auto vtxit = trk2vtx.find(*i_trkchs);
          if (vtxit!=trk2vtx.end() and vtxit->second != 0)
              sumTrkPtBetaPrimeCHS += (*i_trkchs)->pt();
        }
      } // for: all tracks (non-chs included)
    } // if: tracks associated with vertices > 0
    
    qcdpfjetchs.setBeta(sumTrkPtCHS ? sumTrkPtBetaCHS/sumTrkPtCHS : 0.0);
    qcdpfjetchs.setBetaStar(sumTrkPtCHS ? sumTrkPtBetaStarCHS/sumTrkPtCHS : 0.0);
    qcdpfjetchs.setBetaPrime(sumTrkPtCHS ? sumTrkPtBetaPrimeCHS/sumTrkPtCHS : 0.0);
  
    //---- jec uncertainty --------------
    double uncCHS(0.0);
    vector<float> uncSrcCHS(0);
    if (mPFPayloadNameCHS != "") {
      mPFUncCHS->setJetEta(i_pfjetchs->eta());
      mPFUncCHS->setJetPt(i_pfjetchs->pt());
      uncCHS = mPFUncCHS->getUncertainty(true);
    } // if (mPFPayloadName != "")
    if (mPFJECUncSrcCHS != "") {
      for(unsigned isrc=0;isrc<mPFJECUncSrcNames.size();isrc++) {
        mPFUncSrcCHS[isrc]->setJetEta(i_pfjetchs->eta());
        mPFUncSrcCHS[isrc]->setJetPt(i_pfjetchs->pt());
        float unc1 = mPFUncSrcCHS[isrc]->getUncertainty(true);
        uncSrcCHS.push_back(unc1);
      } // for(unsigned isrc=0;isrc<mPFJECUncSrcNames.size();isrc++)
    } // if (mPFJECUncSrc != "")
    
    qcdpfjetchs.setP4(i_pfjetchs->p4());
    qcdpfjetchs.setCor(scaleCHS);
    qcdpfjetchs.setUnc(uncCHS);
    qcdpfjetchs.setUncSrc(uncSrcCHS);
    qcdpfjetchs.setArea(i_pfjetchs->jetArea());
    
    double chf   = i_pfjetchs->chargedHadronEnergyFraction();
    double nhf   = i_pfjetchs->neutralHadronEnergyFraction();// + i_pfjetchs->HFHadronEnergyFraction();
    double nemf  = i_pfjetchs->neutralEmEnergyFraction(); // equals to deprecated phf but has HF info too
    double cemf  = i_pfjetchs->chargedEmEnergyFraction(); // equals to deprecated elf
    double muf   = i_pfjetchs->muonEnergyFraction();
    double hf_hf = i_pfjetchs->HFHadronEnergyFraction();
    double hf_phf= i_pfjetchs->HFEMEnergyFraction();
    int hf_hm    = i_pfjetchs->HFHadronMultiplicity();
    int hf_phm   = i_pfjetchs->HFEMMultiplicity();
    int chm      = i_pfjetchs->chargedHadronMultiplicity();
    int nhm      = i_pfjetchs->neutralHadronMultiplicity();
    int phm      = i_pfjetchs->photonMultiplicity();
    int elm      = i_pfjetchs->electronMultiplicity();
    int mum      = i_pfjetchs->muonMultiplicity();
    int npr      = i_pfjetchs->chargedMultiplicity() + i_pfjetchs->neutralMultiplicity();
    
    float eta    = i_pfjetchs->eta();
    int cm       = i_pfjetchs->chargedMultiplicity();
     
    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID
    bool looseID, tightID;
    if ( fabs(eta) <= 2.7) {
       looseID = (nhf<0.99 && nemf<0.99 && npr > 1) && ((fabs(eta)<=2.4 && chf>0 && chm>0 && cemf <0.99) || fabs(eta)>2.4);
       tightID = (nhf<0.90 && nemf<0.90 && npr > 1) && ((fabs(eta)<=2.4 && chf>0 && chm>0 && cemf <0.99) || fabs(eta)>2.4);
       //OLD JET IDs, 
       //	 bool looseID = (nhf<0.99 && nemf<0.99 && npr>1 && muf<0.8) && ((fabs(eta) <= 2.4 && chf>0 && cm>0 && cemf<0.99) || fabs(eta)>2.4);
       //	 bool tightID = (nhf<0.90 && nemf<0.90 && npr>1 && muf<0.8) && ((fabs(eta)<=2.4 && chf>0 && cm>0 && cemf<0.90) || fabs(eta)>2.4);
    } else if ( fabs(eta) <= 3.0) {
       looseID = (nemf<0.90 && (npr - cm)>2 ); 
       tightID = (nemf<0.90 && (npr - cm)>2 ); 
    } else {
       looseID = (nemf<0.90 && (npr - cm)>10 ); 
       tightID = (nemf<0.90 && (npr - cm)>10 ); 
    }

    qcdpfjetchs.setLooseID(looseID);
    qcdpfjetchs.setTightID(tightID);
    qcdpfjetchs.setFrac(chf,nhf,nemf,cemf,muf);
    qcdpfjetchs.setMulti(npr,chm,nhm,phm,elm,mum,cm);
    qcdpfjetchs.setHFFrac(hf_hf,hf_phf);
    qcdpfjetchs.setHFMulti(hf_hm,hf_phm);
    
    double hof = i_pfjetchs->hoEnergyFraction(); // Juska
    qcdpfjetchs.setVtxInfo(mpuTrk,mlvTrk,mjtTrk);
    qcdpfjetchs.setHO(hof);
   
    double CSVpfPositive = i_pfjetchs->bDiscriminator("pfPositiveCombinedSecondaryVertexV2BJetTags");
    double CSVpfNegative = i_pfjetchs->bDiscriminator("pfNegativeCombinedSecondaryVertexV2BJetTags");

    double pfBoostedDoubleSecondaryVertex = i_pfjetchs->bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags");
    //C taggers
    double pfCombinedCvsL = i_pfjetchs->bDiscriminator("pfCombinedCvsLJetTags");
    double pfCombinedCvsB = i_pfjetchs->bDiscriminator("pfCombinedCvsBJetTags");

    float DeepCSVb   = i_pfjetchs->bDiscriminator("deepFlavourJetTags:probb");
    float DeepCSVc   = i_pfjetchs->bDiscriminator("deepFlavourJetTags:probc");
    float DeepCSVl   = i_pfjetchs->bDiscriminator("deepFlavourJetTags:probudsg");
    float DeepCSVbb  = i_pfjetchs->bDiscriminator("deepFlavourJetTags:probbb");
    float DeepCSVcc  = i_pfjetchs->bDiscriminator("deepFlavourJetTags:probcc");
    float DeepCSVbN  = i_pfjetchs->bDiscriminator("negativeDeepFlavourJetTags:probb");
    float DeepCSVcN  = i_pfjetchs->bDiscriminator("negativeDeepFlavourJetTags:probc");
    float DeepCSVlN  = i_pfjetchs->bDiscriminator("negativeDeepFlavourJetTags:probudsg");
    float DeepCSVbbN = i_pfjetchs->bDiscriminator("negativeDeepFlavourJetTags:probbb");
    float DeepCSVccN = i_pfjetchs->bDiscriminator("negativeDeepFlavourJetTags:probcc");
    float DeepCSVbP  = i_pfjetchs->bDiscriminator("positiveDeepFlavourJetTags:probb");
    float DeepCSVcP  = i_pfjetchs->bDiscriminator("positiveDeepFlavourJetTags:probc");
    float DeepCSVlP  = i_pfjetchs->bDiscriminator("positiveDeepFlavourJetTags:probudsg");
    float DeepCSVbbP = i_pfjetchs->bDiscriminator("positiveDeepFlavourJetTags:probbb");
    float DeepCSVccP = i_pfjetchs->bDiscriminator("positiveDeepFlavourJetTags:probcc");

    //the three recommended                                                                                                                                        
    double pfJetProbabilityBJetTags=i_pfjetchs->bDiscriminator("pfJetProbabilityBJetTags");
    double pfCombinedInclusiveSecondaryVertexV2BJetTags= i_pfjetchs->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
    double pfCombinedMVAV2BJetTags=i_pfjetchs->bDiscriminator("pfCombinedMVAV2BJetTags");
    
    float partonFlavour=-100;
    float partonFlavourPhysicsDef=-100;
    float hadronFlavour=-100;
    if (mIsMCarlo && mUseGenInfo) {
      cout << "Parton flav " << i_pfjetchs->partonFlavour() << endl;
      cout << "Hadron flav " << i_pfjetchs->hadronFlavour() << endl;
      cout << "Gen parton available " << bool(i_pfjetchs->genParton() != NULL) << endl;
      partonFlavour = i_pfjetchs->partonFlavour();
      hadronFlavour = i_pfjetchs->hadronFlavour();
      if (i_pfjetchs->genParton() != NULL) partonFlavourPhysicsDef = i_pfjetchs->genParton()->pdgId(); //it is not always defined!!
    }
    qcdpfjetchs.setFlavour(partonFlavour,hadronFlavour,partonFlavourPhysicsDef);
    
    float QGTagger=-100; 
    if (mAK4) QGTagger = i_pfjetchs->userFloat("QGTaggerAK4PFCHS:qgLikelihood");
    
    //Filling B-tag infos
    qcdpfjetchs.setPositiveNegativeCSV(CSVpfPositive,CSVpfNegative);
    qcdpfjetchs.setTagRecommended(pfJetProbabilityBJetTags,pfCombinedInclusiveSecondaryVertexV2BJetTags,pfCombinedMVAV2BJetTags);
    qcdpfjetchs.setDeepCSV(DeepCSVb, DeepCSVc, DeepCSVl, DeepCSVbb, DeepCSVcc,
                           DeepCSVbN, DeepCSVcN, DeepCSVlN, DeepCSVbbN, DeepCSVccN,
                           DeepCSVbP, DeepCSVcP, DeepCSVlP, DeepCSVbbP, DeepCSVccP);
    
    qcdpfjetchs.setQGTagger(QGTagger);	 
    qcdpfjetchs.setBoosted(pfBoostedDoubleSecondaryVertex);
    qcdpfjetchs.setCTagger(pfCombinedCvsL,pfCombinedCvsB);
    
    float pileupJetId = -999;
    if (i_pfjetchs->hasUserFloat(pfchsjetpuid)) pileupJetId = i_pfjetchs->userFloat(pfchsjetpuid);
    qcdpfjetchs.SetPUJetId(pileupJetId);
    
    if (mIsMCarlo) {
      GenJetCollection::const_iterator i_matchedchs;
      float rmin(999);
      for(GenJetCollection::const_iterator i_gen = genjets->begin(); i_gen != genjets->end(); i_gen++) {
        double deltaR = reco::deltaR(*i_pfjetchs,*i_gen);
        if (deltaR < rmin) {
          rmin = deltaR;
          i_matchedchs = i_gen;
        }
      }
      if (genjets->size() == 0) {
        LorentzVector tmpP4(0.0,0.0,0.0,0.0);
        qcdpfjetchs.setGen(tmpP4,0);
      } else
        qcdpfjetchs.setGen(i_matchedchs->p4(),rmin);
    } else {
      LorentzVector tmpP4(0.0,0.0,0.0,0.0);
      qcdpfjetchs.setGen(tmpP4,0);
    }
    mPFJetsCHS.push_back(qcdpfjetchs);
  } // for: chs Jets
  
  //---------------- met ---------------------------------------------
  Handle<pat::METCollection> pfmet;
  event.getByToken(mPFMET, pfmet);
  const pat::MET &met = pfmet->front();
  mPFMet.setVar(met.et(),met.sumEt(),met.phi());

  //-------------- fill the tree -------------------------------------
  sort(mPFJets.begin(),mPFJets.end(),sort_pfjets);
  mEvent->setEvtHdr(mEvtHdr);
  mEvent->setPFJetsCHS(mPFJetsCHS); // -- later substitute chs jets
  mEvent->setGenJets(mGenJets);
  mEvent->setGenFlavour(GenFlavour);
  mEvent->setGenFlavourPhysicsDef(GenPartonFlavourPhysicsDef);
  mEvent->setGenHadronFlavour(GenHadronFlavour);
  mEvent->setPFMET(mPFMet);
  mEvent->setL1Obj(mL1Objects);
  mEvent->setHLTObj(mHLTObjects);
  if ((mEvent->nPFJetsCHS() >= (unsigned)mMinNPFJets) ) {
    if ((mEvent->pfchsmjjcor(0) >= mMinJJMass) ) {
      //    cout<<"Feeling tree ----"<<endl;
      mTree->Fill();
    }
  }
}


/////////////// Matching Flavour ///////////////////////////////

int ProcessedTreeProducerBTag::getMatchedPartonGen(edm::Event const& event,GenJetCollection::const_iterator i_gen)
{
  int jetFlavour=-100;
  bool switchB=0;
  bool switchC=0;

  edm::Handle<reco::GenParticleCollection> genParticles;
  event.getByToken(mgenParticles, genParticles);

  for (size_t i = 0; i < genParticles->size (); ++i) {
    const GenParticle & genIt = (*genParticles)[i];
    int pdgId = genIt.pdgId();
    double DeltaR=deltaR(genIt.p4().eta(),genIt.p4().phi(),i_gen->eta(),i_gen->phi());
    double DeltaRmin=0.3;
    if (DeltaR < DeltaRmin ){
      DeltaRmin=DeltaR;
      if(abs(pdgId)==5){ jetFlavour=5; switchB=true;}
      if(abs(pdgId)==4){ jetFlavour=4; switchC=true;}
      if(abs(pdgId)<=3 && abs(pdgId)>=1){ jetFlavour=1; }
      if(abs(pdgId)==21){ jetFlavour=21; }
    }      
    if (switchB) {jetFlavour=5;}
    if (switchC && !switchB) {jetFlavour=4;}
  }
  return jetFlavour;
}

int ProcessedTreeProducerBTag::getMatchedHadronGen(edm::Event const& event,GenJetCollection::const_iterator i_gen)
{
  int jetFlavour=-100;

  edm::Handle<reco::GenParticleCollection> genParticles;
  event.getByToken(mgenParticles, genParticles);

  for (size_t i = 0; i < genParticles->size (); ++i) {
    const GenParticle & genIt = (*genParticles)[i];    
    int aid = abs(genIt.pdgId());
    if (aid/100 == 5 || aid/1000==5) {
      // 2J+1 == 1 (mesons) or 2 (baryons)
      if (aid%10 == 1 || aid%10 == 2) {
        // No B decaying to B
        if (aid != 5222 && aid != 5112 && aid != 5212 && aid != 5322) {
          double DeltaR=deltaR(genIt.p4().eta(),genIt.p4().phi(),i_gen->eta(),i_gen->phi());
          if(sqrt(DeltaR)<0.5){
            jetFlavour=5;
          }
          else jetFlavour=21;
        }
      }
    }
  }
  return jetFlavour;
}

//////////////////////////////////////////////////////////////////////////////////////////
ProcessedTreeProducerBTag::~ProcessedTreeProducerBTag() {}

DEFINE_FWK_MODULE(ProcessedTreeProducerBTag);
