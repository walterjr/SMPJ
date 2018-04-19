//Author K. Kousouris
//Modified by: S. Ganguly

#ifndef QCDEvent_h
#define QCDEvent_h
#include "SMPJ/AnalysisFW/interface/QCDJet.h"
#include "SMPJ/AnalysisFW/interface/QCDMET.h"
#include "SMPJ/AnalysisFW/interface/QCDCaloJet.h"
#include "SMPJ/AnalysisFW/interface/QCDPFJet.h"
#include "SMPJ/AnalysisFW/interface/QCDEventHdr.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include <vector>

class QCDEvent
{
    public:
      typedef reco::Particle::LorentzVector LorentzVector;
      //------------ Constructor ------------------------------
      QCDEvent();
      //------------ Destructor -------------------------------
      ~QCDEvent();
      //------------ Set methods ------------------------------
      void setPFMET(const QCDMET& fPFMET)                         {PFMet_ = fPFMET;}
      void setEvtHdr(const QCDEventHdr& fEvtHdr)                  {EvtHdr_ = fEvtHdr;}
      void setPFJetsCHS(const std::vector<QCDPFJet>& fPFJetsCHS);

      void setGenJets(const std::vector<LorentzVector>& fGenJets);
      void setL1Obj(const std::vector<std::vector<LorentzVector> >& fL1Obj);
      void setHLTObj(const std::vector<std::vector<LorentzVector> >& fHLTObj);
      void setPrescales(const std::vector<int>& fPreL1, const std::vector<int>& fPreHLT) {L1Prescale_ = fPreL1; HLTPrescale_ = fPreHLT;}
      void setTrigDecision(const std::vector<int>& fTrigDecision) {TriggerDecision_ = fTrigDecision;}

      void setGenFlavour(const std::vector<float> GenFlavour){ genFlavour_= GenFlavour; }
      void setGenHadronFlavour(const std::vector<float> GenFlavourHadron){ genFlavourHadron_= GenFlavourHadron; }
      void setGenFlavourPhysicsDef(const std::vector<float> GenPartonFlavourPhysicsDef){ genFlavourPartonPhysicsDef_= GenPartonFlavourPhysicsDef; }

      //------------ Get methods -------------------------------
      unsigned int nTriggers()                         const {return TriggerDecision_.size();}
      unsigned int nL1Obj(int i)                       const {return L1Obj_[i].size();}
      unsigned int nHLTObj(int i)                      const {return HLTObj_[i].size();}
      unsigned int nPFJetsCHS()                        const {return PFJetsCHS_.size();}
      unsigned int nGenJets()                          const {return GenJets_.size();}
      int nGoodJets(int unc, int id, float ymax, float ptmin, std::vector<QCDJet> jets);
      int fired(int i)                                 const {return TriggerDecision_[i];}
      int preL1(int i)                                 const {return L1Prescale_[i];}
      int preHLT(int i)                                const {return HLTPrescale_[i];}

      float GenJetFlavour(int i)                       const {return genFlavour_[i];}
      float GenHadronJetFlavour(int i)                       const {return genFlavourHadron_[i];}
      float GenPartonPhysicsDefJetFlavour(int i)                       const {return genFlavourPartonPhysicsDef_[i];}

      float pfmjj();
      float genmjj();
      float pfchsmjjcor(int unc);
      float pfchsmjjcor(int unc,int src);
      float pfmjjgen();
      const QCDMET&        pfmet()                     const {return PFMet_;}
      const LorentzVector& hltobj(int itrig, int iobj) const {return (HLTObj_[itrig])[iobj];}
      const LorentzVector& l1obj(int itrig, int iobj)  const {return (L1Obj_[itrig])[iobj];}
      const LorentzVector& genjet(int i)               const {return GenJets_[i];}
      const QCDPFJet&      pfjetchs(int i)             const {return PFJetsCHS_[i];}
      const QCDEventHdr&   evtHdr()                    const {return EvtHdr_;}

      const std::vector<std::vector<LorentzVector>>& HLTObj() const {return HLTObj_;}
      const std::vector<LorentzVector>& hltObjsForPath(int i) const {return HLTObj_[i];}

    private:
      //---- event header (contains all the event info) --------------
      QCDEventHdr                              EvtHdr_;
      //---- PF met object -------------------------------------------
      QCDMET                                   PFMet_;
      //---- trigger decision vector ---------------------------------
      std::vector<int>                         TriggerDecision_;
      //---- L1 prescale vector --------------------------------------
      std::vector<int>                         L1Prescale_;
      //---- HLT prescale vector -------------------------------------
      std::vector<int>                         HLTPrescale_;
      //---- HLT objects ---------------------------------------------
      std::vector<std::vector<LorentzVector> > HLTObj_;
      //---- L1 objects ----------------------------------------------
      std::vector<std::vector<LorentzVector> > L1Obj_;
      //---- Genjets -------------------------------------------------
      std::vector<LorentzVector>               GenJets_;
      //---- PFJetsCHS -----------------------------------------------
      std::vector<QCDPFJet>                    PFJetsCHS_;
      std::vector<float>  genFlavour_;
      std::vector<float>  genFlavourHadron_;
      std::vector<float>  genFlavourPartonPhysicsDef_;
};
#endif
