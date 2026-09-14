# RTU_BDAA_Course_2026

Business Data Processing Automatization course - RTU VIAA DAS.LV fall 2026.

## Course Page in Latvian - requires authorization

https://www.das.lv/platforma/course/view.php?id=39

## Lecture 6 — Web Scraping

Lecture 6 uses Jupyter Notebooks. They can be run either locally in **VS Code** or directly in **Google Colab**.

### Notebooks

#### 6.01 — Web Scraping Refresher

Refreshes the basic workflow with `requests`, `BeautifulSoup`, HTML elements and attributes, CSS selectors, pagination, `pandas.DataFrame`, and CSV export.

[Open notebook on GitHub](notebooks/lecture_06_web_scraping/06_01_web_scraping_refresher.ipynb)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ValRCS/RTU_BDAA_Course_2026/blob/main/notebooks/lecture_06_web_scraping/06_01_web_scraping_refresher.ipynb)

#### 6.02 — Apartment Scraping

Applies the scraping workflow to apartment listings and turns the extracted information into tabular data suitable for later analysis.

[Open notebook on GitHub](notebooks/lecture_06_web_scraping/06_02_apartment_scraping.ipynb)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ValRCS/RTU_BDAA_Course_2026/blob/main/notebooks/lecture_06_web_scraping/06_02_apartment_scraping.ipynb)

## Running Lecture 6 notebooks locally

### 1. Install the required software

Install:

- [Python 3](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/)
- the **Python** extension for VS Code
- the **Jupyter** extension for VS Code
- [Git](https://git-scm.com/) if you want to clone the repository with Git

### 2. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/ValRCS/RTU_BDAA_Course_2026.git
cd RTU_BDAA_Course_2026
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

### 3. Recommended: create a virtual environment

Creating a separate Python environment keeps the course packages isolated from the rest of your Python installation.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If `python` is not recognized on Windows, try `py` instead.

### 4. Install the course requirements

The repository contains a [`requirements.txt`](requirements.txt) file with the Python packages needed for the current notebooks.

First, optionally update `pip`:

```bash
python -m pip install --upgrade pip
```

Then install all required packages:

```bash
python -m pip install -r requirements.txt
```

On Windows, if you use the `py` launcher instead of `python`, run:

```powershell
py -m pip install -r requirements.txt
```

For Lecture 6 this installs Jupyter/IPython kernel support together with `requests`, `beautifulsoup4`, `pandas`, and `lxml`.

You normally need to run the requirements installation only once for a given virtual environment. If `requirements.txt` is updated later in the course, run the same command again.

The notebooks also contain a small setup check for their main runtime packages, which is useful in Google Colab or when a package is missing locally.

### 5. Open the repository in VS Code

From the repository folder you can run:

```bash
code .
```

Or open the folder manually using **File → Open Folder** in VS Code.

### 6. Open a notebook and select the Python kernel

Open one of these files:

```text
notebooks/lecture_06_web_scraping/06_01_web_scraping_refresher.ipynb
notebooks/lecture_06_web_scraping/06_02_apartment_scraping.ipynb
```

In the upper-right corner of the notebook editor choose **Select Kernel** and select the Python interpreter you want to use. If you created `.venv`, choose the interpreter from that environment.

Then run the cells from top to bottom using **Run All** or execute them one at a time with `Shift+Enter`.

## Running in Google Colab

No local Python installation is required. Click the **Open in Colab** badge next to the notebook above, then run the cells from top to bottom.

Colab runs on a temporary cloud environment, so files created by a notebook disappear when the Colab session is deleted unless you download them or save them to Google Drive.
