# Using the Noether Cluster: A Practical Guide for High-Energy Physics Simulations

## Introduction

The **Noether Cluster** at the University of Manchester provides extensive computational resources for physics students and researchers engaged in high-performance computing tasks, particularly in particle physics. This guide serves as a practical tutorial for effectively using Noether for simulation workflows involving tools like **Herwig**, **MadGraph5_aMC@NLO**, and **Rivet**, and covers best practices based on real user experience.

---

## 1. Cluster Specifications

As of the current configuration, Noether comprises:

- **8 high-performance nodes**  
  - 96 cores, 384 GB RAM (4 GB/core)  
  - Intel(R) Xeon(R) Gold 5220R CPU @ 2.20GHz  

- **20 standard nodes**  
  - 16 cores, 64 GB RAM (4 GB/core)  
  - Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz  

- **3 GPU nodes**  
  - 32 cores, 128 GB RAM  
  - 3x NVIDIA Tesla V100 GPUs each  
  - Same CPU as standard nodes  

> Total: **31 compute nodes**, **1184 cores**, **9 GPUs**. Hardware availability may vary slightly with maintenance and upgrades.

---

## 2. Getting Started

### Account Request and Access

- Apply for access through your course leader or supervisor.
- Upon approval, you'll receive a username and access to your home directory (`/home/YOURNAME/`, ~20 GB quota).

### Connecting to Noether

```bash
ssh YOURNAME@noether.hep.manchester.ac.uk
```

Windows users are encouraged to use WSL, VSCode Remote SSH, or MobaXterm for smoother SSH workflows.

## 3. Storage: Home Directory vs Shared Space

Your home directory has limited capacity. Use the shared group space:

```bash
/gluster/data/atlas/YOURNAME/
```

Create a working project folder:

```bash
mkdir -p /gluster/data/atlas/YOURNAME/my_project/
cd /gluster/data/atlas/YOURNAME/my_project/
```

Always run simulations and store large output files in `/gluster/data`, not in your home directory.

## 4. Activating Software Environments

**Example: Herwig**

```bash
source /gluster/data/theory/event-generators/herwig/activate_herwig.sh
```

This script sets the necessary environment variables and paths for using Herwig.

**Installing MadGraph Locally**

```bash
cd /gluster/data/atlas/YOURNAME/
wget https://launchpad.net/mg5amcnlo/3.0/3.4.x/+download/MG5_aMC_v3.4.2.tar.gz
tar -xzf MG5_aMC_v3.4.2.tar.gz
cd MG5_aMC_v3_4_2
./bin/mg5_aMC
```

Install BSM models (e.g., SMEFTsim, Higgs Characterisation) within MadGraph as needed.

## 5. Running Batch Jobs with HTCondor

HTCondor allows you to submit and manage batch jobs across Noether nodes.

### 5.1 Submission File (`submit.sub`)

```text
executable = run_script.sh
arguments = $(ProcId)
output = logs/job_$(ProcId).out
error  = logs/job_$(ProcId).err
log    = logs/job_$(ProcId).log
request_cpus = 1
request_memory = 2GB
queue 10
```

### 5.2 Execution Script (`run_script.sh`)

```bash
#!/bin/bash
source /gluster/data/theory/event-generators/herwig/activate_herwig.sh
python3 my_analysis.py --sample $(($1))
```

Make it executable:

```bash
chmod +x run_script.sh
```

### 5.3 Submit Jobs

```bash
condor_submit submit.sub
```

## 6. Monitoring and Managing Jobs

```bash
condor_q $USER         # View current jobs
condor_rm $USER        # Cancel all running jobs
condor_status          # View available nodes
tail -f logs/job_X.out # Live monitoring of output
```

## 7. Using DAGMan for Job Dependencies and Persistence

DAGMan (Directed Acyclic Graph Manager) allows you to chain jobs with defined dependencies (e.g., preprocessing → simulation → postprocessing). DAGMan is especially useful for structured simulations or parameter scans.

More importantly, DAGMan jobs are not subject to the 24-hour execution limit imposed on standalone jobs. On Noether, any job that runs longer than 24 hours will be automatically killed by the system. DAGMan bypasses this limitation by submitting jobs incrementally through its own meta-scheduler, which is treated as a "pseudo-job" by Condor. This makes it ideal for long-running workflows.

**Example DAG file:**

```text
Job A preprocess.sub
Job B run_simulation.sub
Job C postprocess.sub

Parent A Child B
Parent B Child C
```

Submit the DAG:

```bash
condor_submit_dag job_chain.dag
```

Use this approach for all workflows that may exceed 24 hours in wall time or that require interdependent stages.

## 8. Using tmux for Long Interactive Sessions

When running long or interactive jobs directly:

```bash
tmux new -s mysession
```

Detach with Ctrl+B, then D, and resume later with:

```bash
tmux attach -t mysession
```

This prevents loss of session state due to dropped SSH connections.

## 9. Best Practices

- Work only in `/gluster/data/atlas/YOURNAME/` for heavy jobs.
- Use random seeds properly to avoid identical event samples.
- Structure your job outputs into folders (e.g., `events/`, `logs/`, `plots/`).
- Use `tmux` when running scripts interactively.
- Keep job scripts modular and well-documented.
- Use DAGMan to organize sequential or conditional job logic and bypass 24h limits.
- Clear unused files periodically to manage space responsibly.
- Record software versions and parameters in a `README.md`.

## 10. Sample Folder Structure

```text
/gluster/data/atlas/YOURNAME/my_project/
├── code/
│   └── analysis.py
├── events/
│   └── alpha_90/
├── logs/
│   └── condor/
├── results/
│   └── plots/
├── submit/
│   ├── submit.sub
│   └── run_script.sh
└── README.md
```

## 11. Optional: Job Completion Notification

You can automate job completion alerts using a simple script that monitors `condor_q` and sends a notification via:

- Python email script
- IFTTT webhook
- Slack integration

**Example polling loop:**

```bash
while condor_q $USER | grep "$USER" > /dev/null; do sleep 60; done
python3 manager_jobs.py --run
```

## 12. Further References and Support

Noether Cluster FAQ

For additional support, contact: `noether-helpdesk@manchester.ac.uk`
