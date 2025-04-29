// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include <iostream>
#include <map>
#include <vector>
#include <set>
#include <algorithm>
#include <sstream>
#include <cmath>  // for std::abs

namespace Rivet {

  // Helper function to map a PID to a particle name.
  std::string particleName(int pid) {
    int absPid = std::abs(pid);
    if (absPid == 24) return "W";
    if (absPid == 23) return "Z";
    if (absPid == 15) return "τ";
    if (absPid == 5)  return "b";
    if (absPid == 4)  return "c";
    if (absPid == 21) return "g";
    if (absPid == 11) return "e";
    if (absPid == 22) return "γ";
    if (absPid == 3) return "s";
    if (absPid == 13) return "µ";
    std::stringstream ss;
    ss << pid;
    return ss.str();
  }

  class HIGGS_DECAY_PROFILE : public Analysis {
  private:
    // Map: key = sorted vector of daughter PIDs, value = sum of event weights for that decay channel.
    std::map<std::vector<int>, double> _decayWeights;

  public:
    RIVET_DEFAULT_ANALYSIS_CTOR(HIGGS_DECAY_PROFILE);

    void init() {
      // No projections needed as we directly access HepMC particles.
    }

    void analyze(const Event& event) {
      // Retrieve the nominal event weight.
      double eventWeight = event.weights()[0];

      // Use a set to avoid counting the same decay channel more than once per event.
      std::set<std::vector<int>> eventDecayChannels;

      // Loop over all particles looking for Higgs (PID 25).
      for (const Particle& p : event.allParticles()) {
        if (p.pid() == 25) {
          // Only consider decays with 2 or more daughters.
          if (p.children().size() >= 2) {
            std::vector<int> childrenPIDs;
            for (const Particle& child : p.children()) {
              childrenPIDs.push_back(child.pid());
            }
            // Sort the vector so the order is canonical.
            std::sort(childrenPIDs.begin(), childrenPIDs.end());
            eventDecayChannels.insert(childrenPIDs);
          }
        }
      }

      // For each unique decay channel in this event, add its event weight.
      for (const auto& channel : eventDecayChannels) {
        _decayWeights[channel] += eventWeight;
      }
    }

    // Merge results from thread-local instances.
    void merge(const Analysis & other) {
      const HIGGS_DECAY_PROFILE & that = dynamic_cast<const HIGGS_DECAY_PROFILE&>(other);
      for (const auto & entry : that._decayWeights) {
        _decayWeights[entry.first] += entry.second;
      }
    }

    void finalize() {
      // For channels with exactly 2 daughters, we print the two-body result.
      std::map<std::string, double> twoBodyChannels;
      // For three-body decays, we aggregate weights for WW and ZZ.
      double threeBodyWW = 0.0;
      double threeBodyZZ = 0.0;

      for (const auto & entry : _decayWeights) {
        const std::vector<int>& channel = entry.first;
        double weight = entry.second;
        if (channel.size() == 2) {
          std::string key = particleName(channel[0]) + ", " + particleName(channel[1]);
          twoBodyChannels[key] += weight;
        }
        else if (channel.size() == 3) {
          // For three-body decays, check if any daughter is a W or Z.
          bool hasW = std::any_of(channel.begin(), channel.end(), [](int pid) { return std::abs(pid) == 24; });
          bool hasZ = std::any_of(channel.begin(), channel.end(), [](int pid) { return std::abs(pid) == 23; });
          if (hasW) threeBodyWW += weight;
          if (hasZ) threeBodyZZ += weight;
        }
      }

      // Print two-body decay channels.
      for (const auto & entry : twoBodyChannels) {
        std::cout << "Higgs decayed to " << entry.first 
                  << " in this many events: " << entry.second << std::endl;
      }
      // Print three-body aggregated channels.
      if (threeBodyWW > 0.0)
        std::cout << "Higgs decayed to W W in this many events: " << threeBodyWW << std::endl;
      if (threeBodyZZ > 0.0)
        std::cout << "Higgs decayed to Z Z in this many events: " << threeBodyZZ << std::endl;
    }
  };

  RIVET_DECLARE_PLUGIN(HIGGS_DECAY_PROFILE);

} // namespace Rivet
