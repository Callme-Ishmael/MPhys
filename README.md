# MPhys

# Week 1

## 30.01.2025

Summary of last semester
##### Noether Cluster

https://github.com/MANHEP/maf-helpdesk/blob/master/noether_basic_usage.md

- **Login Node:** Used only for file transfers, compiling code, and job submissions. **Do not run heavy computations here.**
- **Worker Nodes:** Used for computations. You need to request a session on a worker node.

It is thus necessary to _copy critical code and data back into one's home or Lab directory_ before the interactive session terminates.


``` shell
ssh abercaru@noether.hep.manchester.ac.uk
Ab1357924680

[abercaru@vm119 ~]$ pwd                           # <---- On Noether's login node!
/gluster/home/abercaru

condor_submit -i  getenv=True
[abercaru@wn3802270 dir_1649162]$ pwd
/scratch/condor_pool/condor/dir_1649162

[mrtest@wn3801320 ~]$ cd $_CONDOR_SCRATCH_DIR


cd /gluster/data/theory/event-generators/herwig/herwig730/src-old/Herwig-7.3.0/src/Matchbox


scp abercaru@noether.hep.manchester.ac.uk:/gluster/data/atlas/abercaru/SM_test/LHC-FRModel.hepmc .

scp ./Christoph-Model_UFO.tar.gz
abercaru@noether.hep.manchester.ac.uk:/gluster/data/atlas/abercaru/CRT_test

source ----theory/mphysproject/ana-karim/activate_herwig.sh
Herwig read .in file (de unde)
```

``` shell
C:\Users\anate>ssh abercaru@noether.hep.manchester.ac.uk
(abercaru@noether.hep.manchester.ac.uk) Password:
Last login: Tue Feb  4 12:41:44 2025 from 10.204.58.116
[abercaru@vm119 ~]$ pwd
/gluster/home/abercaru
[abercaru@vm119 ~]$ ls
[abercaru@vm119 ~]$ cd $_CONDOR_SCRATCH_DIR
[abercaru@vm119 ~]$ ls
[abercaru@vm119 ~]$ pwd
/gluster/home/abercaru
[abercaru@vm119 ~]$ echo $_CONDOR_SCRATCH_DIR

[abercaru@vm119 ~]$ $ condor_submit -i getenv=True
-bash: $: command not found
[abercaru@vm119 ~]$ condor_submit -i  getenv=True
Submitting job(s).
1 job(s) submitted to cluster 5261.
Waiting for job to start...
Welcome to slot1_1@wn3802270.hep.manchester.ac.uk!
You will be logged out after 7200 seconds of inactivity.
[abercaru@wn3802270 dir_1649162]$ pwd
/scratch/condor_pool/condor/dir_1649162
[abercaru@wn3802270 dir_1649162]$
```

Here the shell session of user `mrtest` was teleported to work-node `wn3801320` _under the auspices of the HTCondor scheduler_ (hence the time limit). Note that the working directory `getenv=True` is _not_ `mrtest`'s home directory on Noether! -- it is a _scratch directory_ which is _local to the node_. Heavy IO work should be _confined to these local scratch directories_. However, `mrtest` can easily access his _cluster-wide home directory_ simply by issuing `cd`as follows:


For testing purposes we will need to run Herwig and Rivet on our own machines. We install them as docker images.
##### **What is a Docker Image?**

A **Docker image** is a **lightweight, standalone, and executable package** that contains everything needed to run a software application, including: code, libraries, dependencies, system tools, configurations

**Docker images are like virtual machines but much more efficient** because they share the **host operating system kernel** rather than running a full separate OS.


``` bash
Rivet 4.0.3 docker activation

docker run --rm -it -v /mnt/d/Samples:/data hepstore/rivet bash

root@c026cfba8ef1:/work# rivet -a MC_VH2BB -o /data/MC_VH2BB_output.yoda /data/LHC.hepmc

Herwig 7.1.3 docker commands

docker run --rm -it -v /mnt/d/Samples:/data herwigcollaboration/herwig-7.3:7.3.0 Herwig bash
```

## 01.02.2025

