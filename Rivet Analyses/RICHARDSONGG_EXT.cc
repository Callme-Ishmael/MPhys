// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>

namespace Rivet {

  class RICHARDSONGG_EXT : public Analysis {
  public:
    RIVET_DEFAULT_ANALYSIS_CTOR(RICHARDSONGG_EXT);

    void init() {
      eventCounter = 0;
      _csvData.reserve(1000); // Reserve space for CSV lines.
      _lastWriteIndex = 0;    // No CSV lines have been written yet.
    }

    /// Advances the gluon decay chain.
    /// If a gluon has exactly one child and that child has the same PID,
    /// follow that branch until a vertex is reached where it decays into two particles.
    Particle advanceGluonChain(const Particle &g) {
      Particle current = g;
      while (true) {
        const Particles &children = current.children();
        if (children.size() == 1 && children[0].pid() == current.pid()) {
          current = children[0];
        } else {
          break;
        }
      }
      return current;
    }

    void analyze(const Event &event) {
      // Loop over all particles to find a Higgs boson.
      for (const Particle &p : event.allParticles()) {
        if (p.pid() == PID::HIGGSBOSON) {
          const Particles &higgsChildren = p.children();
          // Ensure the Higgs decays into exactly two particles.
          if (higgsChildren.size() != 2)
            continue;
          // Check that both daughters are gluons (PID 21).
          if (higgsChildren[0].pid() != 21 || higgsChildren[1].pid() != 21)
            continue;
          
          // Advance the chain for both gluons from the Higgs decay.
          Particle g1 = advanceGluonChain(higgsChildren[0]);
          Particle g1prime = advanceGluonChain(higgsChildren[1]);
          
          // For the chain, require that g1 decays into exactly two gluons.
          const Particles &g1Children = g1.children();
          if (g1Children.size() != 2)
            continue;
          if (g1Children[0].pid() != 21 || g1Children[1].pid() != 21)
            continue;
          
          // Advance the chain for both daughters of g1.
          Particle g2 = advanceGluonChain(g1Children[0]);
          Particle g3 = advanceGluonChain(g1Children[1]);
          
          // g2 must further decay into two gluons.
          const Particles &g2Children = g2.children();
          if (g2Children.size() != 2)
            continue;
          if (g2Children[0].pid() != 21 || g2Children[1].pid() != 21)
            continue;
          
          // Advance the chain for both daughters of g2.
          Particle g4 = advanceGluonChain(g2Children[0]);
          Particle g5 = advanceGluonChain(g2Children[1]);
          
          // Build the decay chain structure.
          DecayChainInfo info;
          info.higgs       = p;
          info.gluon1      = g1;
          info.gluon1prime = g1prime;
          info.gluon2      = g2;
          info.gluon3      = g3;
          info.gluon4      = g4;
          info.gluon5      = g5;
          
          // Build CSV line: eventID, then PID and four-momenta.
          std::ostringstream oss;
          oss << eventCounter << ",";
          // Higgs.
          oss << info.higgs.pid() << ","
              << info.higgs.momentum().E() << ","
              << info.higgs.momentum().px() << ","
              << info.higgs.momentum().py() << ","
              << info.higgs.momentum().pz() << ",";
          // Gluon1.
          oss << info.gluon1.pid() << ","
              << info.gluon1.momentum().E() << ","
              << info.gluon1.momentum().px() << ","
              << info.gluon1.momentum().py() << ","
              << info.gluon1.momentum().pz() << ",";
          // Gluon1prime.
          oss << info.gluon1prime.pid() << ","
              << info.gluon1prime.momentum().E() << ","
              << info.gluon1prime.momentum().px() << ","
              << info.gluon1prime.momentum().py() << ","
              << info.gluon1prime.momentum().pz() << ",";
          // Gluon2.
          oss << info.gluon2.pid() << ","
              << info.gluon2.momentum().E() << ","
              << info.gluon2.momentum().px() << ","
              << info.gluon2.momentum().py() << ","
              << info.gluon2.momentum().pz() << ",";
          // Gluon3.
          oss << info.gluon3.pid() << ","
              << info.gluon3.momentum().E() << ","
              << info.gluon3.momentum().px() << ","
              << info.gluon3.momentum().py() << ","
              << info.gluon3.momentum().pz() << ",";
          // Gluon4.
          oss << info.gluon4.pid() << ","
              << info.gluon4.momentum().E() << ","
              << info.gluon4.momentum().px() << ","
              << info.gluon4.momentum().py() << ","
              << info.gluon4.momentum().pz() << ",";
          // Gluon5.
          oss << info.gluon5.pid() << ","
              << info.gluon5.momentum().E() << ","
              << info.gluon5.momentum().px() << ","
              << info.gluon5.momentum().py() << ","
              << info.gluon5.momentum().pz();
          
          _csvData.push_back(oss.str());
        }
      }
      eventCounter++;
    }

    // Merge subanalyses if necessary.
    void merge(const Analysis &other) {
      const RICHARDSONGG_EXT &otherAnalysis = dynamic_cast<const RICHARDSONGG_EXT&>(other);
      _csvData.insert(_csvData.end(), otherAnalysis._csvData.begin(), otherAnalysis._csvData.end());
    }

    // Write only the new CSV lines since the last write.
    // Do not write the header if the file already exists.
    void finalize() {
      bool fileExists = false;
      {
        std::ifstream infile("chain_data_ext.csv");
        fileExists = infile.good();
      }
      std::ofstream csvOut("chain_data_ext.csv", std::ios::app);
      // Write header only if this is the first write and the file does not exist.
      if (_lastWriteIndex == 0 && !fileExists) {
        csvOut << "EventID,"
               << "higgsPID,higgsE,higgspx,higgspy,higgspz,"
               << "gluon1PID,gluon1E,gluon1px,gluon1py,gluon1pz,"
               << "gluon1primePID,gluon1primeE,gluon1primepx,gluon1primepy,gluon1primepz,"
               << "gluon2PID,gluon2E,gluon2px,gluon2py,gluon2pz,"
               << "gluon3PID,gluon3E,gluon3px,gluon3py,gluon3pz,"
               << "gluon4PID,gluon4E,gluon4px,gluon4py,gluon4pz,"
               << "gluon5PID,gluon5E,gluon5px,gluon5py,gluon5pz"
               << std::endl;
      }
      // Write only the new events.
      for (size_t i = _lastWriteIndex; i < _csvData.size(); ++i) {
        csvOut << _csvData[i] << "\n";
      }
      // Update the index to mark these events as written.
      _lastWriteIndex = _csvData.size();
      csvOut.close();
    }

  private:
    int eventCounter;
    std::vector<std::string> _csvData;
    size_t _lastWriteIndex; // Tracks the number of lines already written.

    /// Structure holding copies of the particles in the extended decay chain.
    struct DecayChainInfo {
      Particle higgs;
      Particle gluon1;      // g1: from H decay that decays further
      Particle gluon1prime; // g1': the other gluon from H decay
      Particle gluon2;      // g2: first daughter of g1 that decays further
      Particle gluon3;      // g3: second daughter of g1
      Particle gluon4;      // g4: first daughter of g2
      Particle gluon5;      // g5: second daughter of g2
    };
  };

  RIVET_DECLARE_PLUGIN(RICHARDSONGG_EXT);

} // namespace Rivet
