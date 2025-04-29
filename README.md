# MPhys

# Week 1 (27.01 - 2.02)

## 30.01.2025

### Summary of last semester

In the preceding semester, we initiated a study of CP violation in Higgs-fermion interactions within the framework of the Standard Model Effective Field Theory (SMEFT). Focusing on processes such as $$pp \to ZH \to e^+e^-b\bar{b}$$ and $$pp \to H b\bar{b},$$

we employed `MadGraph5_aMC@NLO` for event generation, constructing CP-sensitive observables from parton-level kinematic variables. However, a significant limitation emerged: MadGraph fixes the helicities of final-state particles at generation, preventing the preservation of spin correlations crucial for probing CP-violating interference effects. This constraint rendered many CP-sensitive observables ineffective and underscored the need for a more sophisticated treatment of spin.

Consequently, in the present phase of the project, we transitioned to using `Herwig`, an event generator that preserves spin correlations throughout the hard scattering, parton shower, and hadronization stages. In this semester, the focus is placed on the realistic study of the process $$pp \to Z \to ZH,$$ with the Higgs boson decaying to $$b\bar{b}.$$ Crucially, the b-quarks are allowed to shower and hadronize, enabling an analysis of CP-sensitive observables based on the true, physically accessible final states — b-jets — rather than on artificially modified decay chains.

This transition represents a significant improvement in the physical realism of the study. Unlike previous exploratory work that relied on unphysical setups, the present work targets the direct Higgs decay into bottom quarks under experimentally relevant conditions. By leveraging `Herwig`'s spin-preserving evolution, we aim to construct and analyze observables capable of revealing the CP nature of the Higgs-bottom coupling, thereby contributing towards a deeper understanding of possible new sources of CP violation in the Higgs sector.

### The Noether Cluster

We use the **Noether Cluster** of UoM to perform computationally intensive tasks such as event generation and showering.

Access and usage are structured as follows:

- **Login Node:**  
  Used only for lightweight operations such as file transfers, compiling code, and submitting jobs.  
  **Heavy computations must not be performed here.**

- **Worker Nodes:**  
  Computations are performed on worker nodes, accessed via the HTCondor scheduler.  
  Users must _copy critical code and data back_ to permanent storage (e.g., home or Lab directories) before the interactive session ends.

More detailed instructions are available in the repository under **`Noether_Managers/Nother.md`**, which provides a comprehensive "How to use Noether" guide.

