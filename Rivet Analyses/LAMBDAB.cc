#include "Rivet/Analysis.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Projections/FinalState.hh"

namespace Rivet {

  class LAMBDAB : public Analysis {
  public:
    RIVET_DEFAULT_ANALYSIS_CTOR(LAMBDAB);

    /// Initialize the analysis.
    void init() {
      // No projections are needed since we loop over all particles.
    }

    /// Analyze each event by scanning all particles.
    void analyze(const Event &event) {
      bool foundLambdaB = false;
      bool foundAntiLambdaB = false;
      
      // Loop over all particles in the event.
      for (const Particle &p : event.allParticles()) {
        if (p.pid() == 5122)
          foundLambdaB = true;
        if (p.pid() == -5122)
          foundAntiLambdaB = true;
        // If both are found, we can break early.
        if (foundLambdaB && foundAntiLambdaB)
          break;
      }
      
      // Increment the total event counter.
      _totalEvents++;
      
      // Count the event only if both a Lambda_b and an anti-Lambda_b are found.
      if (foundLambdaB && foundAntiLambdaB)
        _bothCount++;
    }

    /// Finalize the analysis: output the event counts and fraction.
    void finalize() {
      double fraction = 0.0;
      if (_totalEvents > 0)
        fraction = static_cast<double>(_bothCount) / _totalEvents;
      MSG_INFO("Number of events with both a Lambda_b baryon and anti-Lambda_b baryon: " << _bothCount);
      MSG_INFO("Total number of events: " << _totalEvents);
      MSG_INFO("Fraction of events with both: " << fraction);
    }

  private:
    int _totalEvents = 0;  ///< Total number of processed events.
    int _bothCount = 0;    ///< Number of events containing both a Lambda_b baryon and anti-Lambda_b baryon.
  };

  RIVET_DECLARE_PLUGIN(LAMBDAB);

} // namespace Rivet