Getting used to Herwig. What can it do?

```
cd /Herwig/EventHandlers
set EventHandler:CascadeHandler NULL
set EventHandler:CascadeHandler:MPIHandler NULL
set EventHandler:DecayHandler NULL
set EventHandler:HadronizationHandler NULL

```

## 02.02.2025

Because SMEFTsim (or our adapted Chritoph model) are the only

Option 1 - With Madgraph
  1: Run Madgraph as you did last sem, but now also do "output madevent mysim"
  2: This will make a folder "mysim" in which you will find LHE Files
  3: Use LHEReader in Herwig to Shower, MPI, Hadronize etc

Option 2 - With UFO2Herwig
  1: Use the instructions on the website
  2: Use the input file with the settings Karim and I looked at yesterday

The first thing you can do is try using ufo2herwig:
https://herwig.hepforge.org/tutorials/bsm/ufo.html
This is will automatically generate the input file for you to use. I'd say keep the simple input file around too, so you can do comparison, check for anything

Setting up a first trial input file for Herwig to read and run, LHE.in which uses input from Madgraph. The workflow in this case is this : generate a .lhe file through Madgraph. Reference this file in your input file - and it will be used

``` cpp
##################################################
# Example generator based on LHC parameters
# Generic Les Houches Event file input
# Look at customised input files for:
# MadGraph5/aMC@NLO: LHE-MCatNLO.in
# POWHEG:	     LHE-POWHEG.in
# FxFx merging with MG5/aMC@NLO: LHE-FxFx.in
# Tree-level merging with MG5/aMC@NLO: LHE-MGMerging.in
# usage: Herwig read LHE.in
##################################################
# Technical parameters for this run
##################################################
cd /Herwig/Generators
set EventGenerator:NumberOfEvents 10000
set EventGenerator:RandomNumberGenerator:Seed 31122001
set EventGenerator:DebugLevel 0
set EventGenerator:PrintEvent 10
set EventGenerator:MaxErrors 10000
##################################################
#   Create the Les Houches file handler and reader
##################################################
cd /Herwig/EventHandlers
library LesHouches.so
# create the event handler
create ThePEG::LesHouchesEventHandler LesHouchesHandler

# set the various step handlers
set LesHouchesHandler:PartonExtractor /Herwig/Partons/PPExtractor
set LesHouchesHandler:CascadeHandler /Herwig/Shower/ShowerHandler
set LesHouchesHandler:DecayHandler /Herwig/Decays/DecayHandler
set LesHouchesHandler:HadronizationHandler /Herwig/Hadronization/ClusterHadHandler

# set the weight option (e.g. for MC@NLO)
set LesHouchesHandler:WeightOption VarNegWeight

# set event hander as one to be used
set /Herwig/Generators/EventGenerator:EventHandler /Herwig/EventHandlers/LesHouchesHandler

# Set up an EMPTY CUTS object
# Normally you will have imposed any cuts you want
# when generating the event file and don't want any more
# in particular for POWHEG and MC@NLO you must not apply cuts on the
# the extra jet
create ThePEG::Cuts /Herwig/Cuts/NoCuts

####################################################################
# PDF settings #
####################################################################
# You may wish to use the same PDF as the events were generated with
create ThePEG::LHAPDF /Herwig/Partons/LHAPDF ThePEGLHAPDF.so
set /Herwig/Partons/LHAPDF:PDFName CT14lo
set /Herwig/Partons/RemnantDecayer:AllowTop Yes
set /Herwig/Partons/LHAPDF:RemnantHandler /Herwig/Partons/HadronRemnants
set /Herwig/Particles/p+:PDF /Herwig/Partons/LHAPDF
set /Herwig/Particles/pbar-:PDF /Herwig/Partons/LHAPDF
set /Herwig/Partons/PPExtractor:FirstPDF  /Herwig/Partons/LHAPDF
set /Herwig/Partons/PPExtractor:SecondPDF /Herwig/Partons/LHAPDF

# We would recommend the shower uses the default PDFs with which it was tuned.
# However it can be argued that the same set as for the sample should be used for
# matched samples, i.e. MC@NLO (and less so POWHEG)
#set /Herwig/Shower/ShowerHandler:PDFA /Herwig/Partons/LHAPDF
#set /Herwig/Shower/ShowerHandler:PDFB /Herwig/Partons/LHAPDF

# You can in principle also change the PDFs for the remnant extraction and
# multiple scattering. As the generator was tuned with the default values
# this is STRONGLY DISCOURAGED without retuning the MPI parameters
# create the reader and set cuts
create ThePEG::LesHouchesFileReader LesHouchesReader
set LesHouchesReader:FileName /home/ana/workspace/mad/saves/Events/run_01/unweighted_events.lhe.gz
set LesHouchesReader:AllowedToReOpen No
set LesHouchesReader:InitPDFs 0
set LesHouchesReader:Cuts /Herwig/Cuts/NoCuts

# option to ensure momentum conservation is O.K. due rounding errors (recommended)
set LesHouchesReader:MomentumTreatment RescaleEnergy
# set the pdfs
set LesHouchesReader:PDFA /Herwig/Partons/LHAPDF
set LesHouchesReader:PDFB /Herwig/Partons/LHAPDF
# if using BSM models with QNUMBER info
#set LesHouchesReader:QNumbers Yes
#set LesHouchesReader:Decayer /Herwig/Decays/Mambo
# and add to handler
insert LesHouchesHandler:LesHouchesReaders 0 LesHouchesReader

##################################################
#  Shower parameters
##################################################
# normally, especially for POWHEG, you want
# the scale supplied in the event files (SCALUP)
# to be used as a pT veto scale in the parton shower
set /Herwig/Shower/ShowerHandler:MaxPtIsMuF Yes
set /Herwig/Shower/ShowerHandler:RestrictPhasespace Yes
# Shower parameters
# treatment of wide angle radiation
set /Herwig/Shower/PartnerFinder:PartnerMethod Random
set /Herwig/Shower/PartnerFinder:ScaleChoice Partner
# with MC@NLO these parameters are required for consistency of the subtraction terms
# suggested parameters (give worse physics results with POWHEG)
#set /Herwig/Shower/KinematicsReconstructor:InitialInitialBoostOption LongTransBoost
#set /Herwig/Shower/KinematicsReconstructor:ReconstructionOption General
#set /Herwig/Shower/KinematicsReconstructor:InitialStateReconOption Rapidity
#set /Herwig/Shower/ShowerHandler:SpinCorrelations No

##################################################
# LHC physics parameters (override defaults here) 
##################################################
# e.g if different top mass used
#set /Herwig/Particles/t:NominalMass 173.0

#hepmc
insert /Herwig/Generators/EventGenerator:AnalysisHandlers[0] /Herwig/Analysis/HepMCFile
set /Herwig/Analysis/HepMCFile:PrintEvent 100
set /Herwig/Analysis/HepMCFile:Format GenEvent
set /Herwig/Analysis/HepMCFile:Units GeV_mm

##################################################
# Save run for later usage with 'Herwig run'
##################################################
cd /Herwig/Generators
saverun LHE EventGenerator
```