Reference: [Noether Basic Usage Tutorial](https://github.com/MANHEP/maf-helpdesk/blob/master/noether_basic_usage.md)

---

### Basic Workflow

1. **Connect to Noether:**
   ```bash
   ssh abercaru@noether.hep.manchester.ac.uk
   ```

2. **Submit an interactive HTCondor session:**
   ```bash
   condor_submit -i getenv=True
   ```

3. **Inside the worker node:**
   - The current working directory is a **local scratch directory** (e.g., `/scratch/condor_pool/condor/dir_xxxxxxx`).
   - Heavy I/O operations should be confined to this local directory.
   - To access your permanent home directory at any time:
     ```bash
     cd /gluster/home/abercaru
     ```

4. **Useful Commands:**
   - Copy files between Noether and local machine using `scp`. Example:
     ```bash
     scp abercaru@noether.hep.manchester.ac.uk:/gluster/data/atlas/abercaru/SM_test/LHC-FRModel.hepmc .
     ```
   - Activate Herwig environment:
     ```bash
     source /gluster/data/theory/mphysproject/ana-karim/activate_herwig.sh
     ```

---

**Notes:**
- The scratch directory is **temporary** and local to the worker node.
- Sessions are **time-limited** (typically two hours of inactivity will cause logout).
- _Always copy important results back to permanent storage after the computation ends._

For a full guide on efficient Noether usage, troubleshooting common errors, and maximizing cluster resources, please refer to the **Nother.md** tutorial in the **Noether_Managers** folder of this repository.



A notable limitation: Noether access requires being inside the university network; VPN access is not available. To address this, we plan to also configure a home workstation capable of running Herwig and Rivet using Docker containers.

### Local Setup: Using Docker for Herwig and Rivet

To enable event generation and analysis outside Noether, we configure **Docker containers** for both Herwig and Rivet. Docker images are lightweight, standalone, and executable packages containing all necessary components — code, libraries, dependencies, and system tools — while sharing the host’s operating system kernel. This makes them significantly more efficient than traditional virtual machines.

### Rivet 4.0.3 Docker Setup

The Rivet environment is launched using:

```bash
docker run --rm -it -v /mnt/d/Samples:/data hepstore/rivet bash
```

Once inside the container, a Rivet analysis can be executed with:

```bash
rivet -a MC_VH2BB -o /data/MC_VH2BB_output.yoda /data/LHC.hepmc
```

Here, the `.yoda` output file is stored inside the mounted `/data` directory.

### Herwig 7.3.0 Docker Setup

Similarly, the Herwig environment is started using:

```bash
docker run --rm -it -v /mnt/d/Samples:/data herwigcollaboration/herwig-7.3:7.3.0 Herwig bash
```

This allows for local event generation and parton showering directly within the Docker container environment. A lengthy tutorial on how to run Herwig and Rivet on your own machine can be found here: https://phab.hepforge.org/w/herwigtutorial/ but more one this later...


### First Contact with Herwig

**Date:** 01.02.2025

To begin familiarizing ourselves with Herwig, we explored its internal event generation architecture. Herwig's event generation process is modular, with different handlers responsible for various stages of event evolution. Each handler can be individually modified, enabled, or disabled depending on the analysis goals.

#### Understanding Herwig's Modular Structure

The main handlers include:

- **CascadeHandler**:  
  Responsible for modeling parton showers. Disabling it (`set EventHandler:CascadeHandler NULL`) turns off all showering.

- **MPIHandler**:  
  Models multiple parton interactions (MPI), i.e., simultaneous secondary interactions in the same proton-proton collision. Disabling it (`set EventHandler:CascadeHandler:MPIHandler NULL`) prevents additional soft/secondary parton-parton scatters.

- **DecayHandler**:  
  Manages particle decays. Setting it to NULL disables the decay of unstable particles within Herwig.

- **HadronizationHandler**:  
  Handles the hadronization process, where partons are converted into hadrons. Disabling it (`set EventHandler:HadronizationHandler NULL`) stops the formation of hadrons, leaving the event at the partonic level.

Understanding these components is critical for tailoring the event generation to match different levels of physical realism, depending on the analysis goals.

![image](https://github.com/user-attachments/assets/b192b794-73e6-4a0c-801f-ab39ece3e0f7)


#### Basic Workflow for Event Generation

Herwig's event generation typically follows a structured workflow:

1. **Reading the Input File**:  
   Prepare an input file (e.g., `LHC-Matchbox.in`) that specifies the process and settings. Then execute:

   ```bash
   Herwig read LHC-Matchbox.in
   ```

   This step initializes the process and creates a `.run` file containing the compiled setup.

2. **Running the Simulation**:  
   Generate events using the `.run` file:

   ```bash
   Herwig run LHC-Matchbox.run -N 100
   ```

   Here, `-N 100` specifies the number of events to generate.

3. **Analyzing the Output**:  
   The output includes event records and logs that can be analyzed to study the generated events. Tools like Rivet can be integrated for further analysis.

#### Key Observations

- **Disabling CascadeHandler and MPIHandler**:  
  Leads to events without any parton showers or underlying events, isolating the hard scattering process.

- **Disabling DecayHandler**:  
  Results in final states where unstable particles (e.g., Higgs, top quark) remain undecayed unless decayed manually.

- **Disabling HadronizationHandler**:  
  Provides parton-level final states, allowing direct study of quark and gluon distributions without the complications of hadronization.

These explorations are crucial for understanding the impact of each component on the final event structure and for tailoring simulations to specific analysis needs.

#### Additional Resources

For a more in-depth understanding and advanced configurations, refer to the [Herwig Tutorials](https://herwig.hepforge.org/tutorials/) and the [Herwig 7.2 Documentation](https://herwig.hepforge.org/tutorials/gettingstarted/firstrun.html).

---

### Integrating SMEFTsim Couplings into Herwig

**02.02.2025**  
An essential requirement is the inclusion of CP-odd couplings, as featured in the SMEFTsim or adapted Christoph models. Two approaches are considered:

- **Option 1 – Using LHE Files:**
  1. Generate events with MadGraph.
  2. Output LHE (Les Houches Event) files (`output madevent mysim`).
  3. Import these LHE files into Herwig using the `LHEReader` for showering, MPI, and hadronization.

- **Option 2 – UFO to Herwig Conversion:**
  1. Use Herwig’s `ufo2herwig` tool.
  2. Generate a native Herwig model input file directly from the UFO model.

Reference: [Herwig UFO Tutorial](https://herwig.hepforge.org/tutorials/bsm/ufo.html)

We are initially attempting Option 2 to avoid dependency on MadGraph for event generation, aiming for a cleaner, Herwig-native workflow.

### First Input File Setup

Drafted a first trial input file (`LHE.in`) that references a MadGraph-generated `.lhe` file for Herwig to read and evolve. The workflow:

1. Generate `.lhe` events via MadGraph.
2. Reference the `.lhe` file in a Herwig input file.
3. Run Herwig for full event evolution.

Nonetheless, direct model integration via `ufo2herwig` remains the preferred long-term solution.


# Week 2 (03.02.2025 – 09.02.2025)

## Focus of the Week

This week was dedicated to investigating the practical methods for interfacing MadGraph event generation with Herwig showering, while preserving critical spin correlation information necessary for CP-violation studies.

---

## Attempted Strategy: Option 1 (LHE Workflow)

We explicitly tested **Option 1**, namely:

1. Generate `.lhe` files using MadGraph with the SMEFTsim model.
2. Feed the `.lhe` files into Herwig using `LHEReader` for showering, MPI, and hadronization.

This approach initially succeeded in producing `.hepmc` output files containing both stable final states and intermediate particle information (important for jet substructure studies). We confirmed that `.hepmc` files could be analyzed using **Rivet** and **PyHepMC** for truth-level analyses, such as jet clustering and jet constituent correlations.

---

## Critical Problem: Loss of Spin Correlations

Following deeper discussions with **Sid**, **Aidin**, and input from **Andy**, a fundamental flaw was identified:

- MadGraph, when producing `.lhe` files, **fixes helicities** and **zeroes out** off-diagonal elements of the spin density matrix.
- Once MadGraph writes the `.lhe` file, the spin correlations relevant to CP-violating interference effects are **irretrievably lost**.
- Herwig cannot reconstruct or invent this missing spin information after reading the `.lhe`.

The core physics we aim to study — interference effects between different helicity states of the \( b\bar{b} \) pair from the Higgs decay — requires preserving these off-diagonal spin density matrix elements.  
Thus, **Option 1 is fundamentally insufficient** for the goals of this project.

---

## Investigated Alternative: Option 2 (UFO2Herwig)

As a result, we began exploring **Option 2**:

- Convert the UFO model (SMEFTsim) into a Herwig-usable format using `ufo2herwig`.
- Generate matrix elements inside Herwig, allowing it to control the amplitude-level information and reconstruct the spin density matrix.

Initial attempts to use UFO2Herwig succeeded in basic event generation at **tree level**. However, limitations were observed:
- Loop-induced processes like gluon-gluon fusion (ggF) are not fully supported at tree level.
- Parameter setting within Herwig is nontrivial and might require manual editing of the UFO model's `parameters.py`.

Thus, while Option 2 offers promise, it remains technically challenging and requires further development.

---

## Technical Progress and Cluster Work

- Established personal data directories in `/gluster/data/atlas/` to store run outputs (due to limited home directory quotas).
- Activated Herwig using:
  ```bash
  source /gluster/data/theory/event-generators/herwig/activate_herwig.sh
  ```
- Understood basic Herwig workflow:
  ```bash
  Herwig read input.in
  Herwig run input.run
  ```
- Gained practical experience with Unix cluster commands (`scp`, `cp`, `rm`, `mv`, `ls`, etc.).
- Resolved technical issues such as source activation and correct file paths for `.lhe` ingestion.

---

## Summary of Discussions

- **ROOT files** skip intermediate particles — `.hepmc` files must be used for full event record analysis.
- **Sid** and **Aidin** confirmed that `.lhe` files lose spin correlations.
- **Matrix element access** through MadGraph (rather than `.lhe`) is necessary for CP studies.
- **LO (tree-level)** matrix element generation inside Herwig using UFO2Herwig was achieved, but limitations exist for loop processes.
- Discussions on **future direction** include using **OpenLoops** to supply loops into Herwig for full event simulation.

---

## Immediate Next Steps

- Continue developing UFO2Herwig path and attempt to incorporate loops (via OpenLoops).
- Set up basic Rivet analysis framework on `.hepmc` output for preliminary truth-level studies (jet reconstruction, b-jet correlations).
- Investigate manual control of parameters inside SMEFTsim UFO models for flexible generation.
- Follow up on matrix element interfacing between MadGraph and Herwig to correctly handle helicity amplitudes.

---

> For full technical guidance on cluster operations, refer to the `Noether_Managers/Nother.md` guide inside the repository.



In addition to the wide range of internal BSM models it is possible to use most models using the UFO format with Herwig. **Herwig can currently only handle the perturbative Lorentz structures which arise in the coupling of particles but in most cases this is sufficient.**



# Week 3 (10.02.2025 – 16.02.2025)

## Focus of the Week

During this week, we officially abandoned the approach of using MadGraph-generated LHE files as input to Herwig, following confirmation that spin correlations are irreversibly lost at the LHE stage. Instead, we moved to the strategy of using MadGraph purely as a matrix element generator, interfaced directly with Herwig through the Matchbox framework. This shift was necessary to preserve the delicate interference effects critical to our CP-violation study.

---

## Summary of Progress

Our first objective was to import the SMEFTsim model into Herwig using the `ufo2herwig` converter. This effort revealed multiple issues. The SMEFTsim UFO was originally written in Python 2, while Herwig expects Python 3 compatible models. We attempted conversion using both the `2to3` tool and the `--convert` option in `ufo2herwig`, but even after these adjustments, the conversion failed. Herwig raised errors about unsupported vertices and unrecognized Lorentz structures, particularly for 4-point interactions.

We then attempted to follow the terminal suggestion of using the `--include-generic` option, but this led to a new Python error inside Herwig’s ThePEG framework, related to a deprecated `sort()` function. Manual modification of ThePEG’s Python files was attempted, but given the scale of the changes needed, we ultimately abandoned this path.

Instead, we adopted a more practical workaround: we modified `general_lorentz.py` to simply skip any unsupported vertices rather than crash. This allowed the conversion to complete, producing `.model` and `.so` files. However, many vertices were skipped, particularly all four-point interactions and some critical three-point vertices like \( Z \to \mu^+ \mu^- \). Fortunately, the \( ggh \) and \( hbb \) vertices required for gluon-gluon fusion and Higgs decay to \( b\bar{b} \) were not among those skipped.

In parallel, we tested Christoph’s custom UFO model. This model converted successfully without any manual intervention. However, Christoph’s model lacks effective gluon-gluon-Higgs vertices, making it unsuitable for simulating gluon fusion processes. As a result, we shifted focus to studying the associated production process \( pp \to ZH \to (\ell^+\ell^-)(b\bar{b}) \), where these vertices are not required.

At this stage, we encountered a new practical limitation. The Herwig installation on the Noether cluster only supported two UFO models, `loop_sm` and `heft`. Custom models such as ours, even after successful conversion, could not be loaded because the corresponding `.so` shared object files were not integrated into the Herwig build. Sid and Aidin began working on patching the Herwig installation to allow loading of external `.so` files.

Following discussions with our supervisor and Herwig experts, we also adopted a stricter philosophy for the event generation chain. We committed to using MadGraph only as a matrix element provider, ensuring that Herwig could assemble the full spin density matrix without introducing artificial spin correlations. OpenLoops was to be excluded wherever possible, with the aim of working purely at tree level for initial tests.

Finally, we started constructing custom `.in` files for Herwig, specifying manual settings for the collision energy, PDF set, matrix element generation, process selection, and event handling, based on the Matchbox formalism. Parallel to this, we continued working on Rivet for future analysis, preparing to handle `.hepmc` outputs and exploring methods to produce `.h5` files for machine learning inputs.

This shift in methodology was summarized and communicated to our supervisor via a detailed series of emails, supported by mind maps outlining the new workflow. Here are the emails for reference

---


![image](https://github.com/user-attachments/assets/fe26d12b-1d49-419a-bf92-8cf59f5d6e62)


-------------------------------
# Week 4 (17.02 - 23.02)

We performed a basic truth-level analysis using the **MC_VH2BB** Rivet routine:  
🔗 [MC_VH2BB Analysis Page](https://heprivet.gitlab.io/analysis/analist/mc_vh2bb/)

#### **Run Details**

- **Simulated process**: `pp → V H → (ℓν / ℓ⁺ℓ⁻)(b b̄)`,  
  where the Higgs decays hadronically to $b\bar{b}$, and the vector boson decays leptonically (electron or muon channels).
- Applied a **transverse momentum cut**:  
  $p_T(Z) > 100 \, \text{GeV}$,  
  placing us in a **boosted regime**.

---

#### **Jet Multiplicity**

We observe events with **0 to 3 b-jets**, despite the boost applied to the Z.  
While some jet merging or splitting effects are expected, the frequency of **0 or 1 b-jet events** is somewhat surprising and warrants further investigation.

**Possible contributing factors:**
- Particle-level b-tagging inefficiencies  
  (e.g., b-hadrons falling outside the jet cone or below the tagging threshold),
- Jet–lepton **overlap removal** may discard valid b-jets,
- Limitations in the **Rivet projection logic**.

<img src="https://github.com/user-attachments/assets/f87c8ed1-9171-4387-a0c2-8daec2bfeaee" width="500" height="500"/><img src="https://github.com/user-attachments/assets/6230b8c0-2e00-4197-84f6-7ec436875a6a" width="500" height="500"/>

---

#### **Invariant Mass of $b\bar{b}$ Pair**

The invariant mass distribution of the leading two b-jets **does not resemble a clean Higgs peak**.

While there is an enhancement near $m_H \sim 125\, \text{GeV}$,  
the distribution exhibits a **significant asymmetric tail towards lower masses**.

This **low-mass tail** is unexpected for well-reconstructed $H \to b\bar{b}$ decays.  
In a typical truth-level analysis, we would expect a roughly Gaussian peak centred at the Higgs mass.





**Potential causes:**
- Mismatched jet pairing (e.g., using jets not from the Higgs decay),
- Misidentified or missed b-jets,
- Energy mismeasurement or clustering artifacts.

  

> [!TIP]
>   Meeting Verbatim – 20 February 2025  
> - We produced two samples of pure CP-even and CP-odd events.  
> - The framework is designed to track spin correlations. Spin correlations should be implemented here, but we’re not yet certain that they are.  
> - **Action:** Ask Mike if Herwig provides any verbose output confirming that the spin density matrix has been calculated.  
> - **Question:** What plots would you generate as a Herwig developer? There’s a difference between making fancy plots and verifying that spin correlations are enabled—perhaps there is an output option that confirms their inclusion.  
> - A pTₘᵢₙ cut of 100 GeV is applied to the Z boson itself, giving it a slight boost.  
> - A histogram of jet multiplicity shows 0–3 b-jets.  
> - **Next step:** Ask Sid to review how Rivet is configured. Broadly speaking, Rivet projects observables and performs particle-level b-tagging by identifying a b-hadron within the jet cone with pT above a threshold.  
> - **Clarification:** In a highly boosted system, both b-hadrons could merge into one jet, yielding only one b-jet. Although this is unlikely for a 100 GeV cut on the Z, it’s worth understanding.  
> - Alternatively, a b-hadron might fall below the pT threshold or outside the cone. I expect these to be few-percent effects; if higher, our truth-level definition is problematic. We need to inspect whether Rivet correctly traces upstream cascade particles and uses PDG IDs to tag b-hadrons.  
> - At detector level, observing 0 or 1 b-jets is acceptable (∼60 % efficiency). How can there be zero? Neither jet contains a b-hadron.  
> - Overlap removal can also remove jets: if a lepton overlaps a jet, the jet is excluded.  
> - **To do:** Document each stage’s cuts and prepare a list to share over Skype.  
> - **Question:** Why do the jets appear back-to-back? (Answer: by construction—need to specify which step enforces this.)  
> - Applying a 30 GeV cut on jets causes significant loss because boosting the Higgs system shifts events into the high-pT tail. The isotropic pT distribution of a Higgs decaying at rest changes when boosted, and a tight cut selects only the tail.  
> - **Test:** Lower the jet pT threshold and see if b-jet multiplicity increases.  
> - **Proposal:** Require exactly two jets for the selection, then proceed with further analysis.  
> - I will apply the jet-finder algorithm; then use object-level cuts to remove jets overlapping leptons. Select events with exactly two jets, reconstruct their invariant mass, and check for a peak at the Higgs mass.  
> - For examples of selection cuts, see the ATLAS ZH observation paper—its kinematic cuts will guide our ZH analysis.  
> - Compare and contrast their cuts in your report. Also review the b-tag definition: it includes a pT cut on the hadron and should be configurable, since FastJet does clustering but not b-tagging (handled by Rivet).  
> - We suspect Rivet tags b-hadrons at truth level by inspecting the HepMC record. Experimentally, you must correct detector-level b-jet definitions to a consistent truth-level definition. At detector level, a b-jet is identified via a reconstructed secondary vertex within the jet, displaced from the primary vertex (reflecting the b-hadron’s finite lifetime), along with other kinematic variables.  
> - **Send:** ATLAS truth-particle note from the Top group, outlining the rationale and principles behind the truth-level particle definition.

---------

### Detangling the Jets Algorithms b-tagging: what's going on

b-tagging is the technique used to identify jets that probably come from b-quarks. This is based on a few signatures:

- **Displaced vertex**: B-hadrons live long enough (~10⁻¹² s) to travel some distance before decaying. That decay happens at a vertex that's not at the primary collision point — and this secondary vertex is one of the main handles for tagging.

- **Impact parameter**: The tracks from the B-hadron decay tend to have large impact parameters — i.e., they don’t point back neatly to the primary vertex, which helps distinguish them from light-quark jets.

- **Soft leptons & other tricks**: You can also catch things like soft muons or electrons from semileptonic B decays. Useful but not always present.

---

#### When does the b-hadron form?

Yes, b-hadrons come after the initial showering. Here's the rough picture:

1. **Hard scatter**: Happens at the primary vertex. In our case, this is `pp → ZH`, and the Higgs decays to `b b̄` immediately — so the b-quarks are produced right at the primary vertex.

2. **Parton showering**: Almost instantaneous (~10⁻²⁴ s). The b-quarks radiate gluons — this happens close to the primary vertex.

3. **Hadronization**: The b-quarks turn into B-hadrons (e.g., B⁰, B⁺, Λ_b, etc). Still happens very close to the PV.

4. **Decay → secondary vertex**: The B-hadrons then travel some measurable distance before decaying — which is what gives us the displaced vertex for tagging.

---

#### Detector vs Truth Level

This came up in the context of how deep the tagging algorithm is allowed to look.

- **Truth-level tagging**: You go into the generator-level record and trace jet ancestry. You can say: “this jet came from a b-quark” because you have access to the full decay tree. This is not how experiments work — it’s useful for validation, not real analysis.

- **Detector-level tagging**: You only use what a detector would actually see — tracks, hits, vertices, calorimeter deposits. If a vertex is reconstructed well enough and is displaced, and has tracks with large impact parameters, it gets tagged.

**Important:** If your tagging algorithm relies on info that would require you to see inside the event history (like PDG IDs or ancestry), then it’s not detector-level tagging anymore.

---

#### Open questions / things to check

- Is Rivet tagging b-jets using truth info (e.g., looking for a b-hadron in the jet cone)?
- If yes → that’s not detector-level. It won’t capture real-world inefficiencies.
- If a b-hadron flies too far before decaying, or decays outside acceptance, does that affect the multiplicity we're seeing?
- Are we losing jets due to overlap removal with leptons?

These are probably what’s behind the weird 0 or 1 b-jet cases, even in a boosted setup.

---

#### Diagram context

Useful sketch (attached below) shows the full chain: from hard scatter to EM showers, jets, and what the detector "sees." Good for visualizing where things are happening in space/time — especially useful for understanding where the secondary vertex sits and how far we are from truth info when tagging.

![image](https://github.com/user-attachments/assets/15f4039d-839b-4556-a305-6f7f251b4495)

### Jet Clustering with the Anti-$k_t$ Algorithm

In our truth-level analysis, jets were reconstructed using the Anti-$k_t$ clustering algorithm, which is the standard choice for LHC experiments. Anti-$k_t$ is a sequential recombination algorithm that clusters particles based on a distance measure, favoring the creation of nearly conical jets. Specifically, it defines a distance between particles $i$ and $j$ as

$$
d_{ij} = \text{min}(p_{Ti}^{-2}, p_{Tj}^{-2}) \frac{\Delta R_{ij}^2}{R^2},
$$

where $\Delta R_{ij}$ is the separation in rapidity–azimuth space, and $R$ is the jet radius parameter. A distance to the beam is also defined as

$$
d_{iB} = p_{Ti}^{-2}.
$$

The algorithm iteratively merges the pair of objects with the smallest $d_{ij}$, or declares an object a final jet if $d_{iB}$ is smaller. Because of the inverse weighting by transverse momentum, hard particles act as centers that draw in softer ones, resulting in regular, circular jets that are resilient against soft contamination and pile-up.

This behavior is particularly important for analyses involving boosted Higgs bosons, where closely spaced decay products from $H \to b\bar{b}$ must be clustered into distinct jets without being excessively broadened by underlying event activity. In our study, we verified that Anti-$k_t$ appropriately reconstructs well-separated b-jets when the Higgs is modestly boosted, although merging effects may still become non-negligible at higher boosts or tighter radius parameters.


-----------------------------------
### How to make your own Rivet Analysis

```bash
mkdir ANALYSIS_X
cd ANALYSIS_X
rivet-mkanalysis ANALYSIS_X
# Edit and work in the ANALYSIS_X.cc file
rivet-build RivetANALYSIS_X.so ANALYSIS_X.cc
export RIVET_ANALYSIS_PATH=$PWD
rivet --analysis=ANALYSIS_X /data/LHC-PPZHbbee_odd.hepmc
rivet-mkhtml /data/ANALYSIS_X/Rivet.yoda -o /data/ANALYSIS_X/html_plots
```


-------------------------------
# Week 5 (24.02 - 2.03)

### Understanding Rivet: Projections and Analysis Flow

In Rivet, the structure of an analysis is organized around the concept of **projections**. A projection is a modular algorithm that extracts a particular physical feature from the event record, such as clustering final-state particles into jets (using FastJet), selecting isolated leptons, or computing invariant masses. The design philosophy of Rivet emphasizes modularity and reproducibility, allowing analyses to be portable across different event generators.

Each Rivet analysis consists of two main phases. The first is the `init()` function, which is executed once at the beginning of the run. During this phase, all projections required by the analysis are declared and registered. For instance, if jets are needed, the analysis declares a `FastJets` projection, specifying parameters such as the clustering algorithm (e.g., anti-\(k_T\)) and the radius parameter \( R \). Similarly, projections for identifying final-state leptons or photons are declared here, often using helper projections like `FinalState` or `DressedLeptons`.

The second phase is the `analyze()` function, which is executed once for each event. Here, the previously declared projections are used to retrieve the corresponding objects in the current event. The analysis logic is implemented at this stage: cuts are applied, observables are computed, and histograms are filled. For example, after retrieving a list of reconstructed jets from the `FastJets` projection, the analysis might impose a minimum transverse momentum threshold, select b-tagged jets, and compute the invariant mass of the leading two jets.

Histograms are declared during the `init()` stage using the `book()` function, and filled during `analyze()` using the `fill()` method. This ensures that Rivet manages histogram normalization and output automatically, enforcing consistency across analyses.

At the end of the run, the `finalize()` function is called. This is where the histograms are normalized, scaled if necessary, and prepared for output. Typically, Rivet outputs histograms in the `.yoda` format, a standardized, human-readable data format designed for particle physics analyses.

An essential feature of Rivet is that all projections and analyses are based solely on the truth-level information available in the event record, without reference to detector-specific effects. This ensures that Rivet analyses remain generator-independent and reproducible, allowing for meaningful generator validation and physics comparisons.

When developing a new Rivet analysis, it is crucial to carefully define the selection criteria, object reconstruction, and observable computation exclusively through projections and event record data, avoiding any assumptions about experimental detector performance. This guarantees that the analysis captures only the physics embedded in the event generator, free from detector effects.


### Deconstructing the Rivet Analysis

I'm looking into how `getOption` works in Rivet and how parameters like `PTJMIN` are passed in from the command line. Summary:

- `getOption<T>(...)` pulls in values set via `rivet -a MC_VH2BB:PTJMIN=40`, and stores them in member variables like `_jetptcut` inside the analysis class.
- Example:
  ```cpp
  _jetptcut = getOption<double>("PTJMIN", 30.0) * GeV;

→ Defaults to 30 GeV unless overridden.

### Jet-Lepton Contamination & Vetoing Strategy

I tried vetoing jets if they contain an `e+ e−` pair with invariant mass ≈ `mZ`. The idea was to remove leptons from the Z before they mess with the jet algorithm. But this leads to events with **< 2 jets**, which is a problem since we're after events with **2 b-jets**.

Alternatives:

#### Option 1 — Lepton origin tracing (without hard truth tagging):

- Look at final state leptons.
- Check `ΔR` between each lepton and secondary vertices (truth-level).
- If a lepton is close to a b-decay vertex → assume it came from the b-jet.
- Whatever’s left should be from the Z → mark those as invisible *before* running the jet finder.
- After jets are built, bring the leptons back for analysis.

This feels like a hack to avoid full truth-level tagging. In a detector, lepton origin is inferred from tracks and EM clusters — so this kind of masking might not be needed or justified.

**Better framing:**

- Identify which leptons come from Z → dR or vertex association.
- Remove them before jet finding.
- Add them back after jets are defined.

---

### On QCD Backgrounds

QCD background removal is tempting to do at truth level, but that’s not how real detectors work — we need to avoid this.

---

> [!message] Skype – 26.01.2025  
> - File issue was due to a truncated HEPMC file.  
> - Rivet 3.1.8 and 4.0.3 give **same histograms** → we’re good to go.  
> - Let’s build on `MC_VH2BB` for **2 b-jet selection**.  
> - **To check**: Are spin correlations on in Herwig?  
>   - The input file doesn’t mention “spin” at all.  
>   - Ask Mike if there’s any verbose output that confirms spin matrices are being calculated.  
> - Reminder: Read the **ATLAS truth particle note** (Top group).

---

### ATLAS ZH Paper Notes (27.01.2025)
https://arxiv.org/pdf/1808.08238

We want to see how consistent the cuts imposed by MVH2BB are with the ATLAS studies of ZH

- `H → bb̄` = 58% branching ratio.
- ggF production swamped by QCD → VH production (Z or W + H) is preferred for cleaner triggering.
- Boosted selection increases S/B ratio.

![image](https://github.com/user-attachments/assets/31b31e17-a126-489a-9efa-16e0bf7024a9)

#### Jet selection:

- Algorithm: anti-kt, R = 0.4
- Jet pT cuts:
  - Central: pT > 20 GeV
  - Forward: pT > 30 GeV
  - Leading b-jet: pT > 45 GeV
- b-tag: b-hadron within ΔR < 0.3 and pT > 5 GeV
- 2 loose leptons; one with pT > 27 GeV
- m(ll) ≈ mZ
- Boost regions:
  - High: pT^V > 150 GeV
  - Medium: 75 < pT^V < 150 GeV
 
### Key Observations

- The `MC_VH2BB` Rivet analysis functions correctly. We've now fully understood its logic and structure.
- It mirrors the ATLAS Run 2 analysis for \( ZH, H \to b\bar{b} \) closely, including:
  - A 30 GeV minimum \( p_T \) cut on jets, which is justified.
  - Use of `DileptonFinder` to dress and veto leptons before jet clustering via FastJet, reducing lepton–jet overlap issues.

So, in principle, this analysis provides a robust starting point for our study.
 
----------
### Theoretical Note on Spin Correlations

This week we focused entirely on understanding the Rivet framework in depth. We implemented custom projections, which now allow us to search the event record at truth level. This includes access to the full decay structure and particle ancestry, enabling us to track spin-relevant quantities from the initial hard process down to the final-state observables.

### Spin Correlation Test (Adapted from Bernreuther)

Using the method from [hep-ph/9701347](https://arxiv.org/pdf/hep-ph/9701347), originally developed for studying spin correlations in $$t\bar{t}$$ decays, we constructed a test to assess whether spin information is preserved in our simulation of $$H \to b\bar{b}$$. The procedure is:

- Identify the Higgs boson in the event record.
- Follow its decay to the two b-quarks.
- Define two decay branches from the b and $$\bar{b}$$, and trace each branch through the parton shower and hadronisation.
- For each branch, identify the **last B-hadron** before decay.
- Store the momentum and decay structure of that B-hadron as a proxy for the original b-quark spin information.

This allows for a truth-level observable that can potentially capture spin correlations passed down from the Higgs decay.

A second reference [arXiv:1410.6362](https://arxiv.org/pdf/1410.6362) provides context on using truth-level observables to probe CP and spin effects in hadronic decays. Relevant for validating the above method.


As part of validating whether Herwig is correctly preserving spin correlations in $$H \to b\bar{b}$$, I took a closer look at the theoretical framework laid out in Bernreuther et al. ([hep-ph/9701347](https://arxiv.org/pdf/hep-ph/9701347)). Their analysis is built for the case of $$\phi \to t\bar{t}$$, but the methodology generalises.

They start from a Yukawa-like interaction for a mixed CP Higgs:

<p align="center">
  𝓛<sub>Y</sub> = − (m<sub>f</sub> / v) &nbsp; <b>f̄</b> (a<sub>f</sub> + iγ<sub>5</sub>ã<sub>f</sub>) <b>f</b> φ
</p>

so the decay products can carry scalar and pseudoscalar components depending on (a<sub>f</sub>, ã<sub>f</sub>).  
The key insight is that this structure imprints itself in the spin density matrix of the final-state fermion pair.  
They write this matrix as:

<p align="center">
  R = A ⋅ 𝟙 ⊗ 𝟙 + B<sub>i</sub><sup>+</sup> σ<sup>i</sup> ⊗ 𝟙 + B<sub>i</sub><sup>-</sup> 𝟙 ⊗ σ<sup>i</sup> + C<sub>ij</sub> σ<sup>i</sup> ⊗ σ<sup>j</sup>
</p>

where the C<sub>ij</sub> term encodes the spin-spin correlation — the main object of interest.

<br/>

To quantify the effect of CP violation, they build a basis of spin observables:

<p align="center">
  𝒪₁ = k̂ ⋅ (s⃗₁ − s⃗₂) &nbsp;&nbsp; (CP-odd)
</p>
<p align="center">
  𝒪₂ = k̂ ⋅ (s⃗₁ &times; s⃗₂) &nbsp;&nbsp; (CP-odd)
</p>
<p align="center">
  𝒪₃ = s⃗₁ ⋅ s⃗₂ &nbsp;&nbsp; (CP-even)
</p>
<p align="center">
  𝒪₄ = (k̂ ⋅ s⃗₁)(k̂ ⋅ s⃗₂) &nbsp;&nbsp; (CP-even)
</p>

and define expectation values:

<p align="center">
  ⟨𝒪<sub>i</sub>⟩ = Tr(R 𝒪<sub>i</sub>) / Tr(R)
</p>

These are the theoretical quantities they aim to measure.


---

In practice, they construct CP-odd observables like:

<p align="center">
  ℰ<sub>1</sub> = ⟨k̂<sub>t</sub> · p̂<sub>ℓ<sup>+</sup></sub>*⟩<sub>𝒜</sub> + ⟨k̂<sub>t</sub> · p̂<sub>ℓ<sup>-</sup></sub>*⟩<sub>𝒜̄</sub>
</p>

and

<p align="center">
  ℰ<sub>2</sub> = ⟨k̂<sub>t</sub> · (p̂<sub>ℓ<sup>+</sup></sub>* × p̂<sub>𝑏̄</sub>*)⟩<sub>𝒜</sub> − ⟨k̂<sub>t</sub> · (p̂<sub>ℓ<sup>-</sup></sub>* × p̂<sub>b</sub>*)⟩<sub>𝒜̄</sub>
</p>

These are <b>averages over events</b>, and that’s the key point — spin correlations aren’t extracted from a single decay but from statistical asymmetries over many events. ℰ<sub>2</sub>, in particular, is sensitive to spin-spin interference and is strongly CP-odd.

---

### Adaptation to $$H \to b\bar{b}$$

Because b-quarks hadronise, we can’t use spinors directly — but we can still probe spin-sensitive structure if we trace:
- Higgs → b, $$\bar{b}$$
- Follow both decay branches forward to the last B-hadron before decay.
- Use the 3-momenta of the resulting B-hadrons and their decay products as spin analysers.

This procedure is entirely at truth level and gives us a well-defined way to verify whether spin correlations survive in our event generator output. The relevant Rivet analyses developed for this study are `LAMBDAB` and `HIGGS2BB`, located in the designated analysis folder. The `LAMBDAB` analysis serves as a minimal check, scanning each event for the presence of both a $\Lambda_b$ baryon and an anti-$\Lambda_b$ baryon, thus probing baryon–antibaryon correlations at truth level. In contrast, the `HIGGS2BB` analysis provides a full truth-level reconstruction of the $H \to b\bar{b}$ decay, identifying the final B-hadron descendants, categorizing events based on hadronic and semileptonic decay modes, and recording detailed kinematic information necessary for spin correlation studies. Together, these analyses form the basis for validating the event structure and exploring CP-sensitive observables.

![image](https://github.com/user-attachments/assets/a93604af-150a-4260-aaff-9d1226ea7fef)![image](https://github.com/user-attachments/assets/a8b6759e-4578-4178-a239-126d4b7fd4aa)
![image](https://github.com/user-attachments/assets/21dbe7e6-b539-440d-b98d-85f6a606273d)![image](https://github.com/user-attachments/assets/1e1273f7-192c-4a95-8f32-8b43044068c3)


### Outstanding Issues

- **Spin correlations may not be enabled.**  
  Based on our truth-level observables, we do not see evidence of spin structure being preserved in the decay. Need to verify if Herwig is including spin correlations by default. Request: check with Mike whether there is any verbose Herwig output or flag that confirms spin density matrices are being calculated.

- **Christoph’s UFO model may be misconfigured.**  
  Approximately 17% of events show bottom-loop contributions, which should not be allowed by the model. This may be a limitation of the UFO → Herwig translation (e.g., via UFO2Herwig). Needs further inspection.

To investigate the presence of unexpected Higgs decay modes and classify the decay topologies at truth level, we developed three dedicated Rivet analyses: HIGGS_DECAY_HISTO, which records two-body decay frequencies; HIGGS_3PLUS, which catalogs decays involving three or more final-state particles; and HIGGS_DECAY_ALL, which provides a complete inventory of all Higgs decays with two or more daughters.

---

### Final Note

We now have a working Rivet setup capable of tracing the full event structure and performing spin-sensitive truth-level observables. However, the physical validity of the results, especially regarding spin correlations and model consistency, remains uncertain and requires further checks.

------------------------------
# Week 6 (3.03 - 9.03)

#### Attempt at SHERPA

[🔗 Sherpa 2.2.2 Manual](https://sherpa.hepforge.org/doc/SHERPA-MC-2.2.2.html)

Investigating Sherpa as an alternative to Herwig, because Herwig steering turned out to be painful and Sherpa has way better documentation.

---

### Hadronization and Spin Correlations

#### HADRONS++

- Module responsible for simulating hadron and tau-lepton decays.
- Full spin correlations can be included if desired.
- Several matrix elements and form-factor models implemented (e.g., Kühn-Santamaría model, Resonance Chiral Theory, heavy quark effective theory).

#### Spin correlations (hard process)

- **HARD_SPIN_CORRELATIONS** is **enabled by default**.
- To disable: set `HARD_SPIN_CORRELATIONS=0`.

#### Hadron Decays

- Handled by HADRONS++ by default.
- Controlled via `DECAYMODEL = Hadrons` (default) or can be turned off (`DECAYMODEL = Off`).
- Massive decay tables (~2500 channels).
- Dynamical mass smearing and matrix-element modeling for realistic decays.

**Relevant options:**

- `SOFT_MASS_SMEARING = [0,1,2]`  
- `MAX_PROPER_LIFETIME = [mm]`  
- `DECAYPATH` sets where decay tables are read from.

---

### Further Spin Correlations

> [!NOTE]
> Spin correlations can be turned on with `SOFT_SPIN_CORRELATIONS=1` in the `(run)` section.  
>  
> For spin correlations in **tau leptons produced in the hard scattering**, also set `HARD_SPIN_CORRELATIONS=1`.  
>  
> If using AMEGIC++ as matrix element generator, recompile libraries if spin settings are changed.

---

### Observations from Sherpa Documentation

- **Spin correlations between hard scattering and decays are ON by default**.
- Hadrons++ module provides a very complete decay modeling, similar to Tauola and EvtGen.
- Sherpa allows fairly fine-grained steering without having to hack the codebase.

---

### Context Check: Event Generators

Reading about the general state of event generators made something clear:

- **Herwig is currently the only major generator that implements spin correlations inside the parton shower.**
- Other generators like Sherpa and Pythia typically implement spin correlations for hard scattering and decays, but not inside the parton shower.

(Reference: *The State of Current MC Generators*)

---

## References

- [ISAJET 7.91: A Monte Carlo Event Generator for pp, p¯p, and e⁺e⁻ Reactions](https://www.nhn.ou.edu/~isajet/isajet791.pdf)
- [Scholar search: Status of High Energy Physics Event Generators (2024+)](https://scholar.google.co.uk/scholar?as_ylo=2024&q=status+of+high+energy+physics+event+generators&hl=en&as_sdt=0,5)
- [Status of C++ Event Generators (indico)](https://indico.cern.ch/event/411610/contributions/985714/attachments/838223/1164753/summaryMC.pdf)
- [Event Generators for High-Energy Physics Experiments (SciPostPhys 16.5.130)](https://www.scipost.org/SciPostPhys.16.5.130/pdf)
- [Event Generators for High-Energy Physics Experiments (UZH/Fermilab)](https://www.zora.uzh.ch/id/eprint/229175/1/fermilab_pub_22_116_scd_t.pdf)
- [General-Purpose Event Generators for LHC Physics (arXiv 1101.2599)](https://arxiv.org/pdf/1101.2599)
- [PEPPER: A Portable Parton-Level Event Generator](https://indico.cern.ch/event/1330797/papers/5791236/files/13277-Enrico-Bothmann-Pepper-Portable-Event-Generation.pdf)

---

![image](https://github.com/user-attachments/assets/55db4483-acd8-47d0-a2ef-3d3a46a29b91)


08.03.2025

By the end of this week, we encountered persistent difficulties in reconciling the branching ratios obtained from our generated events with the expected Standard Model values. In principle, since we do not explicitly force Higgs decays in the input file, the branching ratios should naturally reproduce the Standard Model predictions. The observed discrepancies raise concerns about the underlying model implementation, particularly Christoph’s customized UFO model, which was built on top of the Standard Model (SM) UFO provided with MadGraph. To diagnose the issue, we initiated a systematic comparison between different models, including the default SM model and the HEFT (Higgs Effective Field Theory) model.

Using the UFO2HERWIG translation, we generate events and subsequently inspect the event structure at the particle level, making extensive use of the HIGGS_DECAY_ALL Rivet analysis to map all decay modes observed. This procedure allows us to check whether the deviations arise already at the UFO level or later during the event generation or showering steps. Further verification is ongoing, focusing particularly on distinguishing whether the branching ratio shifts originate from the modifications introduced in Christoph’s model or from subtleties in how Herwig treats different models internally.

The current focus is on devising a sure-fire test for the activation of spin correlations. With several papers in mind:

- Berheuter:
- Uzan:
- Richardson & Webster:

--------------------------------
# Week 7 (10.03 - 16.03)

Bernheuter paper is useful but we cannot guarantee the valdity of our check. Uzan is almost impossible to implement due to low stats



## Deconstructing the Richardson and closely related PanScales paper: Spin Correlations 

### 1. Richardson & Webster, _“Spin Correlations in Parton Shower Simulations”_  
*(Eur. Phys. J. C 80 (2020) 83, arXiv:1807.01955)*

| Aspect | Author’s construction |
|--------|------------------------|
| **Elementary geometry** | Every splitting _i → jk_ defines a plane **P** spanned by the three-momenta of the daughters. The azimuth of that plane, φ, is measured in the rest frame in which the emitter is chosen to lie on the _z_ axis. |
| **Core variable** | For two successive branchings 0 → 12 followed by 2 → 34 they study:<br>  **Δφ ≡ φ₂ − φ₁** – the signed angle between the two planes. |
| **Analytic structure** | In the collinear limit:<br>  (1/2π) dσ/dΔφ = (1/2π) [1 + A(z₁) B(z₂) cos (2 Δφ)]<br>Coefficients A and B depend **only** on the light-cone momentum fractions _z₁_ and _z₂_. They tabulate A,B for all four helicity chains (q→qg then g→qq̄, etc.) – see Table 1 of the paper. |
| **Illustrative example** | _H_ → g g followed by g → qq̄ on each leg. Using the Collins–Knowles density–matrix algebra they derive:<br>  dσ/dΔφ ∝ 3 + 2 cos²Δφ (after z-integration). |
| **Measurement prescription** | Δφ is always taken **in the frame of the second splitting**, guaranteeing that the recoil does not spoil the plane definition. For dipole showers they enforce one common spectator so that both splittings share the same boost sequence. |
| **ISR analogue** | Replace final–state correlation by initial–state chains (e.g. g→qq̄ backwards splittings). The same Δφ observable is used; analytic expressions analogous to Eq. (20) are given and validated (Figs. 5–8). |
| **Decay observables** | For top decays they propagate the hard-process density matrix into the W→ℓν decay and study the charged–lepton azimuthal separation; the same plane formalism applies. |

---

### 2. Karlberg _et al._, _“Spin correlations in final-state parton showers and jet observables”_  
*(arXiv:2103.16526)*

| Aspect | Author’s construction |
|--------|------------------------|
| **Azimuth in a shower tree** | In the PanScales implementation each branching node holds a normalised cross-product **n̂** of daughter momenta. The azimuth of node _i_ is built recursively:<br>  ψ₀ = 0;<br>  ψᵢ = ψᵢ₋₁ + Δψ(i−1,i), where Δψ(i−1,i) is the signed angle between successive **n̂**’s. |
| **Lund-declustered observables** | Embedded in a **Cambridge/Aachen Lund diagram**:<br>• _Primary_ splitting = hardest-kₜ declustering on the **primary** Lund plane with _z > z_cut_;<br>• _Secondary_ = hardest-kₜ on the **secondary** Lund plane of that primary, again with _z > z_cut_. |
| **Core variables** | • **Δψ₁₂** = ψ(secondary) − ψ(primary) (intra-jet).<br>• **Δψ₁1′** = difference between the two primary splittings in opposite hemispheres (e.g. H → g g). |
| **Fixed-order template** | In the strict collinear limit:<br>  dσ/dΔψ = a₀ [1 + A(z₁) B(z₂) cos (2 Δψ)] (Eq. 11)<br>They list analytic A,B for every flavour channel (Table 2). |
| **Three-point EEEC** | As a complementary _z_-independent probe they adopt the **spin-sensitive 3-point energy–energy correlator**:<br>  (1/σ) d³Σ/dΔψ dθ_S dθ_L (Eq. 12)<br>Here Δψ is the angle between the _(ij)–k_ and _i–j_ planes, θ_S the soft opening, θ_L the larger opening. |
| **Infra-red safety & cuts** | • _z_cut_ (usually 0.1) ensures IR safety of the Lund observable at all orders.<br>• They exploit freedom in z₁,z₂ cuts to **magnify** the modulation (cf. Table 3).<br>EEEC needs no _z_cut_ but its energy weighting suppresses extreme-z regions. |
| **All-order validation** | The analytic cos(2Δψ) template survives single-log resummation; toy-shower and PanScales results agree to NLL accuracy (Figs. 17–18). |
| **Design philosophy** | • Observable must be computable in fixed-order **and** resummed frameworks.<br>• Must separate flavour channels to avoid g→gg / g→qq̄ cancellations. |

----------


## Detailed Summary of Spin Correlations in Herwig and PanScales

This week we focused on understanding in full detail the theoretical and algorithmic construction of spin correlations as implemented in the Herwig (Richardson) and PanScales frameworks.

In the Richardson paper (Herwig shower with spin correlations), the central idea is that spin effects are captured by assigning a spin density matrix to each particle at the moment of production or branching. Specifically, when a gluon is produced, for example from a hard process such as \( H \to gg \), it is assigned a spin density matrix \( \rho \) determined by the helicity amplitudes of the production process:

<div align="center">
\[
\rho_{\lambda_g \lambda'_g} = \frac{1}{N} \sum_{\text{other helicities}} M_{\lambda_g} M^*_{\lambda'_g}
\]
</div>

where \( M_{\lambda_g} \) is the helicity amplitude for the gluon with helicity \( \lambda_g \), and \( N \) is a normalization factor ensuring \( \text{Tr}(\rho) = 1 \).

When the gluon subsequently branches, for instance via \( g \to q\bar{q} \), the azimuthal angle \( \phi \) of the branching is not chosen randomly, but according to a distribution proportional to:

<div align="center">
\[
\rho_{\lambda_g \lambda'_g} M_{\lambda_g \lambda_q \lambda_{\bar{q}}} M^*_{\lambda'_g \lambda_q \lambda_{\bar{q}}}
\]
</div>

where \( M_{\lambda_g \lambda_q \lambda_{\bar{q}}} \) are the helicity amplitudes for the branching.  
This construction ensures that the azimuthal distribution between the daughter partons encodes the spin information of the parent particle.

After the branching, new spin density matrices are assigned to the daughters, carrying forward spin information into subsequent emissions. Thus, spin information is propagated through the entire shower evolution.

Observables sensitive to these correlations are typically built from the relative azimuthal angles between the planes defined by two successive branchings.  
For example, for two correlated emissions, the distribution of the azimuthal angle difference \( \Delta\phi \) between the planes satisfies:

<div align="center">
\[
\frac{d\sigma}{d\Delta\phi} \propto 1 + A \cos(2\Delta\phi)
\]
</div>

where the modulation amplitude \( A \) quantifies the strength of the spin correlation.  
A positive \( A \) corresponds to correlated emissions favoring aligned spin planes, while a negative \( A \) indicates anticorrelations.

---

The PanScales paper develops a similar but more general formalism, applicable to dipole and antenna showers beyond the angular-ordered case.  
They formulate the emission probability from a parent parton (say parton 0 splitting into partons 1 and 2) in terms of a spin-correlated matrix element:

<div align="center">
\[
|M_{0\to12}|^2 = \sum_{\lambda_0, \lambda_1, \lambda_2} M_{\lambda_0 \lambda_1 \lambda_2} M^*_{\lambda_0 \lambda_1 \lambda_2}
\]
</div>

where \( \lambda_i \) denote the helicities.  
At each branching, a spin density matrix is assigned, and the azimuthal angle of the emission is sampled according to the interference between different helicity amplitudes, ensuring spin correlations are preserved.

Importantly, PanScales carefully treats the correlation between different splittings by defining an evolution tree, where at each node a Collins–Knowles step is applied.  
The evolution is thus a sequence of emissions, each carrying spin information inherited from the parent, and influencing the distribution of the child emissions.

They show that in a fixed-order calculation at \( \mathcal{O}(\alpha_s^2) \), spin correlations between two emissions manifest as modulations in the azimuthal angle difference \( \Delta\psi \) between the two splitting planes:

<div align="center">
\[
\frac{d\sigma}{d\Delta\psi} \propto 1 + A(z_1)B(z_2) \cos(2\Delta\psi)
\]
</div>

where \( z_1 \) and \( z_2 \) are the energy fractions carried by the emissions, and \( A(z) \), \( B(z) \) are functions encoding how the energy distribution affects the strength of the spin correlation.

In Figure 6 of the PanScales paper, they plot the ratio \( a_2/a_0 \) as a function of \( z_1 \) and \( z_2 \), where \( a_2 \) corresponds to the coefficient of the \( \cos(2\Delta\psi) \) term, and \( a_0 \) is the overall normalization.  
The ratio is maximal when both \( z_1 \) and \( z_2 \) are near 0.5, corresponding to symmetric splittings, and vanishes when either energy fraction becomes close to 0 or 1.

- If both gluons split into quark-antiquark pairs: correlation is **positive and strongest**.
- If one gluon splits into a quark-antiquark pair and the other into gluons: **negative correlation**.
- If both gluons split into gluons: **very small correlation**.

---

PanScales also places this discussion in the context of **Lund planes**.  
In their setup, a Lund plane parametrization organizes emissions according to transverse momentum and energy fraction.  
Each point on the Lund plane corresponds to an emission characterized by:

<div align="center">
\[
\log\left(\frac{1}{\theta}\right), \quad \log(z\theta)
\]
</div>

where \( \theta \) is the angle between the emitting and emitted parton, and \( z \) is the energy fraction.  
Spin correlations manifest as modulations across the Lund plane, particularly visible when emissions are symmetric in energy sharing and at moderate angles.

---

Thus, both in Richardson and PanScales, spin correlations are not simply an "on/off" effect but are modulated depending on the **kinematics of the splittings**.  
The maximal sensitivity is in configurations where splittings are symmetric in energy sharing, and suppressed in strongly asymmetric emissions.

---

In our case, applying these methods to \(H \to gg\) or \(H \to b\bar{b}\), we must carefully account for the energy fractions of the subsequent splittings and their angular distributions, as spin correlations will be strongest only in specific regions of phase space.

To consolidate the method, I’ve sketched the full variable construction as implemented in Richardson’s algorithm. See illustration below.
![Drawing 2025-03-12 11 14 512 excalidraw (1)](https://github.com/user-attachments/assets/c08aa6e2-de0c-4aeb-9c71-19cdd30f3260)

Towards the end of Week 7, Karim implemented a Python-based analysis, located in `Python Scripts/global_analysis.py`. This script performs a specialized truth-level study of Higgs decays. At a high level, it:

- Loads a Parquet file containing simulated Higgs decay events, with each event consisting of 14 final-state daughter particles and associated event weights.
- Extracts four-momentum components (E, px, py, pz) for each particle using the `vector` library.
- Constructs "interjet" and "intrajet" observables, which are angular variables characterizing separations between subclusters within an event. Two different approaches are used: the "Richardson formalism" and the "Panscales No-Nonsense" formalism.
- Applies channel selection cuts based on PDG ID information (e.g., distinguishing between Higgs decays into gg → qq̄qq̄ versus bb → qgqg topologies).
- Weights, bins, and histograms the computed angular observables (Δφ or Δψ), with proper treatment of statistical uncertainties.
- Loops through the file in row-group "chunks," accumulating histograms per decay channel.
- At the end of the analysis, normalized differential cross-section plots are produced for each decay channel, z-cut, and boost configuration.

Initial results confirm that the **intrajet** observables are sensitive to spin correlations, as expected. This indicates that spin correlations are correctly preserved within the **parton shower** itself. Two figures illustrate the relevant angular structures:

- ![image](https://github.com/user-attachments/assets/c199f38d-c063-4907-b269-79c9763619b6)  
  *Angle between a bg plane where the gluon subsequently decays into two quarks.*

- ![image](https://github.com/user-attachments/assets/cdb49e9b-8eaa-4ace-a4f1-117e494890a6)  
  *Plane formed between two gluons, with one gluon decaying to two quarks.*

However, an important limitation emerges: the **interjet** observable, which probes correlations between the two primary branches linking the hard process to the shower (i.e., between the two b quarks originating from H → bb), yields a **flat distribution** for the H → bb channel. No significant angular correlations are observed.

Upon further inspection of the parton structure using Rivet, it became clear that our initial assumptions about the decay topology were oversimplified. Specifically, we had assumed that the Higgs always decays into two "parent" b-quarks, each of which subsequently splits into a b and a gluon ("children"), followed by further splitting into two "grandchildren." In practice, however, several issues arise:

- In many events, the parent b-quarks do not split further at all.
- Even when splitting occurs, the number of final-state partons is often smaller than expected.
- Disabling hadronization, which we did to reduce event file sizes and generation time, exacerbates these issues. Without hadronization, some partons begin to hadronize before full parton showers develop, leaving incomplete decay chains.

Given these problems, it became evident that the lack of final-state structure was intrinsic to the simulation setup. In response, we planned for Week 8 to go "back to basics" by conducting a very rudimentary test using a clean H → gg process in a standard input file (see "Rudimentary input file" reference). The plan was to generate two samples—one with spin correlations activated and one with spin correlations turned off—allowing us to directly probe the behavior of the interjet variable. 

Although the final state particle multiplicity remains low even in this simplified setup, the situation is manageable because our primary interest lies in the **interjet variable**, where sufficient statistics can still be extracted.


Input 
### References

- P. Richardson, *Spin correlations in Monte Carlo simulations*, [arXiv:1807.01955](https://arxiv.org/abs/1807.01955)
- PanScales Collaboration, *Towards parton shower precision*, [arXiv:2103.16526](https://arxiv.org/abs/2103.16526)

-------------------------------
# Week 8 (17.03 - 23.03)

The figure below illustrates the issue encountered during this week's work: a visualisation of the event record reveals unexpectedly limited parton showering structure, particularly in Higgs decays to gluon or b-quark pairs.
![image](https://github.com/user-attachments/assets/0f40c0b1-295b-4531-a649-1adb268425b9)

We contacted Mike Seymour to investigate this behaviour further:

> **Email – Karim to Mike**  
>  
> We are simulating Higgs boson production via gluon-gluon fusion with the Higgs decaying to either \( b\bar{b} \) or \( gg \). For both channels, we observe very few parton-level branchings — typically only 2–4 in total. This is despite using the Angular-Ordered (AO) shower in Herwig. Hadronisation is disabled to save resources, as we aim to study jet substructure via Lund plane declustering and require the shower to develop properly. Input files and a representative event visualisation were included for reference.

Mike’s reply was cautiously optimistic:

> **Reply – Mike Seymour**  
>  
> That is indeed surprising. For \( H \to gg \), I would expect on average around 10–15 gluons to be emitted during showering, based on an MLLA estimate with the default infrared cutoff at \( p_T = 0.655 \, \text{GeV} \). If your distributions significantly undershoot this, it may indicate a problem with the shower setup.


Link: [https://phab.hepforge.org/source/herwighg/browse/default/src/defaults/Shower.in](https://phab.hepforge.org/source/herwighg/browse/default/src/defaults/Shower.in "https://phab.hepforge.org/source/herwighg/browse/default/src/defaults/Shower.in") line 129

We subsequently produced the following distribution of gluons per event:

![image](https://github.com/user-attachments/assets/873bedb8-ed8c-4c1b-b2f0-1309b37fbfaa)



With the peak around 10–11 gluons, the shower appears to be functioning nominally. As such, we conclude that this “incomplete shower” behaviour is expected for \( H \to b\bar{b} \), especially without hadronisation — and must be worked around rather than “fixed.”

Using these samples, we confirm that **interjet spin correlations** do appear in \( H \to gg \). However, we are confronted with a significant theoretical caveat, clearly noted in the PanScales paper ([arXiv:2103.16526](https://arxiv.org/abs/2103.16526)):

> *That particular case, with a \( q\bar{q} \) hard process, would have zero correlation, but the correlation is non-zero for a \( gg \) hard process.*

This explains why **no azimuthal structure** is observed between the two b-branches in \( H \to b\bar{b} \) — a key disappointment, but also an important finding.

To clarify the issue for ourselves, we framed the following question:

---

#### On the Absence of Spin Correlations in \( H \to b\bar{b} \) after Showering

I'm studying the CP structure of \( H \to b\bar{b} \) using Herwig at generator level. With showering on (but hadronisation off), spin correlations between the b and \( \bar{b} \) branches appear completely washed out, even when tracing all the way to the final B-hadrons.

At first, this was puzzling — because in \( H \to gg \), spin correlations are clearly visible, e.g., in the azimuthal angle between splitting planes. This is understood to result from gluon polarisation being retained through the shower (see [arXiv:1807.01955](https://arxiv.org/abs/1807.01955) and PanScales [arXiv:2103.16526](https://arxiv.org/abs/2103.16526)).

But PanScales explicitly footnotes that for \( q\bar{q} \) final states, **no inter-branch spin correlation** is expected. This makes sense: gluons carry polarisation states, but spin information in quark lines seems less resilient, and the collinear approximation fails to capture it.

Still, this raises the question:  
**Could spin correlations in \( H \to b\bar{b} \) be recovered in any setup?**  
Could going beyond collinear approximations — or considering \( H \to b\bar{b}g \) explicitly — restore this structure? Do current showers (e.g., Collins–Knowles implementation in Herwig) encode any spin entanglement between fermion branches at all?

If such correlations are fundamentally lost in quark final states at shower level, then attempts to probe CP-odd angular asymmetries in \( H \to b\bar{b} \) at generator level must account for this loss carefully.

---

This week marks a conceptual turning point: **we have to change what we expect to be visible in our data**, and realign our analysis strategy accordingly.


-------------------------------

# Week 9 (24.03 – 30.03)

### GN2 Pipeline: Planning and Implementation

On March 24, Andy sent the following email summarizing our next steps for deploying the GN2 graph network architecture on Rivet output:

> Hi both,  
>
> I spoke to Valentina (in cc) today about the final steps for the project. She convinced me that GN2 is going to be implementable.  
>
> To use GN2 you need a `.h5` file. It seems at first sight that we can produce this directly from a `.csv` file. This would mean outputting the information needed to a `.csv` from Rivet.  
>
> (1) First test: write a `.csv` for the decay chain you have been analysing, i.e. H → b b̄, with b → g b and g → q q̄ (same for the b̄ decay). This means 6 particles in the final state and each particle has 5 pieces of information: E, px, py, pz, ID. Hence a `.csv` with 30 columns.  
>
> (2) At this point you write the Python code to convert the `.csv` to `.h5`.  
>
> (3) Then use GN2. Valentina will send tutorial and publicly available code.  
>
> (4) After this first test, you can extend the `.csv` to include more branchings. We can discuss this at the point you get to (2).  
>
> Cheers,  
> Andy

In fact, we had already implemented all the steps outlined above — we are currently beyond step 4. Even though the interjet observable has not provided any significant structure in the H → b b̄ case, Andy recommended we look at the joint distribution of the two **intrajet** variables (b-branch vs. b̄-branch) using a 2D contour plot.

![Intrajet Correlation Contour](https://github.com/user-attachments/assets/2a7ec977-1ac8-459a-b681-77429c8771b7)

This plot revealed a need for higher statistics. The requirement that the intermediate gluon splits into two quarks — a rare occurrence — limits the number of valid events.

To explain this rarity, we refer to the explanation provided by Mrinal:



Gluon splittings of the form $$g \to q \bar{q}$$ are proportional to $$\text{Tr}(t^a t^b)$$, giving a factor of $$1/2 \cdot n_f$$, and are not enhanced in the infrared, unlike $$g \to gg$$ and $$q \to qg$$, which scale with $$C_A$$ and $$C_F$$ respectively. Consequently, gluons are far more likely to undergo $$g \to gg$$ rather than $$g \to q\bar{q}$$, especially at low transverse momenta.

---

### Re-alignment and Dataset Preparation for Gluon Splitting Study

#### 25.03.2025 — Recalibrating Goals

After reading Andy’s message, we re-evaluated our goals. I suggested that we consolidate efforts on building the GN2-ready dataset and begin with a new Rivet analysis designed to:

- Count final-state gluons and quarks.
- Trace specific decay chains:  
  H → b b̄ → b g, and subsequently g → q q̄ or g → g g.

The new insight was that both gluon decay modes (q q̄ and g g) are physically relevant and should be retained in the dataset.

#### 26.03.2025 — CSV Structuring and Filtering Logic

We streamlined the CSV schema exported from Rivet:

- Dropped the Higgs and gluon rows.
- Kept only the child b-quark (from b → g b) and all final-state products from the gluon splits.
- Ensured each row had 6 particles (30 columns).
- Added filtering logic: exclude events where either branch does not yield a full decay tree (i.e., b → b g → q q̄).

The CSV-to-HDF5 conversion was tested using Python and DuckDB, enabling efficient pre-filtering of large Rivet outputs.

We noticed that only ~44k out of 82k H → b b̄ events had the full decay structure. We hypothesized this was due to asymmetric showering.

#### 27.03.2025 — Visual Debugging of Event Topologies

To investigate, we visualized the shower histories using `graphviz` and `pyhepmc`. Matching between the Richardson routine and the Rivet-generated CSV was verified. The likely culprit for the missing decay topologies was identified as **hadronisation settings**.

- With hadronisation off: ~0.015% of events contain g → q q̄.
- With hadronisation on: ~28% of events have at least one such split.

We updated the filtering logic to exclude all-zero entries and retain only cleanly split events on both b and b̄ sides.

#### 28.03.2025 — Efficient Event Processing via Internal Rivet Hook

Karim successfully ran Rivet **inside Herwig** via direct analysis hooks, bypassing `.hepmc` file generation and I/O bottlenecks. The new workflow supports:

- Multicore parallelism.
- Direct `.csv` output from each job.
- Estimated throughput: ~100 million events in under 2 hours using 16 threads.

This dramatically improved scalability, paving the way for large-scale dataset generation suitable for GN2 training.



-------------------------------
# Week 10 (31.03 - 6.04)

### 02.04.2025 — Investigating Interjet Differences Using Intrajet Correlations

Karim modified our Python analysis pipeline (see `Python Scripts/intrajet_for_interjet.py`) to produce **2D contour plots** that compare angular observables between the two branches of the H → b b̄ decay. Specifically, the script focuses on the **Panscales “no-nonsense” observable** Δψ, computed for each branch individually, then plotted as a joint distribution.

This approach is designed to reveal **subtle correlations** between decay planes in the presence of CP violation. We had initially believed that by eye we could detect a ~2σ difference between CP-even and CP-odd cases; however, after using this statistical method, **no significant difference** appears — even with high statistics.

#### Summary of What the Script Does
- Reads cleaned `.parquet` files produced by Rivet, containing particle four-momenta and PDG IDs.
- Reconstructs **decay chains** such as b → b g and g → q q̄ or g g, separately for each b-branch.
- Computes Δψ observables for each branch using boosted or unboosted frames.
- Filters events by decay topology (e.g., bg → qq̄ on both sides).
- Produces histograms and contour plots for:
  - Weighted Δψ–Δψ distributions.
  - Asymmetry between CP-even and CP-odd samples.
  - Statistical significance of the asymmetry.


![bg_gg_asymmetry (1)](https://github.com/user-attachments/assets/221e8b96-9452-403d-a3e8-987d11652ae9)


#### Conclusion
While the tool performs as expected, it confirms a lack of measurable **interjet angular correlation** between the two sides of H → b b̄ — consistent with theoretical expectations from the PanScales papers. Those works note that spin correlations are preserved for **gluon-initiated** processes, but **not** for quark-initiated ones like H → q q̄.

This supports the idea that, in the quark decay channel, any CP-odd structure is either:
- Washed out by parton showering, or
- Fundamentally absent in the leading-log approximation used by current shower algorithms.

This result will guide our next steps in re-evaluating how CP-violating effects might manifest in the parton-level structure of H → b b̄ decays.


### Investigating Skewed Higgs Decay Ratios Using MadGraph vs Herwig

A lingering issue throughout the project has been the observation that the Higgs decay branching ratios in our Herwig-based simulations appear skewed compared to Standard Model expectations. This week, we finally addressed this systematically by contrasting how MadGraph and Herwig handle decays, particularly in the absence of hadronisation or showering.

We begin by disabling the Herwig shower and relying solely on parton-level MadGraph output. The philosophy behind MadGraph becomes immediately relevant: MadGraph is designed to compute matrix elements for hard scatterings, focusing on on-shell final-state particles. Decays must be explicitly included in the process definition. For example, if one wants the Higgs to decay into a b b̄ pair, the correct syntax is `generate g g > h > b b~`. MadGraph otherwise assumes final-state particles are stable, unless decays are defined as subprocesses. This separation is intentional: MadGraph does not mix parton-level generation with decay dynamics or hadronisation, maintaining a modular design philosophy.

In contrast, Herwig operates as a full Monte Carlo event generator, managing not only the hard scattering but also subsequent decays, parton showers, and hadronisation. Herwig's decay logic is tightly coupled to the UFO model it is given. If a model contains non-zero decay widths for a particle, Herwig will automatically decay it according to the defined branching ratios. This is not just a convenience — it's a core feature. Herwig imports decay widths via UFO2Herwig from the UFO model, where all decays and interactions are specified. Once the Higgs production process is defined, Herwig proceeds to decay the Higgs boson according to the width table, even if the user never specifies the decay in the run card or process file.

The root cause of our discrepancy clicked into place when we inspected the `decays.py` file in Christoph’s UFO model. In that file, the Higgs boson's decay to b b̄ is defined as:

```python
Decay_H = Decay(name = 'Decay_H',
                particle = P.H,
                partial_widths = {
                  (P.b,P.b__tilde__): '((-12*MB**2*yb**2 - 24*coupbeven*MB**2*yb**2 - 12*coupbeven**2*MB**2*yb**2 + 3*MH**2*yb**2 + 6*coupbeven*MH**2*yb**2 + 3*coupbeven**2*MH**2*yb**2 + 3*coupbodd**2*MH**2*yb**2)*cmath.sqrt(-4*MB**2*MH**2 + MH**4))/(16.*cmath.pi*abs(MH)**3)',
                  ...
                })
```

This clearly shows that the partial width is not the Standard Model one but rather depends explicitly on the CP-even and CP-odd couplings coupbeven and coupbodd. Herwig, in turn, uses this formula directly to compute the decay probabilities. That explains the branching ratio skewness we've observed: the UFO model itself modifies the decay widths.

To cross-check, we referred to the PDG’s standard decay width formulas for the Higgs boson, which can be found at [Cross-Section Formulae — PDG 2019](https://pdg.lbl.gov/2019/reviews/rpp2018-rev-cross-section-formulae.pdf). Comparing those to Christoph’s expressions confirms that the model modifies the b b̄ width in a non-trivial way depending on the couplings.

In conclusion, Herwig applies automatic decays using whatever is defined in the UFO’s decay structure, while MadGraph requires explicit instructions and does not alter decay widths unless configured to. The discrepancy in branching ratios is therefore not a bug but a consequence of how the UFO model was constructed and interpreted by Herwig.

-------------------------------
# Week 11 (7.04 - 13.04)

#### 07.04.2025 — Scaled-Up Production & DAGMan Job Management

We were given access to the whole **8 bulks of 96 cores each** on the Noether cluster. This allowed us to parallelise large-scale event generation for our `pp → H → gg` process.

To avoid cluster congestion and job losses due to time limits, we used **HTCondor’s DAGMan** system to control the submission of batches. Each DAG node manages a group of **30 subjobs**, corresponding to `(nstart, nstop)` ranges with `--sample` either `odd` or `even`.

Each subjob runs a command of the form:
`python3 manager_jobs_modified_96.py --nstart 0 --nstop 24 --sample even`

#### 09.04.2025 

Persistent Monitoring (Experimental Idea):

Tested a remote control method to monitor or trigger runs from outside Noether:
1. Created a **GitHub Gist** with an executable bash snippet.
2. Launched a **`tmux` session** on Noether containing:

`while true; do   curl -s https://gist.githubusercontent.com/ana-gist-id/raw/script.sh | bash   sleep 60 done`

This allowed for live script updates without re-login. **NOTE:** This approach was later abandoned due to security concerns, as flagged by Andy and others.

#### 13.04.2025
All JOBS done and uploaded on drive (3B events for each sample - odd/even   pi/4, -pi/4).

# Week 12 (14.04 - 20.04)

Ana and I think the panscales observable is sensitive to the CP-structure of the effective Hgg coupling. I’m attaching plots of the normalised differential cross section distribution of the observable of CP mixing angles:  0, pi/2, pi/4 and -pi/4 in the lab frame.

EVEN
![image](https://github.com/user-attachments/assets/fecb12f1-2999-4b48-a333-7bf18092ac1b)

ODD
![image](https://github.com/user-attachments/assets/e24a5898-eb31-44c6-9102-88430ae21879)

PI/4
![image](https://github.com/user-attachments/assets/70ed5c85-3e8e-4bc9-ac34-af2700cdfea1)

-PI/4
![image](https://github.com/user-attachments/assets/aad17700-9720-4ae6-8d60-4eb89420e7b2)

In case we don’t meet today (likely), the immediate thing that I notice is (i) the even vs odd is very different with peaks/troughs shifted by pi/2, (ii) the mixed looks like the pure-even contribution with suppressed peaks. 

For the mixed case, I was expecting a phase shift to the distribution so that it peaked half way between odd and even. I wonder whether there is some lack of directionality in the DeltaPsi definition (i.e. equivalent to a modulus) that then partially maps the peaks onto troughs in the mixed case…..this is the first thing to look at.

Spoke to Christoph, he agrees it is interesting. There would be a lot of work to do to flesh this out after MPhys if we wanted to carry on and we have to decide whether this is worth it for you. Ultimately there is clearly an effect, but we would (i) have to understand it more and (ii) build in some realism in terms of not being able to trace the shower in real life.

We bounced around a few ideas for your Mphys
(1) Look at this paper: https://arxiv.org/pdf/1010.0676
Measuring spin and CP from semihadronic ZZ decays using jet substructure - arXiv.org
zz zz + cp + + + = ...
arxiv.org
 and look at the variable defined in (1e). This projects out the correlations for Higgs decaying to two spin one particles. You’ll have to play with the definitions of alpha, beta and plus, minus, to get it to work, but gives you another variable
(2) The above variables are defined with some rapidity ordering: it is worth you playing around with the ordering in your splitting plane definitions  to see if it makes a difference.
(3) Similarly, you could try n_i dot n_(i-1) (n is the normal to the planes) for different orderings to see if something interesting happens.
(4) If/when all fails: you have the NN…..


# References

## Spin Correlations and Parton Showers

- [Spin Correlations — Herwig Manual](https://herwig.hepforge.org/tutorials/hardprocess/matchbox.html#spin-correlations)
- [Spin Correlations in Parton Shower Simulations — Richardson & Webster](https://arxiv.org/pdf/1807.01955)
- [Soft Spin Correlations in Final-State Parton Showers](https://arxiv.org/pdf/2111.01161)
- [Spin Correlations in Final-State Parton Showers and Jet Observables — PanScales](https://arxiv.org/pdf/2103.16526)
- [New Formalism for QCD Parton Showers](https://arxiv.org/pdf/hep-ph/0310083)
- [Improved Monte Carlo Simulations of Massive Quarks](https://etheses.dur.ac.uk/12954/2/thesis.pdf?DDD25+)

## Event Generators and Matrix Elements

- [Matrix Element Providers — Herwig Tutorial](https://herwig.hepforge.org/tutorials/gettingstarted/extmatrix.html)
- [UFO to Herwig Conversion](https://herwig.hepforge.org/tutorials/bsm/ufo.html)
- [ISAJET 7.91 — Monte Carlo Event Generator Manual](https://www.nhn.ou.edu/~isajet/isajet791.pdf)
- [General-Purpose Event Generators for LHC Physics](https://arxiv.org/pdf/1101.2599)
- [Status of C++ Event Generators](https://indico.cern.ch/event/411610/contributions/985714/attachments/838223/1164753/summaryMC.pdf)
- [SciPost Review — Event Generators for High-Energy Physics](https://www.scipost.org/SciPostPhys.16.5.130/pdf)
- [Event Generators for HEP Experiments (Fermilab PUB)](https://www.zora.uzh.ch/id/eprint/229175/1/fermilab_pub_22_116_scd_t.pdf)
- [PEPPER: A Portable Parton-Level Event Generator](https://indico.cern.ch/event/1330797/papers/5791236/files/13277-Enrico-Bothmann-Pepper-Portable-Event-Generation.pdf)
- [Sherpa Manual](https://sherpa-team.gitlab.io/sherpa/master/sherpamanual.pdf)
- [Beyond Standard Model Calculations with Sherpa](https://s3.cern.ch/inspire-prod-files-b/b086f56388637757bf0102afad4cb74b)
- [Herwig Release Note](https://arxiv.org/pdf/1512.01178)
- [History of Herwig](https://www.hep.phy.cam.ac.uk/theory/webber/HerwigHistory.pdf)

## Rivet, LHAPDF, and HEPMC

- [Rivet User Manual](https://arxiv.org/pdf/1003.0694)
- [Potential Rivet Analysis — MC_VH2BB](https://rivet.hepforge.org/analyses/MC_VH2BB.html)
- [Prompt vs Non-Prompt Particles (Rivet Tutorial)](https://indico.cern.ch/event/1131739/contributions/4749497/attachments/2395141/4101021/rivet-tutorial%20(1).pdf)
- [PyHepmc Interface Documentation](https://pyfeyn2.readthedocs.io/en/stable/interfaces/hepmc/hepmc.html)
- [LHAPDF IDs](https://lhapdf.hepforge.org/pdfsets.html)
- [HEPMC Particle IDs](https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf)

## CP Violation and Higgs Sector Studies

- [CP Violation and Higgs — ATLAS 2024 Slide](https://cds.cern.ch/record/2904951/files/ATL-PHYS-SLIDE-2024-250.pdf)
- [Studies of Higgs Boson CP Properties](https://cds.cern.ch/record/2841144/files/ATL-PHYS-SLIDE-2022-596.pdf)
- [Looking for CP Violation in the Higgs Sector — Warwick Seminar](https://warwick.ac.uk/fac/sci/physics/research/epp/events/seminars/WarwickSeminar_HiggsCP_KB_040620.pdf)
- [Nonlinear Top-Higgs CP Violation](https://arxiv.org/pdf/2308.11722)
- [Approaching Robust EFT Limits for Higgs CP Violation](https://arxiv.org/pdf/1901.05982)
- [Machine-Enhanced CP-Asymmetries in the Electroweak Sector](https://journals.aps.org/prd/pdf/10.1103/PhysRevD.107.016008)
- [Machine-Enhanced CP-Asymmetries in the Higgs Sector](https://www.sciencedirect.com/science/article/pii/S037026932200380X?ref=pdf_download&fr=RR-2&rr=8f0c1769392aef3e)
- [Andy’s Paper on Machine-Enhanced CP Asymmetries](https://arxiv.org/pdf/2112.05052)

### Specific Papers on H → bb and ττ

- [Bernreuther Paper on CP-sensitive Observables (H→tt, H→ττ)](https://arxiv.org/pdf/hep-ph/9701347)
- [Bernreuther Paper — Higgs CP-mixing in τ Decay](https://arxiv.org/pdf/1410.6362)
- [Bernreuther — Determining Higgs CP Parity in τ Channels](https://arxiv.org/pdf/0801.2297)
- [ATLAS Measurement of Higgs CP Properties with τ-leptons](https://arxiv.org/pdf/2212.05833)
- [Spin Correlations and Top Mass Trick — Higgs→bb](https://arxiv.org/pdf/2311.08226)

- [H → bb with Λ Mapping](https://link.springer.com/article/10.1007/JHEP08(2021)167)

## Jet Algorithms and Polarization

- [Anti-\(k_T\) Jet Algorithm — Cacciari et al.](https://indico.cern.ch/event/1112883/contributions/4677589/attachments/2395256/4095349/Matteo_Cacciari_2008_J._High_Energy_Phys._2008_063.pdf)
- [Polarization in B Decays](https://pdg.lbl.gov/2019/reviews/rpp2019-rev-b-decays-polarization.pdf)
- [Helicity Suppression Explanation](https://physics.stackexchange.com/questions/704458/confused-about-helicity-suppression-in-the-decay-pi-rightarrow-mu-overl#:~:text=,convert%20one%20into%20the%20other)

## SMEFT, FeynRules, and EFT Tools

- [SMEFTsim 3.0 Guide](https://arxiv.org/pdf/2012.11343)
- [Hands-on SMEFTsim — Ilaria Brivio](https://arxiv.org/pdf/2012.11343)
- [FeynRules 2.0 Toolbox](https://arxiv.org/pdf/1310.1921)

## Additional References

- [Observation of CP Symmetry Breaking in Baryon Decays](https://arxiv.org/pdf/2503.16954)
- [DETECTING HIGGS BOSON DECAYS TO NEUTRALINOS](https://arxiv.org/pdf/hep-ph/9402265)
- [Two-Component Spinor Techniques](https://arxiv.org/pdf/0812.1594)
- [Mapping Kinematical Regimes in SIDIS](https://arxiv.org/pdf/1904.12882)

## Machine Learning in HEP

- [AnalysisG GitHub Project](https://github.com/woywoy123/AnalysisG)
- [Harvard Data Science Review: Machine Learning in HEP](https://hdsr.mitpress.mit.edu/pub/xqle7lat/release/5)
- [IML Working Group — Living Review](https://iml-wg.github.io/HEPML-LivingReview/)
- [Physics Projects Using Data Science (Reddit Discussion)](https://www.reddit.com/r/ParticlePhysics/comments/13uwfoj/what_are_some_physics_projects_using_data_science/)

## Condor and Cluster Job Submission

- [HTCondor Submit Manual](https://htcondor.readthedocs.io/en/latest/man-pages/condor_submit.html)

---
### Key Classical References (Operators and CP Observables)

- Collins & Knowles, *Nucl. Phys.* B304 (1988) 794: **Coherent Spin Evolution Algorithm**.
- Richardson & Webster, *Spin Correlations in Parton Showers*, [arXiv:1807.01955](https://arxiv.org/pdf/1807.01955).
- ATLAS Collaboration, *CP-sensitive Observables for Higgs–Fermion Interactions*, [arXiv:2406.03950](https://arxiv.org/abs/2406.03950).

---

_Work in progress references:_
- Higgs→ττ paper analysis.
- Andy’s own papers on machine-enhanced asymmetries.
- Lund plane spin-sensitive decomposition [PanScales Project](https://gsalam.web.cern.ch/panscales/).
- Tau polarimeters for \( e^+e^- \to \tau^+\tau^- \) setups.


