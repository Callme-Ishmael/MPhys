// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include <iostream>
#include <map>
#include <vector>
#include <set>
#include <algorithm>

namespace Rivet {

  class HIGGS_3PLUS : public Analysis {
  private:
    // Map: key = sorted vector of children PIDs, value = count of events
    std::map<std::vector<int>, unsigned int> _decayCounts;

  public:
    RIVET_DEFAULT_ANALYSIS_CTOR(HIGGS_3PLUS);

    void init() {
      // No projections needed as we access HepMC particles directly.
    }

    void analyze(const Event& event) {
      // Use a set to avoid counting the same decay channel more than once per event.
      std::set<std::vector<int>> eventDecayChannels;

      // Loop over all particles in the event.
      for (const Particle& p : event.allParticles()) {
        if (p.pid() == 25) { // Check for a Higgs boson.
          if (p.children().size() >= 3) { // Only consider decays with 3 or more children.
            // Collect the children pids.
            std::vector<int> childrenPIDs;
            for (const Particle& child : p.children()) {
              childrenPIDs.push_back(child.pid());
            }
            // Sort the vector so that, for example, (1, 2, 3) and (3, 2, 1) are identical.
            std::sort(childrenPIDs.begin(), childrenPIDs.end());
            // Insert this decay channel into the event-local set.
            eventDecayChannels.insert(childrenPIDs);
          }
        }
      }
      // For each unique decay channel observed in this event, increment the counter.
      for (const auto& channel : eventDecayChannels) {
         _decayCounts[channel]++;
      }
    }

    // The merge() method combines results from thread-local instances.
    void merge(const Analysis & other) {
      const HIGGS_3PLUS & that = dynamic_cast<const HIGGS_3PLUS&>(other);
      for (const auto & entry : that._decayCounts) {
        _decayCounts[entry.first] += entry.second;
      }
    }

    void finalize() {
      // Print out each decay channel and how many events contained that channel.
      std::cout << "Higgs decays with 3 or more children:" << std::endl;
      for (const auto & entry : _decayCounts) {
         std::cout << "Higgs decayed to (";
         bool first = true;
         for (int pid : entry.first) {
             if (!first) std::cout << ", ";
             std::cout << pid;
             first = false;
         }
         std::cout << ") ---> in " << entry.second << " event" 
                   << (entry.second > 1 ? "s" : "") << std::endl;
      }
    }
  };

  RIVET_DECLARE_PLUGIN(HIGGS_3PLUS);

}