# Week 2

> [!success] Meeting Verbatim
> To do - truth level analysis (whatever sophisticated analysis we want)
> ROOT file skips over intermediate particle - only contains info about the final particles
> We managed to output a .hepmc file which has all the intermediate particles
> To read .hepmc ---> use Rivet / PyHepmc
> What can we do with jet finding with PyHepmc. In RIVET - everything is built in, you can do the projections and go back through the event record/ the jet record and find the individual clustering
> RIVET TOOL - fastjet building (jet obsejt where all of the individual clustering associated with) You can go backwards, uncluster jets using fastjet (package called by RIVET)
> RIVET OBJECTS - projections
> mpi ??? softjet ???
> Jet constituents correlations
> LundNet (lund plane variables - GNNs)
> Tutorial for model (ask Valentina)
> 
> Up until now used Madgraph with SMEFTsim to output the lhe files. Fed said .lhe files into Herwig
> 
> (The other way is generating the Matrix elements within Herwig - for this need to convert the UFO file to something Herwig understands)
> 
> In the Herwig documentation it says that - they couldn't implement the algorithm from the paper you sent except for the case that the Matrix elements squared are outputted from Madgraph. (speak to Mike)
> 
> If it uses the .lhe - the matrix element calculations have already been done by Madgraph. If instead it uses Madgraph to collect the matrix elements, then it can calculate from those.
> 
> In the first case it would have to spontaneously inventing information (to compensate for what the .lhe file lacks - spin correlations - Madgraph looses them). It doesn't know how to construct the correlations in phase space cause it was zeroed during the calculation. It has to calculate the proper spin density matrix. 
> 
> What we learned in semester one is not consistent with this approach.
> 
> What we want in fact is to call in Madgraph just as a matrix element calculator (not the cross sections) From this assemble the spin density matrix. So in this context what file does Madgraph outputs such that it contains the matrix elements. Apparently they should be contained in the HELAS directory
> 
> What we have shown in semester one is in fact if you get to the corss section calculation - so after the amplitude the interference effect is killed. The specific physics effect that we are looking for is when the helicity of the bb~ pair come from the Higgs boson is different from the standard model aplitude in the bsm amplitude - we are looking at an interference effect where those helicities aren't the same.
> When you calculate this in Madgraph then when madgraph will only produce a non zero value when the helicites in the two amplitudes are the same
> 
> The reason why we want to use Herwig in the first place is to not fix those helicites of the b's. Andy thinks that by the time the cross section calculation is done and is passed to the lhe file it would have killed the exact physics we want to look at
> 
> So, is there a way in which we can use Madgraph as an amplitude generator? - so that the spin density matrix can be calculated. The physics should show in the off diagonal elements of this density matrix
> 
> Definition. Spin density matrix - the different helicity contributions
> 
> We want the core Madgraph from within Herwig. As long as it know where it is it can call it.



