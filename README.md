# RTU_BDAA_Course_2026

Business Data Processing Automatization course - RTU VIAA DAS.LV fall 2026.

## Course Page in Latvian - requires authorization

https://www.das.lv/platforma/course/view.php?id=39

## Jupyter darba burtnīcas

Kursa Jupyter darba burtnīcas var darbināt lokāli **VS Code / Jupyter** vidē vai tieši **Google Colab**. Zemāk ir visas pašlaik repozitorijā pieejamās darba burtnīcas.

### 6. tēma — datu ieguve no tīmekļa (Web Scraping)

#### 6.01 — Tīmekļa rasmošanas atkārtojums

Īss praktisks atkārtojums par HTTP pieprasījumiem ar `requests`, HTML parsēšanu ar `BeautifulSoup`, `find()` / `find_all()`, HTML atribūtiem, CSS selektoriem, vairāku lapu apstrādi, datu pārveidošanu par `pandas.DataFrame` un CSV saglabāšanu. Mācību piemēros izmantota scraping vingrinājumiem paredzētā vietne `quotes.toscrape.com`.

[Atvērt notebook GitHub](notebooks/lecture_06_web_scraping/06_01_web_scraping_refresher.ipynb)

[![Atvērt Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ValRCS/RTU_BDAA_Course_2026/blob/main/notebooks/lecture_06_web_scraping/06_01_web_scraping_refresher.ipynb)

#### 6.02 — SS.com dzīvokļu sludinājumu rasmošana

Reālāks biznesa datu ieguves piemērs ar SS.com dzīvokļu sludinājumiem: HTTP un HTML tabulas, `pandas.read_html()`, sludinājumu saišu atrašana ar `BeautifulSoup`, neliela cenu un platību normalizācija un rezultātu saglabāšana CSV formātā turpmākai analīzei.

[Atvērt notebook GitHub](notebooks/lecture_06_web_scraping/06_02_apartment_scraping.ipynb)

[![Atvērt Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ValRCS/RTU_BDAA_Course_2026/blob/main/notebooks/lecture_06_web_scraping/06_02_apartment_scraping.ipynb)

#### 6.03 — SS.com sludinājumu dziļās saites

Paplašina SS.com rasmošanu ārpus `pandas.read_html()`: ar `requests` un `BeautifulSoup` tiek analizēta lapas HTML struktūra, atrastas rezultātu rindas un iegūtas pilnās saites uz konkrētiem sludinājumiem. Notebook parāda, kā no tabulas skata nonākt līdz strukturētiem ierakstiem ar URL.

[Atvērt notebook GitHub](notebooks/lecture_06_web_scraping/06_03_web_scraping_apartment_links.ipynb)

[![Atvērt Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ValRCS/RTU_BDAA_Course_2026/blob/main/notebooks/lecture_06_web_scraping/06_03_web_scraping_apartment_links.ipynb)

#### 6.04 — Pilna SS.com rasmošanas plūsma ar funkcijām

Pilns **Run All** funkcijās sadalīts rasmošanas risinājums. HTTP pieprasījumi ir nodalīti no HTML apstrādes, pirmā lapa tiek pieprasīta tikai vienu reizi, automātiski tiek noteiktas visas lapošanas adreses, apstrādāti visu lapu sludinājumi un rezultāts saglabāts gan CSV, gan XLSX failā ar kategoriju, darījuma tipu un laiku faila nosaukumā.

[Atvērt notebook GitHub](notebooks/lecture_06_web_scraping/06_04_ss_com_full_scraping_workflow.ipynb)

[![Atvērt Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ValRCS/RTU_BDAA_Course_2026/blob/main/notebooks/lecture_06_web_scraping/06_04_ss_com_full_scraping_workflow.ipynb)

### 7. tēma — datu analīze un vizualizācija

#### 7.01 — Datu analīze un vizualizācija ar Pandas un Matplotlib

Turpina SS.com projektu no iegūtā CSV līdz analīzei: datu kvalitātes pārbaude, kolonnu pārdēvēšana un tipu konvertēšana, cenu un stāvu tīrīšana, jaunu pazīmju veidošana, filtrēšana un kārtošana, `groupby()` / `agg()`, aprakstošā statistika un vizualizācijas ar Matplotlib, tostarp histogrammas, stabiņu diagrammas, scatter plot un boxplot.

[Atvērt notebook GitHub](notebooks/lecture_07_data_analysis_visualization/07_data_analysis_visualization.ipynb)

[![Atvērt Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ValRCS/RTU_BDAA_Course_2026/blob/main/notebooks/lecture_07_data_analysis_visualization/07_data_analysis_visualization.ipynb)

## Running notebooks locally

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

The repository contains a [`requirements.txt`](requirements.txt) file with the core Python packages needed for the Lecture 6 notebooks.

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

This installs Jupyter/IPython kernel support together with `requests`, `beautifulsoup4`, `pandas`, and `lxml`.

You normally need to run the requirements installation only once for a given virtual environment. If `requirements.txt` is updated later in the course, run the same command again.

The notebooks also contain setup checks that install their additional runtime packages when needed, which is useful in Google Colab or when a package is missing locally.

### 5. Open the repository in VS Code

From the repository folder you can run:

```bash
code .
```

Or open the folder manually using **File → Open Folder** in VS Code.

### 6. Open a notebook and select the Python kernel

Current notebooks:

```text
notebooks/lecture_06_web_scraping/06_01_web_scraping_refresher.ipynb
notebooks/lecture_06_web_scraping/06_02_apartment_scraping.ipynb
notebooks/lecture_06_web_scraping/06_03_web_scraping_apartment_links.ipynb
notebooks/lecture_06_web_scraping/06_04_ss_com_full_scraping_workflow.ipynb
notebooks/lecture_07_data_analysis_visualization/07_data_analysis_visualization.ipynb
```

In the upper-right corner of the notebook editor choose **Select Kernel** and select the Python interpreter you want to use. If you created `.venv`, choose the interpreter from that environment.

Then run the cells from top to bottom using **Run All** or execute them one at a time with `Shift+Enter`.

## Running in Google Colab

No local Python installation is required. Click the **Atvērt Google Colab** badge next to the relevant notebook above, then run the cells from top to bottom.

Colab runs on a temporary cloud environment, so files created by a notebook disappear when the Colab session is deleted unless you download them or save them to Google Drive.
