// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>

namespace Rivet {

  class RICHARDSON_ULT : public Analysis {
  public:
    RIVET_DEFAULT_ANALYSIS_CTOR(RICHARDSON_ULT);

    void init() {
      eventCounter = 0;
      _csvData.reserve(1000); // Reserve space for CSV lines.
      _lastWriteIndex = 0;    // No CSV lines have been written yet.
    }

    /// Advances the decay chain for any particle.
    /// Follows the chain while there is exactly one child with the same PID,
    /// until a vertex is reached where the particle decays into two or more daughters.
    Particle advanceChain(const Particle &p) {
      Particle current = p;
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
      int eventID = eventCounter;
      // Loop over all particles to find a Higgs boson.
      for (const Particle &p : event.allParticles()) {
        if (p.pid() != PID::HIGGSBOSON) continue;
        
        Particle advancedHiggs = advanceChain(p);
        const Particles &higgsChildren = advancedHiggs.children();
        if (higgsChildren.size() != 2) continue;
        
        int pid0 = higgsChildren[0].pid();
        int pid1 = higgsChildren[1].pid();
        if (!((pid0 == 21 && pid1 == 21) || (std::abs(pid0) == 5 && std::abs(pid1) == 5)))
          continue;
        
        Particle parent1 = advanceChain(higgsChildren[0]);
        Particle parent2 = advanceChain(higgsChildren[1]);
        
        std::ostringstream oss;
        oss << eventID << "," << event.weights()[0] << ",";
        
        // Use the helper function to write CSV.
        oss << particleCSV(&advancedHiggs) << ",";
        oss << particleCSV(&parent1) << ",";
        oss << particleCSV(&parent2) << ",";
        
        bool validP1 = (parent1.children().size() == 2);
        bool validP2 = (parent2.children().size() == 2);
        Particle child1, child2, child3, child4;
        if (validP1) {
          const Particles &p1children = parent1.children();  // cache children
          child1 = advanceChain(p1children[0]);
          child2 = advanceChain(p1children[1]);
        }
        if (validP2) {
          const Particles &p2children = parent2.children();
          child3 = advanceChain(p2children[0]);
          child4 = advanceChain(p2children[1]);
        }
        oss << particleCSV(validP1 ? &child1 : nullptr) << ",";
        oss << particleCSV(validP1 ? &child2 : nullptr) << ",";
        oss << particleCSV(validP2 ? &child3 : nullptr) << ",";
        oss << particleCSV(validP2 ? &child4 : nullptr) << ",";
        
        bool validChild1 = validP1 && (child1.children().size() == 2);
        bool validChild2 = validP1 && (child2.children().size() == 2);
        bool validChild3 = validP2 && (child3.children().size() == 2);
        bool validChild4 = validP2 && (child4.children().size() == 2);
        Particle gc1, gc2, gc3, gc4, gc5, gc6, gc7, gc8;
        if (validChild1) {
          const Particles &ch1children = child1.children();
          gc1 = advanceChain(ch1children[0]);
          gc2 = advanceChain(ch1children[1]);
        }
        if (validChild2) {
          const Particles &ch2children = child2.children();
          gc3 = advanceChain(ch2children[0]);
          gc4 = advanceChain(ch2children[1]);
        }
        if (validChild3) {
          const Particles &ch3children = child3.children();
          gc5 = advanceChain(ch3children[0]);
          gc6 = advanceChain(ch3children[1]);
        }
        if (validChild4) {
          const Particles &ch4children = child4.children();
          gc7 = advanceChain(ch4children[0]);
          gc8 = advanceChain(ch4children[1]);
        }
        oss << particleCSV(validChild1 ? &gc1 : nullptr) << ",";
        oss << particleCSV(validChild1 ? &gc2 : nullptr) << ",";
        oss << particleCSV(validChild2 ? &gc3 : nullptr) << ",";
        oss << particleCSV(validChild2 ? &gc4 : nullptr) << ",";
        oss << particleCSV(validChild3 ? &gc5 : nullptr) << ",";
        oss << particleCSV(validChild3 ? &gc6 : nullptr) << ",";
        oss << particleCSV(validChild4 ? &gc7 : nullptr) << ",";
        oss << particleCSV(validChild4 ? &gc8 : nullptr);
        
        _csvData.push_back(oss.str());
        break; // Process one valid chain per event.
      }
      eventCounter++;
    }

    // Merge subanalyses if necessary.
    void merge(const Analysis &other) {
      const RICHARDSON_ULT &otherAnalysis = dynamic_cast<const RICHARDSON_ULT&>(other);
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
      if (_lastWriteIndex == 0 && !fileExists) {
        // Build header: 2 event columns + 15 particles * 5 entries each = 77 columns.
        csvOut << "EventID,EventWeight,"
               << "HiggsPID,HiggsE,Higgspx,Higgspy,Higgspz,"
               << "P1PID,P1E,P1px,P1py,P1pz,"
               << "P2PID,P2E,P2px,P2py,P2pz,"
               << "C1PID,C1E,C1px,C1py,C1pz,"
               << "C2PID,C2E,C2px,C2py,C2pz,"
               << "C3PID,C3E,C3px,C3py,C3pz,"
               << "C4PID,C4E,C4px,C4py,C4pz,"
               << "GC1PID,GC1E,GC1px,GC1py,GC1pz,"
               << "GC2PID,GC2E,GC2px,GC2py,GC2pz,"
               << "GC3PID,GC3E,GC3px,GC3py,GC3pz,"
               << "GC4PID,GC4E,GC4px,GC4py,GC4pz,"
               << "GC5PID,GC5E,GC5px,GC5py,GC5pz,"
               << "GC6PID,GC6E,GC6px,GC6py,GC6pz,"
               << "GC7PID,GC7E,GC7px,GC7py,GC7pz,"
               << "GC8PID,GC8E,GC8px,GC8py,GC8pz"
               << std::endl;
      }
      for (size_t i = _lastWriteIndex; i < _csvData.size(); ++i) {
        csvOut << _csvData[i] << "\n";
      }
      _lastWriteIndex = _csvData.size();
      csvOut.close();
    }

  private:
    int eventCounter;
    std::vector<std::string> _csvData;
    size_t _lastWriteIndex; // Tracks the number of lines already written.

    // New helper to convert particle data to CSV.
    std::string particleCSV(const Particle* ptcl) const {
      if (ptcl)
        return std::to_string(ptcl->pid()) + "," + std::to_string(ptcl->momentum().E()) + "," +
               std::to_string(ptcl->momentum().px()) + "," + std::to_string(ptcl->momentum().py()) + "," +
               std::to_string(ptcl->momentum().pz());
      else
        return "0,0,0,0,0";
    }
  };

  RIVET_DECLARE_PLUGIN(RICHARDSON_ULT);

} // namespace Rivet
