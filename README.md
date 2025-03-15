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
