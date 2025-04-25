# MPhys

### Week 1

#### 30.01.2025

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

#### 01.02.2025

Getting used to Herwig. What can it do?

```
cd /Herwig/EventHandlers
set EventHandler:CascadeHandler NULL
set EventHandler:CascadeHandler:MPIHandler NULL
set EventHandler:DecayHandler NULL
set EventHandler:HadronizationHandler NULL

```

#### 02.02.2025

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


### Week 2

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

-------------------------------
### Week 4 (17.02 - 23.02)

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
#### Detangling the Jets Algorithms

b-tagging = technique  to identify jets that likely originated from bottom (b) quarks. This process involves analyzing several distinctive features of b-quark jets:

- **Displaced Vertices:** B-hadrons (particles containing a b-quark) have a relatively long lifetime, so they decay at a measurable distance from the primary collision point. This decay produces a secondary vertex that is displaced from the primary vertex.
- **Impact Parameters:** The tracks of particles from b-hadron decays tend to have large impact parameters (the shortest distance between the track and the primary vertex), which is a signature used in b-tagging.
- **Other Characteristics:** Additional variables, such as the presence of soft leptons from semileptonic decays, help in distinguishing b-jets from jets initiated by lighter quarks or gluons.

**1. Does the b-hadron appear after initial showering, which is supposed to take place instantaneously very near the primary vertex?**

![image](https://github.com/user-attachments/assets/15f4039d-839b-4556-a305-6f7f251b4495)

Yes, b-hadrons are formed **after** the initial parton showering. The process is as follows:

1. **Primary Vertex Production**:
    
    - In your process (pp→Z→ZHpp \to Z \to ZHpp→Z→ZH, with H→bbˉH \to b \bar{b}H→bbˉ), the Higgs boson decays into two bbb-quarks at the **primary vertex**, which is where the hard scattering took place.
2. **Parton Showering** (Occurs Almost Instantly):
    
    - The outgoing **b-quarks** start radiating gluons immediately after being produced, initiating a **parton shower**. This occurs on an extremely short time scale (~10−2410^{-24}10−24 s).
    - The showering mostly occurs **very close** to the primary vertex.
3. **Hadronization** (Formation of B-Hadrons):
    
    - The b-quarks then hadronize into **b-hadrons** (e.g., B0,B+,BsB^0, B^+, B_sB0,B+,Bs​, or Λb\Lambda_bΛb​).
    - This process happens **right after** the showering and still very close to the primary vertex (~10−2410^{-24}10−24 s).
    - However, unlike partons, **b-hadrons** are massive (~~5 GeV) and have a long lifetime (~~10−1210^{-12}10−12 s).
    - Due to their lifetime, **b-hadrons can travel a measurable distance before decaying**, leading to a **secondary vertex**.

What is the purpose of detector vs truth level?
How deep does the algorithm go from the finals states towards the primary vertex such that it is able to tag the jets? 
Does the algorithm mimic an actual detector?
If it goes too deep we call it truth level - and this is not what a detector could do.
If its only surface level from the final states we call it detector level. Tagging requires a secondary vertex in the case of b-tagging ---> the vetex at which a b-hadron starts decaying. What if this secondary vertex is too deep? 


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
