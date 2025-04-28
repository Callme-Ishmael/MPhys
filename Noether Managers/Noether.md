# 🌟 Using the Noether Cluster Effectively: A Practical Guide for Physics Students

## Introduction

The Noether Cluster is a powerful computing resource provided by the University of Manchester, intended for computationally intensive physics research. However, first-time users often find it challenging to navigate its environment effectively.  
This guide offers a step-by-step tutorial based on real experience using Noether for high-energy physics simulations (e.g., with **Herwig**, **MadGraph**, and **Rivet**).

---

## 1. Accessing Noether

### Step 1: Request an Account

- Apply for a Noether account through your supervisor or course organizer.
- Once approved, you’ll receive a username and limited storage quota (~20 GB in your home directory).

### Step 2: SSH into Noether

```bash
ssh USERNAME@noether.cld.manchester.ac.uk
```

Replace `USERNAME` with your Noether username.

If you're on Windows, it’s easiest to use **WSL (Windows Subsystem for Linux)** or a terminal like **MobaXterm** or **VSCode Remote-SSH**.

---

## 2. Understanding Storage: Home Directory vs `/gluster/data`

- Your **home directory** (`/home/USERNAME/`) has limited space (~20 GB).
- For **large event files, analysis outputs, or Condor jobs**, use the shared `/gluster/data/atlas/USERNAME/` space:
  - Unlimited for practical purposes.
  - Accessible across nodes.

Create your folder structure:

```bash
mkdir -p /gluster/data/atlas/YOURNAME/your_project/
```

> 🔔 **Important**: Always work and run from `/gluster/data`, not your home directory, for big jobs.

---

## 3. Loading Software (Herwig, MadGraph, Rivet, etc.)

Noether uses module files or manual activation scripts.

### Example: Activating Herwig

```bash
source /gluster/data/theory/event-generators/herwig/activate_herwig.sh
```

### Installing MadGraph Locally

```bash
cd /gluster/data/atlas/YOURNAME/
wget https://launchpad.net/mg5amcnlo/3.0/3.4.x/+download/MG5_aMC_v3.4.2.tar.gz
tar -xzvf MG5_aMC_v3.4.2.tar.gz
cd MG5_aMC_v3_4_2
./bin/mg5_aMC
```

Then install models inside MadGraph as needed (e.g., SMEFTsim, HC).

---

## 4. Running Jobs with Condor

Use Condor for batch job submissions.

### 4.1 Create a Submission File (`submit.sub`)

```text
executable = run_script.sh
arguments = $(ProcId)
output = logs/job_$(ProcId).out
error = logs/job_$(ProcId).err
log = logs/job_$(ProcId).log
request_cpus = 1
request_memory = 2GB
queue 10
```

### 4.2 Create the Run Script (`run_script.sh`)

```bash
#!/bin/bash
source /gluster/data/theory/event-generators/herwig/activate_herwig.sh
python3 your_analysis.py --option whatever
```

Make it executable:

```bash
chmod +x run_script.sh
```

### 4.3 Submit Jobs

```bash
condor_submit submit.sub
```

> 🔔 Important: Always write outputs to `/gluster/data/atlas/YOURNAME/`, not your home directory.

---

## 5. Monitoring Jobs

Check running jobs:

```bash
condor_q $USER
```

Remove all your jobs (if needed):

```bash
condor_rm $USER
```

Check cluster machine status:

```bash
condor_status
```

Tail job output for live checking:

```bash
tail -f logs/job_X.out
```

---

## 6. Best Practices & Tips

- Use random seeds carefully in event generators when running multiple jobs.
- Parallelize parameter scans (e.g., varying coupling constants) over multiple Condor jobs.
- Always log outputs, parameters, and runtime info.
- Clean up old event files to save space.
- Use `screen` or `tmux` if running long interactive jobs to avoid losing progress.
- Keep Condor submission scripts modular to easily vary seeds, parameters, and output paths.

---

## 7. Advanced: Setting up Notifications (Optional)

Set up an automatic script that monitors:

- When `condor_q $USER` returns empty (no running jobs), trigger a webhook or send yourself an email.
- You can use a simple script or services like IFTTT or PythonAnywhere.

---

## 8. Common Issues

| Issue | Solution |
|:------|:---------|
| `Permission Denied` on `/gluster/data` | Check folder permissions with `chmod -R 755 your_folder` |
| Condor jobs stuck | Kill them with `condor_rm $USER` and check your submission files |
| Herwig activation fails | Ensure correct activation script is sourced |
| MadGraph crashes | Reinstall model or regenerate process |
| Large LHE files | Apply parton-level cuts to reduce event sizes |

---

## 9. Recommended Project Folder Structure

```text
/gluster/data/atlas/YOURNAME/project_name/
├── code/
│   ├── run_analysis.py
│   └── run_jobs.sh
├── events/
│   ├── alpha_0/
│   └── alpha_90/
├── logs/
│   └── condor_logs/
├── results/
│   └── plots/
├── submit/
│   ├── submit.sub
│   └── run_script.sh
└── README.md
```

---

# 🚀 Good Luck and Happy Simulations!