---------------------------------------------
UFO2Herwig

This is will automatically generate the input file for you to use. I'd say keep the simple input file around too, so you can do comparison, check for anything

In addition to the wide range of internal BSM models it is possible to use most models using the UFO format with Herwig. **Herwig can currently only handle the perturbative Lorentz structures which arise in the coupling of particles but in most cases this is sufficient.**


> [!NOTE]  
> Highlights information that users should take into account, even when skimming.

> [!TIP]
> Optional information to help a user be more successful.

> [!IMPORTANT]  
> Crucial information necessary for users to succeed.

> [!WARNING]  
> Critical content demanding immediate user attention due to potential risks.

> [!CAUTION]
> Negative potential consequences of an action.
> 

# Week 3 (10.02 - 16.02)

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

Yes, b-hadrons are formed **after** the initial parton showering. The process is as follows:

Paragraph on Anti -k

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

~ this needs a lot of Rivet details

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

- `H → bb̄` = 58% branching ratio.
- ggF production swamped by QCD → VH production (Z or W + H) is preferred for cleaner triggering.
- Boosted selection increases S/B ratio.

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

In principle, this analysis provides a robust starting point for our study.
 
----------
### Theoretical Note on Spin Correlations

This week I focused entirely on understanding the Rivet framework in depth. I implemented custom projections, which now allow me to search the event record at truth level. This includes access to the full decay structure and particle ancestry, enabling me to track spin-relevant quantities from the initial hard process down to the final-state observables.

### Spin Correlation Test (Adapted from Bernreuther)

