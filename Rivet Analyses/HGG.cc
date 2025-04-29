// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>

namespace Rivet {

  class HGG : public Analysis {
  public:

    RIVET_DEFAULT_ANALYSIS_CTOR(HGG);

    void init() {
      _csvData.reserve(1000);
      _lastWriteIndex = 0;
    }

    // Check if the particle is a quark (u, d, s, c, b, t, or antiparticles)
    bool isQuark(int pid) {
      int absPid = std::abs(pid);
      return (absPid == 1 || absPid == 2 || absPid == 3 || absPid == 4 || absPid == 5 || absPid == 6);
    }

    // Advance through correction chains (e.g. g -> g -> g), return last corrected particle
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

    // Extract: g → X + Y (both quarks)
    std::vector<Particle> extract_g_to_2(const Particle& gstart) {
      Particle g_corrected = advanceChain(gstart);
      const Particles& g_children = g_corrected.children();
      if (g_children.size() != 2) return {};  // Must decay to exactly two particles

      // Check if both children are quarks
      Particle c1 = advanceChain(g_children[0]);
      Particle c2 = advanceChain(g_children[1]);
      if (!isQuark(c1.pid()) || !isQuark(c2.pid())) return {};

      return {c1, c2};
    }

    void analyze(const Event &event) {
      for (const Particle &p : event.allParticles()) {
        if (p.pid() != PID::HIGGSBOSON) continue;

        Particle higgs = advanceChain(p);
        const Particles &children = higgs.children();
        if (children.size() != 2) continue;

        // Check if the children are gluons
        Particle g1 = advanceChain(children[0]);
        Particle g2 = advanceChain(children[1]);
        if (!(g1.pid() == 21 && g2.pid() == 21)) continue;

        // Extract the quark children of each gluon
        std::vector<Particle> g1Children = extract_g_to_2(g1);
        std::vector<Particle> g2Children = extract_g_to_2(g2);

        if (g1Children.size() != 2 || g2Children.size() != 2) continue;

        // Prepare the CSV entry
        std::ostringstream oss;
        oss << event.weights()[0] << ",";
        oss << particleCSV(&g1) << ",";
        oss << particleCSV(&g2) << ",";
        oss << particleCSV(&g1Children[0]) << ",";
        oss << particleCSV(&g1Children[1]) << ",";
        oss << particleCSV(&g2Children[0]) << ",";
        oss << particleCSV(&g2Children[1]);

        _csvData.push_back(oss.str());
        break; // One Higgs per event
      }
    }

    void finalize() {
      std::ofstream csvOut("hgg_quark_children.csv", std::ios::app);
      csvOut << "EventWeight,g1PID,g1E,g1px,g1py,g1pz,g2PID,g2E,g2px,g2py,g2pz,c1PID,c1E,c1px,c1py,c1pz,c2PID,c2E,c2px,c2py,c2pz,c3PID,c3E,c3px,c3py,c3pz,c4PID,c4E,c4px,c4py,c4pz" << std::endl;
      for (const std::string& line : _csvData)
        csvOut << line << std::endl;
    }

  private:
    std::vector<std::string> _csvData;
    size_t _lastWriteIndex;

    std::string particleCSV(const Particle* ptcl) const {
      if (!ptcl) return "0,0,0,0,0";
      const FourMomentum& p4 = ptcl->momentum();
      return std::to_string(ptcl->pid()) + "," +
             std::to_string(p4.E()) + "," +
             std::to_string(p4.px()) + "," +
             std::to_string(p4.py()) + "," +
             std::to_string(p4.pz());
    }
  };

  RIVET_DECLARE_PLUGIN(HGG);

} // namespace Rivet
