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
herwig read .in file (de unde)
```
