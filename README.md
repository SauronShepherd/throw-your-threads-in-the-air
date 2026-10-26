# Throw Your Threads in the Air — Spark/PySpark Concurrency Labs

Companion project for the Apache Spark WTF article **“When Threads Go Bump in the Night”**. Eleven guided Jupyter notebooks explain the labs, expected observations, and why each result matters.

## Runtime baseline

- Apache Spark / PySpark **4.2.0** (pinned in `requirements.txt`)
- Python **3.10 or newer**; notebooks were designed for Python 3.13 as well
- Java **17, 21, or 25** for Spark 4.2.0. Use a full JDK, not only a JRE: notebook 02 needs `jcmd`; notebooks 03 and 08 need `javac` and JDK 21+ for virtual threads.
- Jupyter Notebook or JupyterLab

Spark 4.2.0's official docs: [release](https://spark.apache.org/releases/spark-release-4-2-0), [overview and supported runtimes](https://spark.apache.org/docs/4.2.0/), [PySpark install](https://spark.apache.org/docs/4.2.0/api/python/getting_started/install.html).

## Quick start

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install jupyterlab
jupyter lab
```

Open a notebook in `notebooks/` and run cells in order. Local Spark sessions use small datasets. Most use `local[2]`; notebook 07 uses `local[2,2]` so the deliberately failing task can be retried. Labs that inspect OS/cgroup state report “not available” on unsupported platforms. Do not run resource-exhaustion experiments on shared or production clusters.

## Notebook map

| # | Lab | Article subsection | Main idea |
|---|---|---|---|
| 01 | [The Cast: Driver, Executor, Task, Worker](notebooks/01-the-cast-driver-executor-worker.ipynb) | 1.1 | JVM SQL vs Python workers |
| 02 | [Find the Pool by Its Job](notebooks/02-find-the-pool-by-its-job.ipynb) | 1.2 | Thread dumps and pool roles |
| 03 | [Java Platform Threads and Virtual Threads](notebooks/03-java-platform-and-virtual-threads.ipynb) | 2.1 | JDK platform threads vs Loom |
| 04 | [Python Threads, the GIL and Processes](notebooks/04-python-gil-and-processes.ipynb) | 2.2 | I/O, CPU and process parallelism |
| 05 | [Classify the OOM Without Summoning One](notebooks/05-classify-the-oom.ipynb) | 3.1 | Heap, native, worker and cgroup evidence |
| 06 | [Cancellation Is a Request](notebooks/06-cancellation-is-a-request.ipynb) | 3.2 | Cancellation signal vs termination |
| 07 | [Retries, Attempts and Idempotency](notebooks/07-retries-and-idempotency.ipynb) | 3.3 | Physical retries and side effects |
| 08 | [Loom: Prototype One Blocking Component](notebooks/08-loom-virtual-threads.ipynb) | 4.2 | Evaluate a narrow Loom use case |
| 09 | [Build an Incident Card](notebooks/09-incident-card.ipynb) | 5.1 | Capture versions, topology and budgets |
| 10 | [Draw the Boundary, Not the Buzzword](notebooks/10-draw-the-boundary-not-the-buzzword.ipynb) | 5.2 | Make accurate technical metaphors |
| 11 | [Review the Five Halloween Image Concepts](notebooks/11-visual-metaphor-review.ipynb) | 5.2 | Turn image ideas into teaching aids |

## Safety and interpretation

- The OOM lab observes existing limits; it does not intentionally exhaust heap, memory or PIDs.
- The retry lab records task attempt metadata and writes duplicate rows only to a disposable local file. It does not contact external systems.
- The thread dump lab uses `jcmd` only against a process you own or are authorized to inspect.
- Thread counts, RSS/PSS, JVM heap, Native Memory Tracking and cgroup totals have different scopes. Read the notebook caveats before interpreting them.
- Spark retries and speculation can repeat physical work; arbitrary side effects need an idempotent or transactional sink.
- Loom does not automatically convert Spark's existing pools to virtual threads.

## Validate notebooks

The checked-in `.ipynb` files are the canonical teaching artifacts. Validate notebook structure and Python cell syntax with:

```bash
python scripts/validate_notebooks.py
```