Using the method from [hep-ph/9701347](https://arxiv.org/pdf/hep-ph/9701347), originally developed for studying spin correlations in \( t\bar{t} \) decays, I constructed a test to assess whether spin information is preserved in our simulation of \( H \to b\bar{b} \). The procedure is:

- Identify the Higgs boson in the event record.
- Follow its decay to the two b-quarks.
- Define two decay branches from the b and \( \bar{b} \), and trace each branch through the parton shower and hadronization.
- For each branch, identify the **last B-hadron** before decay.
- Store the momentum and decay structure of that B-hadron as a proxy for the original b-quark spin information.

This allows for a truth-level observable that can potentially capture spin correlations passed down from the Higgs decay.

A second reference [arXiv:1410.6362](https://arxiv.org/pdf/1410.6362) provides context on using truth-level observables to probe CP and spin effects in hadronic decays. Relevant for validating the above method.


As part of validating whether Herwig is correctly preserving spin correlations in \( H \to b\bar{b} \), I took a closer look at the theoretical framework laid out in Bernreuther et al. ([hep-ph/9701347](https://arxiv.org/pdf/hep-ph/9701347)). Their analysis is built for the case of \( \phi \to t\bar{t} \), but the methodology generalizes.

They start from a Yukawa-like interaction for a mixed CP Higgs:
\[
\mathcal{L}_Y = -\frac{m_f}{v} \bar{f} (a_f + i \gamma_5 \tilde{a}_f) f \, \phi
\]
so the decay products can carry scalar and pseudoscalar components depending on \( a_f, \tilde{a}_f \). The key insight is that this structure imprints itself in the **spin density matrix** of the final-state fermion pair. They write this matrix as:
\[
R = A \cdot \mathbb{1} \otimes \mathbb{1} + B_i^+ \sigma^i \otimes \mathbb{1} + B_i^- \mathbb{1} \otimes \sigma^i + C_{ij} \sigma^i \otimes \sigma^j
\]
where the \( C_{ij} \) term encodes the spin-spin correlation — the main object of interest.

To quantify the effect of CP violation, they build a basis of spin observables:
\[
\begin{aligned}
\mathcal{O}_1 &= \hat{k} \cdot (\vec{s}_1 - \vec{s}_2) \quad &\text{(CP-odd)} \\
\mathcal{O}_2 &= \hat{k} \cdot (\vec{s}_1 \times \vec{s}_2) \quad &\text{(CP-odd)} \\
\mathcal{O}_3 &= \vec{s}_1 \cdot \vec{s}_2 \quad &\text{(CP-even)} \\
\mathcal{O}_4 &= (\hat{k} \cdot \vec{s}_1)(\hat{k} \cdot \vec{s}_2) \quad &\text{(CP-even)}
\end{aligned}
\]
and define expectation values:
\[
\langle \mathcal{O}_i \rangle = \frac{\text{Tr}(R \, \mathcal{O}_i)}{\text{Tr}(R)}
\]
These are the theoretical quantities they aim to measure.

---

In practice, they construct CP-odd observables like:
\[\mathcal{E}_1 = \langle \hat{k}_t \cdot \hat{p}_{\ell^+}^* \rangle_{\mathcal{A}} + \langle \hat{k}_t \cdot \hat{p}_{\ell^-}^* \rangle_{\bar{\mathcal{A}}}\]
and
\[\mathcal{E}_2 = \langle \hat{k}_t \cdot (\hat{p}_{\ell^+}^* \times \hat{p}_{\bar{b}}^*) \rangle_{\mathcal{A}} - \langle \hat{k}_t \cdot (\hat{p}_{\ell^-}^* \times \hat{p}_b^*) \rangle_{\bar{\mathcal{A}}}\]
These are **averages over events**, and that’s the key point — spin correlations aren’t extracted from a single decay but from statistical asymmetries over many events. \( \mathcal{E}_2 \), in particular, is sensitive to spin-spin interference and is strongly CP-odd.

---

### Adaptation to \( H \to b\bar{b} \)

Because b-quarks hadronize, we can’t use spinors directly — but we can still probe spin-sensitive structure if we trace:
- Higgs → b, \( \bar{b} \)
- Follow both decay branches forward to the last B-hadron before decay.
- Use the 3-momenta of the resulting B-hadrons and their decay products as spin analyzers.

By analyzing angular distributions (e.g. triple products), we can reconstruct CP-odd observables analogously to \( \mathcal{E}_2 \). In particular, we implement:
\[
\vec{k}_b \cdot (\vec{n}_{bb} \times \vec{n}_{ee})
\]
as a Rivet observable, where \( \vec{n}_{bb} \) and \( \vec{n}_{ee} \) are plane normals built from the decay products of each b-branch and the Z → \( \ell^+ \ell^- \) system respectively.

This procedure is entirely at truth level and gives us a well-defined way to verify whether spin correlations survive in our event generator output.


  ![image](https://github.com/user-attachments/assets/31b31e17-a126-489a-9efa-16e0bf7024a9)

---
~ reference rivet analysis LAMBDAB, HIGG2BB

![image](https://github.com/user-attachments/assets/a93604af-150a-4260-aaff-9d1226ea7fef)![image](https://github.com/user-attachments/assets/a8b6759e-4578-4178-a239-126d4b7fd4aa)
![image](https://github.com/user-attachments/assets/21dbe7e6-b539-440d-b98d-85f6a606273d)![image](https://github.com/user-attachments/assets/1e1273f7-192c-4a95-8f32-8b43044068c3)




### Outstanding Issues

- **Spin correlations may not be enabled.**  
  Based on our truth-level observables, we do not see evidence of spin structure being preserved in the decay. Need to verify if Herwig is including spin correlations by default. Request: check with Mike whether there is any verbose Herwig output or flag that confirms spin density matrices are being calculated.

- **Christoph’s UFO model may be misconfigured.**  
  Approximately 17% of events show bottom-loop contributions, which should not be allowed by the model. This may be a limitation of the UFO → Herwig translation (e.g., via UFO2Herwig). Needs further inspection.

issue with Higgs decay ~ reference HIGGS_DECAY_HISTO, HIGGS_2PLUS, HIGGS_DECAY_ALL
---

### Final Note

We now have a working Rivet setup capable of tracing the full event structure and performing spin-sensitive truth-level observables. However, the physical validity of the results — especially regarding spin correlations and model consistency — remains uncertain and requires further checks.

------------------------------
### Week 6 (starting 03.02.2025)

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

## Context Check: Event Generators

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


![image](https://github.com/user-attachments/assets/e91bfd89-5559-43ff-9173-dd235835b79b)
![image](https://github.com/user-attachments/assets/55db4483-acd8-47d0-a2ef-3d3a46a29b91)


08.03.2025 - week 6 is ending shortly. At the moment we have trouble picking out why our branching ratios do not match the real world ones. As it has been proven difficult to force the specific decay of the Higgs in the input file - there should be no reason for the ratios to differ. But this could be specific to how Christoph's model is built. This needs to be verified using the SM model that Madgraph uses (CRT model was built on top of this one)

I'm trying out different models: see picture above. UFO2HERWIG and afterwards I look inside the anatomy of the event: ~reference HIGGS_DECAY_ALL


The current focus is on devising a sure-fire test for the activation of spin correlations. With several papers in mind:

- Berheuter:
- Uzan:
- Richardson & Webster:

--------------------------------
### Week 7 (10.03 - 16.03)

Deconstructing the Richardson and closley related PanScales paper

. In Fig. 6 we show the ratio a2/a0 as a function of the energy fractions z1 and z1 0. In all three cases the ratio is peaked when z1 = z1 0 = 0.5 and is largest in magnitude when both gluons split into quark-antiquark pairs. When only one gluon splits into a quark-antiquark pair the ratio becomes negative and −11.1% around the peak. When both gluons split into gluons the spin correlations almost vanish. In all three cases the ratio vanishes when either of the energy fractions approach 0 or 1.

What This Means:

- In QCD, calculations are performed as a power series expansion in **αs**, which is a small parameter at high energies.
- The leading-order (LO) term in this expansion corresponds to **O(αs⁰)** (tree-level diagrams).
- The next-to-leading order (NLO) corresponds to **O(αs¹)** (one-loop corrections).
- The next-to-next-to-leading order (NNLO) corresponds to **O(αs²)** (two-loop corrections or two additional emissions in real corrections).

Context in This Paper:

- The authors mention **O(αs²)** because they are working with **two collinear splittings** (branchings).
- In order to study **azimuthal correlations** between splitting planes, they need at least two emissions, which naturally arises at **O(αs²)** in perturbation theory.
- This is a **fixed-order** calculation, meaning they do not include effects from all higher orders in αs, but rather stop at αs².

Why **O(αs²)** is Special Here:

- Since a single splitting happens at **O(αs¹)** (e.g., a quark emits a gluon), observing **correlations between two splittings** requires an additional emission, bringing the total order to **O(αs²)**.
- They aim to measure how spin effects from different splittings correlate by analyzing the azimuthal angle **Δψ** between the splitting planes.

Going back to the Richardson paper - they specify they work in the massless quark limit -whatever that means and how we could activate it to replicate it exactly we don't know

Question - how do we turn the massless approx. on so that we can fully replicate the Richardson paper.
Question - why does Herwig have so much more g--->gg events than g --->qq 


3.1 Correlations inside the Parton Shower
Subsequent splitting. Needs the intermediate gluon (stronger correlations)

3.2 
probe the correlations between the parton shower and the hard process.
H ----> g g -----> q q q' q'   (100K ---> 400 events) statistic can be forcefully improved
interestingly enough they don claim any z cuts on this process - this clashes with the PanScales paper that recognises that z cuts should pe imposed on this one

It is encouraged to do this one -- however our quarks are massive

In PanScales: about the Richardson algorithm
That algorithm continuously boosts between the lab frame and frames specific to each individual collinear splitting, where individual Collins-Knowles steps may be applied directly

Finlly here is the way I understand it 

![Drawing 2025-03-12 11 14 512 excalidraw (1)](https://github.com/user-attachments/assets/c08aa6e2-de0c-4aeb-9c71-19cdd30f3260)

Karim implements this analysis I ask for in python: 


-------------------------------
### Week 9 (24.03 - 30.03)

Andy sends in [email](emails/26.03.2025.md) 
how many events do we even have of this

First test: write a .csv for the decay chain you have been analysing, i.e. H->b bbar, with b->gb and g-> q qbar [same for bbar decay].
As a matter of fact. We have already done everything he asked. We’re at step 4

Andy suggests contour plot to check 
<img src="https://github.com/user-attachments/assets/102e2e33-b1be-440f-a683-6a61fa97fea0" width="100" height="100"/>


![image](https://github.com/user-attachments/assets/2a7ec977-1ac8-459a-b681-77429c8771b7)

we need better stats 

#### Re-alignment and Dataset Preparation for Gluon Splitting Study

##### 25.03.2025 — Recalibrating Goals, Preparing Gluon Splitting Analysis

- After reading Mike's feedback, we realised we had already progressed beyond his outlined steps.
- I suggested we meet to realign our goals and focus on building the GNN pipeline with the remaining time.
- Karim began writing a Rivet analysis to:
    - Count gluons and quarks in the final state.
    - Specifically trace decay chains: H → b b̄, then b → b g, and finally g → q q̄ or g → g g.
- We clarified that g→gg is much more likely than g→qq̄, and that both types of events should be accepted.
    

##### 26.03.2025 — First Parquet → HDF5 Conversion, Rivet CSV Format

- Reviewed our infrastructure: CSVs from Rivet output (initially Parquet) can be converted to HDF5.
- Using DuckDB to handle large files and filter before writing.
- Final CSV format began to take shape, recording:
    - The **child b-quark** from b → b g (not the parent),
    - Children of the gluon: q₁/q₂ and q₃/q₄, for each branch.
- Removed redundant columns: gluon itself, Higgs children.
- We decided to filter out events where both gluon branches don't produce at least **one valid split**, to reduce CSV size.
- Began debugging why only ~44K out of 82K H→bb̄ events showed valid decay chains — suspected asymmetric showering.

##### 27.03.2025 — Matching Analyses and Visual Debugging

- Visualised suspect events using `pyhepmc` and `graphviz`. Inspected events 1, 2, 5, 6.
- Karim confirmed that the Richardson routine matched the Rivet output exactly, with correct PID and momentum conservation.
- Confirmed that **hadronisation being turned on** is the likely reason for getting more g→qq̄ events (~28% hit rate vs 0.015% without).
- New filtering logic added in Rivet: remove all-zero rows, only write events where both b and b̄ split via b→b g, and the g splits.

Herwig run structure for visualisation:

```
cd /Herwig/Generators
set /Herwig/Analysis/Plot:EventNumber 106
insert EventGenerator:AnalysisHandlers 0 /Herwig/Analysis/Plot
Herwig run runfile.run -N100000000 -j16
dot -Tpng LHC-Matchbox-Plot-106.dot > plot.png
```

##### 28.03.2025 — Full Integration of Rivet into Herwig

- Karim managed to run **Rivet from inside Herwig**, on multiple cores, without producing `.hepmc` output.
- Each job writes a single `.csv` file with Rivet output — massive performance gain.
- Estimated: 100M events in ~2 hours on 16 cores.
- This becomes our new strategy for handling large-scale analysis with minimal disk I/O.



-------------------------------
### Week 10 (31.03 - 6.04)

#### 02.04.2025
Karim changes the python analysis into a contour plot of the Asymmetry term. The stats are not the issue - we do not in fact see a 2sigma difference



Something that has been bothering me for a while but I had no time to address it is the skewed. Let's try to make sense of it. One way to do this is cross checking with what MadGraph generates for the same settings. 

We use the fact that we do not shower with Herwig this time. 


**1. Philosophy of MadGraph:**

- MadGraph is primarily focused on generating **parton-level events** from **hard scatterings**.
- It works with **on-shell particles** for final states.
- You must **explicitly specify decays** in the process definition if you want the decays to be handled correctly.
- MadGraph assumes **final states** are **stable** or at least **treated as stable** during the event generation.
#### **Why MadGraph Doesn't Automatically Handle Decays:**

- MadGraph performs **matrix element calculations** for the **hard scattering process** and not for the **decays**.
- The decays must be **explicitly included in the process definition**, as they are treated as **subprocesses**.
- It does **not handle decays on the fly** because that would **mix parton-level generation with hadronization**, which is against the modular philosophy of MadGraph.

 **2. Philosophy of Herwig:**

- Herwig is primarily a **Monte Carlo event generator** that handles both **hard scattering (like MadGraph)** and **full event simulation (including showers and hadronization)**.
- It has **built-in decay tables** and **decay widths** from the **UFO model files**.
- Herwig **automatically decays** any unstable particles it encounters during the event generation, unless explicitly told not to.

**Why Herwig Handles Decays Differently:**
- Herwig, through **UFO2Herwig**, imports all **interactions and decay widths** from the **UFO model file**.
- Once the **Higgs production process** is defined, Herwig **automatically applies** the **decay branching ratios** based on the **decay width table**.
- You don't need to specify **decay chains explicitly**. Herwig will decay **all unstable particles** unless explicitly prevented from doing so.
  ![image](https://github.com/user-attachments/assets/aa06bd91-625b-4d9c-8a4f-d45a7abbea7f)


-------------------------------
### Week 11 (7.04 - 13.04)

#### 07.04.2025 — Scaled-Up Production & DAGMan Job Management

We were given access to **8 bulks of 96 cores each** on the Noether cluster. This allowed us to parallelize large-scale event generation for our `pp → H → gg` process.

To avoid cluster congestion and job losses due to time limits, we used **HTCondor’s DAGMan** system to control the submission of batches. Each DAG node manages a group of **26 subjobs**, corresponding to `(nstart, nstop)` ranges with `--sample` either `odd` or `even`.

Each subjob runs a command of the form:
`python3 manager_jobs_modified_96.py --nstart 0 --nstop 24 --sample even`

[[manager_jobs_dag.py]]
#### 09.04.2025 

Persistent Monitoring (Experimental Idea):

Tested a remote control method to monitor or trigger runs from outside Noether:
1. Created a **GitHub Gist** with an executable bash snippet.
2. Launched a **`tmux` session** on Noether containing:

`while true; do   curl -s https://gist.githubusercontent.com/ana-gist-id/raw/script.sh | bash   sleep 60 done`

This allowed for live script updates without re-login. **NOTE:** This approach was later abandoned due to security concerns, as flagged by Andy and others. [see emails](emails/09.04.2025.md)

#### 13.04.2025
All JOBS done and uploaded on drive (3B events for each sample - odd/even   pi/4, -pi/4).
