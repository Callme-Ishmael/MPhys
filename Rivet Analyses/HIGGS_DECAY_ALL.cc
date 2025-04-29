// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include <iostream>
#include <map>
#include <vector>
#include <set>
#include <algorithm>

namespace Rivet {

  class HIGGS_DECAY_ALL : public Analysis {
  private:
    // Map: key = sorted vector of daughter PIDs, value = count of events
    std::map<std::vector<int>, unsigned int> _decayCounts;

  public:
    RIVET_DEFAULT_ANALYSIS_CTOR(HIGGS_DECAY_ALL);

    void init() {
      // No projections are needed as we access HepMC particles directly.
    }

    void analyze(const Event& event) {
      // Use a set to avoid counting the same decay channel more than once per event.
      std::set<std::vector<int>> eventDecayChannels;

      // Loop over all particles in the event.
      for (const Particle& p : event.allParticles()) {
        if (p.pid() == 25) { // Higgs boson.
          // Check if the Higgs decays into two or more daughters.
          if (p.children().size() >= 2) {
            // Collect the daughter PIDs.
            std::vector<int> childrenPIDs;
            for (const Particle& child : p.children()) {
              childrenPIDs.push_back(child.pid());
            }
            // Sort the vector so that the order is canonical.
            std::sort(childrenPIDs.begin(), childrenPIDs.end());
            // Insert this decay channel into the event-local set.
            eventDecayChannels.insert(childrenPIDs);
          }
        }
      }

      // For each unique decay channel observed in this event, increment the overall counter.
      for (const auto& channel : eventDecayChannels) {
        _decayCounts[channel]++;
      }
    }

    // The merge() method combines results from thread-local instances.
    void merge(const Analysis & other) {
      const HIGGS_DECAY_ALL & that = dynamic_cast<const HIGGS_DECAY_ALL&>(other);
      for (const auto & entry : that._decayCounts) {
        _decayCounts[entry.first] += entry.second;
      }
    }

    void finalize() {
      // Print out each decay channel and how many events contained that channel.
      std::cout << "Higgs decay counts for decays with 2 or more daughters:" << std::endl;
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

  RIVET_DECLARE_PLUGIN(HIGGS_DECAY_ALL);

} // namespace Rivet
