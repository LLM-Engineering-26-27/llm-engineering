# bwUniCluster 3.0: Access and Setup

This guide takes you from no account to a finished GPU test job on bwUniCluster 3.0, the
cluster where the course's graded GPU runs happen. Work through it in order. Every step says
what to do and what you should see.

**When:** do Part A during the first week of the course. Registration has waiting times (the
entitlement can take a working day or more), and you need a working login for the Week 2
exercise. Parts B to D take about 30 minutes once your account works.

**The official reference** for everything in this guide is the bwHPC wiki:
**<https://wiki.bwhpc.de/e/BwUniCluster3.0>**. This guide covers only the steps you need for
the course. Use the wiki when you want the full story on login, file systems or SLURM.

**What you need before you start**

- Your ZDV login ID (the one that looks like `zxabc12`) and its password.
- A smartphone with an authenticator app (for example FreeOTP, Aegis, 2FAS, Google
  Authenticator or Microsoft Authenticator), or a YubiKey.
- A terminal with `ssh`: Terminal on macOS and Linux, PowerShell on Windows 10/11 (or
  [MobaXterm](https://mobaxterm.mobatek.net/), which the bwHPC wiki recommends for Windows).
- A GitHub account that the course staff have invited to the course organization.
- For logging in from home: the university VPN (eduVPN). See step B1.

**Placeholders:** `zxabc12` stands for your ZDV login ID throughout. Replace it with your own
in every command. Text in angle brackets, such as `<job id>`, is also yours to fill in.

**Language:** most pages have an English version. The links below go straight to it. On
`login.bwidm.de`, pick **English** in the language menu at the top of the page.

---

## Part A: Get an account (once)

Registration has four steps. Do them in this order. While you wait for the entitlement
(A1), you can already do A3.

### A1. Request the bwUniCluster entitlement from the university

The entitlement is the university's confirmation that you may use the cluster.

1. Open the ZDV form: <https://uni-tuebingen.de/en/einrichtungen/zentrum-fuer-datenverarbeitung/dienstleistungen/server/computing/registration/bwunicluster/apply-for-entitlement/>
2. Fill in the fields:

   | Field | What to enter |
   |---|---|
   | First and Last Name | your name |
   | ZDV Login ID | your ZDV login ID, for example `zxabc12` |
   | ZDV E-Mail | your university e-mail address |
   | Area of Expertise | `Machine Learning (Computer Science)` |
   | Team | `AG Bethge` |

   Leave the field labelled "Don't fill this field!" empty.
3. Submit the form.
4. Wait. The ZDV processes the request by hand. To check whether it has arrived, log in at
   <https://login.bwidm.de/user/index.xhtml?show=entitlement&highlight=bwUniCluster>
   (choose **Universität Tübingen**, log in with your ZDV ID and password). When a
   bwUniCluster entitlement is listed, continue with A2. If nothing appears after two working
   days, write to <hpcmaster@uni-tuebingen.de>.

### A2. Fill in the bwUniCluster questionnaire

**This step decides which part of the cluster you can use.** Enter the values below exactly,
even if another subject field looks closer to your studies. With other values you may not get
access to the GPU partitions the course uses.

1. Open <https://zas.bwhpc.de/shib/en/bwunicluster_survey.php>
2. Select **Universität Tübingen** as your home organization and click **Proceed**.
3. Log in with your ZDV ID and password.
4. Fill in the questionnaire:

   | Field | What to choose |
   |---|---|
   | DFG subject field | **Communications, High-Frequency and Network Technology, Theoretical Electrical Engineering (408-02)** |
   | Additionally assigned subject fields | leave empty |
   | bwHPC subject field | **Engineering Sciences (50)** |
   | Numerical methods | `pytorch, transformers` |
   | Field of activity | tick **Research** and **Teaching** |
   | Type of activity | tick **Development** and **Methods Development** |
   | EPPN, Email | already filled in, leave as they are |

5. Accept the terms of use and click **Preview**.
6. Check that the preview shows exactly the values in the table, then click **Send**.

If you register for the service (A4) before sending the questionnaire, send it within 14 days,
or your cluster login is deactivated.

### A3. Register a second factor (2FA)

Every login to the cluster asks for a one-time password (OTP) from an authenticator app.

1. Open <https://login.bwidm.de/user/twofa.xhtml>, choose **Universität Tübingen**, and log
   in with your ZDV ID and password. (If an ad blocker or privacy add-on is active, turn it
   off for this site. It can stop the token from being created.)
2. Click **NEW SMARTPHONE TOKEN**, then **Start**, and wait for the QR code.
3. In your authenticator app, add a new entry and scan the QR code. The entry is called
   **bwIDM**. Do not save, print or share the QR code.
4. Type the six-digit code from the app into **Current code:** and click **CHECK**.
   **If you skip CHECK, the token is not activated.**
5. Back on **My Tokens**, click **CREATE NEW TAN LIST**, then **START**, then **SHOW TANS**.
   Print or write down these backup TANs and keep them away from your phone. Each TAN works
   once, for emergencies such as a lost phone.

Create the smartphone token first and the TAN list second, never the other way round.

### A4. Register for the bwUniCluster 3.0 service and set a service password

1. Open <https://login.bwidm.de>, choose **Universität Tübingen**, click **Proceed**, and
   log in with your ZDV ID and password.
2. On your first visit, check the account data shown and click **Continue**.
3. Find the box **bwUniCluster 3.0** and click **Register**. (If it is missing, the
   entitlement from A1 has not arrived yet. If you see "Second factor missing", do A3 first.)
4. Read the terms of use, tick the box to accept them, and click **Register**.
5. Set a **service password** and click **Save**. Use a new password that you use nowhere
   else, and **not** your ZDV password. You type it at every cluster login.

Your account is ready. **Your cluster username is `tu_` followed by your ZDV login ID**, for
example `tu_zxabc12`. If you forget the service password, set a new one on the same page.

---

## Part B: Log in for the first time

### B1. Be on the university network

The cluster accepts connections only from university networks in Baden-Württemberg. On
campus (eduroam or a wired university connection) you can skip this step. From anywhere else,
connect to the university VPN first. The ZDV's eduVPN instructions are here:
<https://uni-tuebingen.de/en/facilities/zentrum-fuer-datenverarbeitung/services/network-services/network-access/remote-access-vpn/>

### B2. Connect with SSH

In your terminal, replacing `zxabc12` with your ZDV ID:

```
ssh tu_zxabc12@uc3.scc.kit.edu
```

1. On the very first connection, `ssh` shows a host key fingerprint and asks whether to
   continue. Compare it with the fingerprints listed on
   <https://wiki.bwhpc.de/e/BwUniCluster3.0/Login>, then type `yes`.
2. At `Your OTP:`, type the current six-digit code from your authenticator app.
3. At `Password:`, type your **service password** from A4.

You should now see a prompt that ends in `$` and shows your username and the machine's name.
You are on a **login node**.
Type `exit` to log out.

On Windows with MobaXterm: create a new SSH session with remote host `uc3.scc.kit.edu`,
username `tu_zxabc12` and port 22.

### B3. Optional: a shorter login command (macOS and Linux)

Add these lines to the file `~/.ssh/config` on your laptop (create it if it does not exist):

```
Host uc3
    HostName uc3.scc.kit.edu
    User tu_zxabc12
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlPersist 4h
```

Now `ssh uc3` logs you in. While the first connection is open (and for four hours after you
close it), further `ssh uc3`, `scp` and `rsync` calls reuse it and ask for no new OTP.

### B4. The one rule of the login node

The login node is shared by everyone on the cluster. Use it **only** to edit files, run `git`,
and submit and watch jobs. **Never run training, tests, `pip install` or any other
computation on it.** Processes like that are killed without warning and can get your account
blocked. All computation runs as a **batch job** on a compute node, as in Part C.

---

## Part C: Set up your workspace and run a first GPU job

### C1. Create a workspace

Course work goes in a **workspace**, the cluster's storage area for job data such as
checkpoints and logs. Your home directory is meant for small, permanent files. Create a
workspace named `lme` for 60 days (the maximum):

```
ws_allocate lme 60
```

The command prints the workspace path. You never need to type that path: `ws_find lme`
prints it, so this command takes you there from anywhere:

```
cd "$(ws_find lme)"
```

**A workspace expires.** After 60 days it and everything in it are deleted. Extend it before
then (you can do this three times, which covers the whole semester):

```
ws_extend lme 60
```

To get an e-mail reminder before it expires, add the workspace to your calendar:

```
ws_send_ical lme your.name@student.uni-tuebingen.de
```

`ws_list` shows your workspaces and how many days each has left.

### C2. Check that you can read the course directory

The course staff keep a shared, read-only course directory on the cluster. It holds:

- the **container image** `pytorch-26.07-py3.sif`, which brings Python, PyTorch and CUDA. Every
  course job runs inside it with Apptainer, so you install nothing on the cluster.
- `pylibs/`, extra Python packages the image lacks (for example `transformers`).
- `assets/synth_monad_v1.npy`, the **full training dataset** (a pre-tokenized token shard)
  used for the graded runs.

List it:

```
ls -l /pfs/work9/workspace/scratch/tu_iiojo01-lme-course/
```

You should see `pytorch-26.07-py3.sif`, `pylibs` and `assets`. Do not copy the image or the
dataset into your workspace. Step D3 links the dataset into your repository instead. If you
get `Permission denied`, send your cluster username (`tu_...`) to the course staff.

### C3. Submit a first GPU job

This job asks for one H100 GPU for five minutes and prints what the container sees.

**1. Go to your workspace:** `cd "$(ws_find lme)"`

**2. Create the job script.** Open a new file with the editor `nano`:

```
nano hello_gpu.sh
```

Paste the lines below, then save with `Ctrl-O`, `Enter` and quit with `Ctrl-X`. Every line
must start at the left edge: if spaces ended up before `#!/bin/bash` or before the last
`EOF`, delete them.

```
#!/bin/bash
#SBATCH --job-name=hello-gpu
#SBATCH --partition=gpu_h100_short
#SBATCH --gres=gpu:1
#SBATCH --time=00:05:00
#SBATCH --output=hello-gpu-%j.out

COURSE=/pfs/work9/workspace/scratch/tu_iiojo01-lme-course
echo "running on $(hostname)"

apptainer exec --nv "$COURSE/pytorch-26.07-py3.sif" python - <<'EOF'
import torch
print("torch", torch.__version__)
print("GPU:", torch.cuda.get_device_name(0))
EOF
```

The `#SBATCH` lines are the job's request: the queue (`gpu_h100_short`, jobs up to 30
minutes), one GPU, a five-minute time limit, and the file the output goes to (`%j` becomes the
job ID). `apptainer exec --nv` runs one command inside the image, here the Python lines
between the two `EOF` markers, and `--nv` makes the GPU visible to it.

**3. Submit it:**

```
sbatch hello_gpu.sh
```

SLURM answers `Submitted batch job 1234567`. The number is your **job ID**.

**4. Watch it.** `squeue --me` lists your jobs. `PD` means it is waiting in the queue, `R`
that it is running. When it no longer appears, it has finished. Waiting a few minutes is
normal. Run `squeue --me` by hand when you want to look, never in a loop or with `watch`: the cluster ends such processes without notice.

**5. Read the output**, replacing the number with your job ID:

```
cat hello-gpu-1234567.out
```

It should start like this:

```
running on uc3n089.localdomain
torch 2.13.0a0+9186a08b2c.nv26.07
GPU: NVIDIA H100
```

The node name will differ. Below these lines the cluster adds a `JOB FEEDBACK` block with the
job's state (`COMPLETED (exit code 0)`), its run time and how much of the requested CPU and
memory it used. If you see an error message instead of the `GPU:` line, see Troubleshooting
below.

You have run a GPU job on the cluster. Delete the two files with
`rm hello_gpu.sh hello-gpu-*.out` if you like.

---

## Part D: Connect your course repository

Do this part once you have access to your pair's repository on GitHub. You work in your own
clone on the cluster. Your partner makes their own.

### D1. Give the cluster access to GitHub

The cluster needs its own SSH key to clone and push. On the **login node**:

1. Create a key. Press `Enter` to accept the default file. If it asks whether to overwrite an
   existing key, answer `n` and continue with step 2 using that key. **Set a passphrase**: the
   key can push to every repository your GitHub account can, and it sits on a shared machine.

   ```
   ssh-keygen -t ed25519 -C "bwunicluster"
   ```
2. Print the public key and copy the whole line:

   ```
   cat ~/.ssh/id_ed25519.pub
   ```
3. On github.com, go to **Settings → SSH and GPG keys → New SSH key**, give it the title
   `bwUniCluster`, paste the line, and click **Add SSH key**.
4. Test it on the cluster:

   ```
   ssh -T git@github.com
   ```

   Before you answer `yes` to the fingerprint question, compare the fingerprint with the ones
   GitHub publishes (search for "GitHub's SSH key fingerprints" on docs.github.com). Then type
   your passphrase. GitHub replies `Hi <your-github-name>! You've successfully authenticated...`.
5. To type the passphrase only once per login instead of at every `git push`, run these two
   commands after you log in:

   ```
   eval "$(ssh-agent)"
   ssh-add
   ```

### D2. Clone your pair's repository into your workspace

On your repository's GitHub page, click **Code → SSH** and copy the address. It looks like
`git@github.com:LLM-Engineering-26-27/<repository name>.git`. On the cluster, go to your
workspace, type `git clone ` (with a space), paste the address and press `Enter`:

```
cd "$(ws_find lme)"
git clone git@github.com:LLM-Engineering-26-27/<repository name>.git
```

Then change into the new folder, which has the repository's name without `.git`:

```
cd <repository name>
```

### D3. Link the training dataset

From the repository root, still on the login node:

```
scripts/run.sh setup
```

It prints `assets/synth_monad_v1.npy -> /pfs/work9/...`: your repository now points at the
shared dataset. Running it again is harmless. If it prints `cannot read`, send your cluster
username to the course staff.

### D4. Check the course environment

From now on, every course job goes through `scripts/run.sh`, which runs your command inside
the course image with the right settings. This check imports PyTorch, `transformers` and the
course package, and asks PyTorch for the GPU. Run the two lines one after the other: the
first stores the Python check in a variable, the second submits it.

```
CHECK='import transformers, llm_engineering, torch; print(torch.cuda.get_device_name(0))'
scripts/run.sh job --time=00:05:00 -- python -c "$CHECK"
```

Note the job ID it prints. When `squeue --me` no longer lists the job, read its log:

```
cat logs/lme-job-<job id>.out
```

The log should start like this (job ID, node, commit and GPU ID will differ):

```
job 7685886 on uc3n104.localdomain, commit e2ddcc8
GPU 0: NVIDIA H100 (UUID: GPU-...)
command: python -c import transformers, llm_engineering, torch; print(...)
NVIDIA H100
```

followed by the cluster's `JOB FEEDBACK` block with `State: COMPLETED (exit code 0)`. An error
message instead of the `NVIDIA H100` line after `command:` means the environment is not
working: send the log to the course staff.

**You are set up.** The repository's `README.md` lists the `scripts/run.sh` commands, and
each week's instructions, which arrive with that week's starter under `exercises/`, say
which ones to run.

---

## Everyday commands

| What | Command |
|---|---|
| Log in | `ssh tu_zxabc12@uc3.scc.kit.edu` (or `ssh uc3` after B3) |
| Go to your workspace | `cd "$(ws_find lme)"` |
| Days left on your workspace | `ws_list` |
| Extend your workspace | `ws_extend lme 60` |
| Submit a training run | `scripts/run.sh train configs/week-02.yaml` |
| Submit any command | `scripts/run.sh job -- <command>` |
| Check your submission | `scripts/run.sh test` (waits for the result, queue time included. `Ctrl-C` stops waiting, not the job) |
| List your jobs | `squeue --me` |
| When will a waiting job start? | `squeue --start` |
| Follow a running job's log | `tail -f logs/lme-job-<job id>.out` (stop with `Ctrl-C`) |
| Cancel a job | `scancel <job id>` |
| How did a job end? | `sacct -j <job id>` |
| Which queues have free nodes right now? | `sinfo_t_idle` |
| Copy results to your laptop (run on the laptop) | `rsync -av tu_zxabc12@uc3.scc.kit.edu:<path on cluster> .` |

**Queues.** `scripts/run.sh` submits to `gpu_h100_short` (one H100, up to 30 minutes) unless
you say otherwise. A run that needs longer goes to `gpu_h100`, but only when a week's
instructions say so, with the flags they give (for example
`--partition=gpu_h100 --time=01:30:00`). Ask for no more time than you need: short jobs start
sooner.

**This cluster's SLURM is restricted.** Users see only their own jobs (`squeue` and
`squeue --me` show the same list), and some standard commands are not available: `sinfo` answers `Access/permission denied`, so use `sinfo_t_idle`
instead. When a SLURM tutorial from elsewhere does not work here, check the wiki's
[Running Jobs](https://wiki.bwhpc.de/e/BwUniCluster3.0/Running_Jobs) page.

**Run tests and quick experiments on your laptop**, after `pip install -e ".[dev]"`. The
cluster is for GPU runs and the submission check.

---

## Troubleshooting

| What you see | What it means and what to do |
|---|---|
| `bwUniCluster 3.0` is missing on login.bwidm.de | The entitlement (A1) has not arrived. Check the entitlement link in A1. Write to <hpcmaster@uni-tuebingen.de> after two working days. |
| "Second factor missing" | Register a token (A3), then try again. |
| `ssh` hangs, then `Connection timed out` | You are not on the university network. Connect to eduVPN (B1). |
| `Permission denied` right after `Password:` | Use your **service password** (A4), not your ZDV password. Wait for a fresh OTP code and try again. If your phone's clock is wrong, codes fail: set it to automatic time. |
| `Permission denied` on the course directory, or `cannot read` from `run.sh setup` | Your account cannot read the course directory yet. Send your cluster username to the course staff. |
| Job stays `PD` for a long time | The queue is busy. `squeue --start` shows an estimated start time, and `sinfo_t_idle` shows which queues have free nodes. Do not submit the same job again. |
| `sacct` shows `TIMEOUT` | The job hit its time limit. Submit again with a longer `--time` (on `gpu_h100` if over 30 minutes and the instructions allow it). |
| `ssh -T git@github.com` says `Permission denied (publickey)` | The key from D1 is not on your GitHub account, or you added a different file. Repeat D1 steps 2 and 3. |
| Your workspace is gone | It expired. `ws_restore -l` lists expired workspaces that can still be restored for a short time. Create a new one with `ws_allocate lme 60`, then restore into it with `ws_restore <name from the list> lme`. |

## Where to get help

- **Course scripts, the course directory, anything in this guide:** the course staff.
- **Entitlement and university account:** ZDV HPC support, <hpcmaster@uni-tuebingen.de>.
- **The cluster itself** (login problems after registration, file systems, SLURM): the bwHPC
  ticket system, <https://wiki.bwhpc.de/e/BwSupportPortal>.
- **Reference:** <https://wiki.bwhpc.de/e/BwUniCluster3.0>, especially the pages *Login*,
  *Filesystem Details* and *Running Jobs*.
