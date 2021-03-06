//Author K. Kousouris
//Modified by: S. Ganguly

#ifndef QCDPFJetBTag_h
#define QCDPFJetBTag_h
#include "SMPJ/AnalysisFW/interface/QCDJet.h"
#include "TLorentzVector.h"
class QCDPFJetBTag : public QCDJet {
  public:
    //------------ Constructor ------------------------------
    QCDPFJetBTag() {}
    //------------ Destructor -------------------------------
    ~QCDPFJetBTag() {}
    //------------ Set methods ------------------------------

    void setFlavour(float fpartonflavour, float fhadronflavour, float fpartonflavourPhysicsDef) {partonFlavour_ = fpartonflavour; hadronFlavour_ = fhadronflavour; partonFlavourPhysicsDef_ = fpartonflavourPhysicsDef;}

    void setQGTagger(float fQGTagger) {QGtagger_ = fQGTagger;}

    float pfBoostedDouble()  const {return pfBoosted_;} 

    float partonflavour()      const {return partonFlavour_;}
    float partonflavourPhysicsDef()      const {return partonFlavourPhysicsDef_;}
    float hadronflavour()      const {return hadronFlavour_;}

    float qgtagger()      const {return QGtagger_;}

    float pfCombinedCvsL() const {return pfCombinedCvsL_;}
    float pfCombinedCvsB() const {return pfCombinedCvsB_;}

    float pfBoosted_;
    float pfCombinedCvsL_, pfCombinedCvsB_;
    float pfDeepCSVb_, pfDeepCSVc_, pfDeepCSVl_, pfDeepCSVbb_;
    float pfDeepFlavourb_, pfDeepFlavourc_, pfDeepFlavourg_, pfDeepFlavourl_, pfDeepFlavourbb_;
    float pfBTag_JetProb_;
    float pfBTag_CombInclSecVtxV2_;
    float pfBTag_CombMVAV2_; 

    float QGtagger_;

    float partonFlavour_;
    float partonFlavourPhysicsDef_;
    float hadronFlavour_;
};
#endif
