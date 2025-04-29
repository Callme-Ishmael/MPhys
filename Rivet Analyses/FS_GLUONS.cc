// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include <iostream>

namespace Rivet {

  class FS_GLUONS : public Analysis {
  public:
    /// Constructor
    FS_GLUONS()
      : Analysis("FS_GLUONS"), _eventCount(0)
    { }

    /// Book histograms and declare projections
    void init() {
      declare(FinalState(), "FS");

      // Histogram: number of final-state gluons from Higgs per event
      book(_h_numHiggsGluons, "HIGGS_GLUONS", 51, -0.5, 50.5);
    }

    /// Per-event analysis
    void analyze(const Event &event) {
      const FinalState& fs = apply<FinalState>(event, "FS");

      int totalHiggsGluons = 0;

      // Loop only over true final-state particles
      for (const Particle& p : fs.particles()) {
        if (p.pid() == 21 && hasHiggsAncestor(p)) {
          ++totalHiggsGluons;
        }
      }

      std::cout << "Event " << _eventCount << ": "
                << totalHiggsGluons << " final-state gluons from Higgs\n";

      _h_numHiggsGluons->fill(totalHiggsGluons, 1.0);
      ++_eventCount;
    }

    /// Finalize: normalize and print summary
    void finalize() {

      std::cout << "Processed " << _eventCount << " events.\n";
      std::cout << "Sum of weights: " << sumOfWeights() << std::endl;
    }

  private:
    /// Recursively check if the particle has a Higgs ancestor
    bool hasHiggsAncestor(const Particle& p) {
      for (const Particle& parent : p.parents()) {
        if (parent.pid() == 25) return true;
        if (hasHiggsAncestor(parent)) return true;
      }
      return false;
    }

    Histo1DPtr _h_numHiggsGluons;
    int _eventCount;
  };

  RIVET_DECLARE_PLUGIN(FS_GLUONS);

}
