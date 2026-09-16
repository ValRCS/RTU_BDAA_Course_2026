#!/usr/bin/env python3
"""SS.com sludinājumu rasmošanas komandrindas rīks.

Skripts ir veidots no kursa darba burtnīcas
06_04_ss_com_full_scraping_workflow.ipynb. Tas lejupielādē katru rezultātu
lapu ne vairāk kā vienu reizi, apvieno sludinājumus Pandas DataFrame un pēc
noklusējuma saglabā rezultātu gan CSV, gan XLSX formātā.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from datetime import datetime
from pathlib import Path
from time import sleep
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit


# DEFAULT_START_URL = "https://www.ss.com/en/real-estate/flats/riga/centre/sell/"
DEFAULT_START_URL = "https://www.ss.com/en/real-estate/flats/riga/bolderaya/sell/"
DEFAULT_DELAY = 0.5
DEFAULT_TIMEOUT = 20.0
DEFAULT_OUTPUT_DIR = Path("data")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RTU-BDAA-teaching-example/1.0)"
}

# Šie nosaukumi tiek aizpildīti pēc atkarību pārbaudes main() funkcijā.
requests = None
pd = None
BeautifulSoup = None


class ArgumentDefaultsRawHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    """Saglabā epilog rindas un vienlaikus rāda argumentu noklusējuma vērtības."""


def validate_ss_url(value: str) -> str:
    """Pārbauda, vai URL ir SS.com kategorijas pirmās rezultātu lapas adrese."""
    parsed = urlsplit(value.strip())
    hostname = (parsed.hostname or "").lower()

    if parsed.scheme not in {"http", "https"}:
        raise argparse.ArgumentTypeError("URL jāsākas ar http:// vai https://.")

    if hostname not in {"ss.com", "www.ss.com"}:
        raise argparse.ArgumentTypeError(
            "Atļautas tikai ss.com vai www.ss.com adreses."
        )

    path = parsed.path or "/"
    if "/msg/" in path:
        raise argparse.ArgumentTypeError(
            "Norādiet SS.com kategorijas rezultātu lapu, nevis viena "
            "sludinājuma /msg/ saiti."
        )

    if re.search(r"/page\d+\.html/?$", path):
        raise argparse.ArgumentTypeError(
            "Norādiet kategorijas pirmo lapu, nevis pageN.html lapošanas adresi."
        )

    parts = [part for part in path.split("/") if part]
    if parts and parts[0] in {"en", "lv", "ru"}:
        parts = parts[1:]

    if len(parts) < 3:
        raise argparse.ArgumentTypeError(
            "SS.com URL ceļš ir pārāk īss. Norādiet kategorijas rezultātu lapu, "
            "piemēram, /en/real-estate/flats/riga/centre/sell/."
        )

    return value.strip()


def non_negative_float(value: str) -> float:
    """Pārveido argumentu par nenegatīvu float vērtību."""
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Vērtībai jābūt skaitlim.") from exc

    if number < 0:
        raise argparse.ArgumentTypeError("Vērtība nedrīkst būt negatīva.")
    return number


def positive_float(value: str) -> float:
    """Pārveido argumentu par pozitīvu float vērtību."""
    number = non_negative_float(value)
    if number == 0:
        raise argparse.ArgumentTypeError("Vērtībai jābūt lielākai par 0.")
    return number


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    """Izveido un apstrādā komandrindas argumentus."""
    parser = argparse.ArgumentParser(
        description=(
            "Savāc SS.com kategorijas sludinājumus no visām rezultātu lapām "
            "un saglabā tos CSV/XLSX formātā."
        ),
        formatter_class=ArgumentDefaultsRawHelpFormatter,
        epilog=(
            "Piemēri:\n"
            "  python scripts/ss_com_scraper.py\n"
            "  python scripts/ss_com_scraper.py "
            "https://www.ss.com/en/real-estate/flats/riga/centre/hand_over/\n"
            "  python scripts/ss_com_scraper.py --delay 1.0 -o exports/centre\n"
            "  python scripts/ss_com_scraper.py --no-xlsx -o exports/centre.csv"
        ),
    )
    parser.add_argument(
        "url",
        nargs="?",
        default=DEFAULT_START_URL,
        type=validate_ss_url,
        help="SS.com kategorijas pirmās rezultātu lapas URL.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help=(
            "Izvades bāzes ceļš. Ja norādīts .csv vai .xlsx paplašinājums, "
            "tas tiek izmantots kā bāzes nosaukums un katram ieslēgtajam "
            "formātam pievienots atbilstošais paplašinājums."
        ),
    )
    parser.add_argument(
        "--delay",
        type=non_negative_float,
        default=DEFAULT_DELAY,
        help="Pauze sekundēs starp secīgiem HTTP pieprasījumiem.",
    )
    parser.add_argument(
        "--timeout",
        type=positive_float,
        default=DEFAULT_TIMEOUT,
        help="HTTP pieprasījuma timeout sekundēs.",
    )
    parser.add_argument(
        "--csv",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Saglabāt CSV failu (izslēgšanai lietojiet --no-csv).",
    )
    parser.add_argument(
        "--xlsx",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Saglabāt XLSX failu (izslēgšanai lietojiet --no-xlsx).",
    )

    args = parser.parse_args(argv)

    if not args.csv and not args.xlsx:
        parser.error("Jābūt ieslēgtam vismaz vienam formātam: --csv vai --xlsx.")

    return args


def check_dependencies(need_xlsx: bool = True) -> list[str]:
    """Atgriež trūkstošo trešo pušu pip pakotņu nosaukumus."""
    required = {
        "requests": "requests",
        "bs4": "beautifulsoup4",
        "pandas": "pandas",
        "lxml": "lxml",
    }
    if need_xlsx:
        required["openpyxl"] = "openpyxl"

    return [
        package
        for module, package in required.items()
        if importlib.util.find_spec(module) is None
    ]


def load_dependencies() -> None:
    """Importē trešo pušu bibliotēkas pēc veiksmīgas atkarību pārbaudes."""
    global requests, pd, BeautifulSoup

    import pandas as pandas_module
    import requests as requests_module
    from bs4 import BeautifulSoup as BeautifulSoupClass

    requests = requests_module
    pd = pandas_module
    BeautifulSoup = BeautifulSoupClass


def print_dependency_help(missing: list[str]) -> None:
    """Izdrukā saprotamas instalēšanas instrukcijas trūkstošām pakotnēm."""
    packages = " ".join(missing)
    print("Kļūda: trūkst nepieciešamo Python pakotņu:", file=sys.stderr)
    print("  " + ", ".join(missing), file=sys.stderr)
    print(file=sys.stderr)
    print("Instalējiet tās ar:", file=sys.stderr)
    print(f"  {sys.executable} -m pip install {packages}", file=sys.stderr)
    print(file=sys.stderr)
    print(
        "Vai instalējiet kursa pamata atkarības un pēc tam trūkstošās pakotnes:",
        file=sys.stderr,
    )
    print(f"  {sys.executable} -m pip install -r requirements.txt", file=sys.stderr)
    if "openpyxl" in missing:
        print(f"  {sys.executable} -m pip install openpyxl", file=sys.stderr)


def fetch_soup(url: str, timeout: float = DEFAULT_TIMEOUT) -> BeautifulSoup:
    """Lejupielādē vienu HTML lapu un atgriež BeautifulSoup objektu."""
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=timeout,
    )
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def process_headline(soup: BeautifulSoup) -> list[str]:
    """No SS.com tabulas galvenes iegūst rezultātu kolonnu nosaukumus."""
    headline = soup.find("tr", id="head_line")

    if headline is None:
        raise ValueError("Neizdevās atrast tabulas galveni ar id='head_line'.")

    header_cells = headline.find_all("td")
    page_columns = [cell.get_text(" ", strip=True) for cell in header_cells[1:]]

    return ["description", "url", *page_columns]


def find_ad_rows(soup: BeautifulSoup) -> list:
    """Atrod SS.com rezultātu tabulas rindas, kas reprezentē sludinājumus."""
    rows = soup.find_all("tr")

    return [
        row
        for row in rows
        if row.get("id", "").startswith("tr_")
        and not row.get("id", "").startswith("tr_bnr")
    ]


def process_ad_row(row, columns: list[str]) -> dict:
    """Pārvērš vienu SS.com sludinājuma HTML rindas elementu par vārdnīcu."""
    cells = row.find_all("td")

    if len(cells) < 3:
        return {}

    link = row.find("a", href=True)
    if link is None:
        return {}

    ad = {
        "description": cells[2].get_text(" ", strip=True),
        "url": urljoin("https://www.ss.com", link["href"]),
    }

    for cell, column in zip(cells[3:], columns[2:]):
        ad[column] = cell.get_text(" ", strip=True)

    return ad


def process_all_ads(soup: BeautifulSoup, columns: list[str]) -> list[dict]:
    """Apstrādā visas vienas SS.com rezultātu lapas sludinājumu rindas."""
    ads = []

    for row in find_ad_rows(soup):
        ad = process_ad_row(row, columns)
        if ad:
            ads.append(ad)

    return ads


def process_page(soup: BeautifulSoup) -> pd.DataFrame:
    """Pārvērš vienas jau lejupielādētas SS.com lapas HTML par DataFrame."""
    columns = process_headline(soup)
    ads = process_all_ads(soup, columns)
    return pd.DataFrame(ads, columns=columns)


def get_last_page_number(soup: BeautifulSoup) -> int:
    """No SS.com lapošanas saitēm nosaka pēdējās rezultātu lapas numuru."""
    page_numbers = []

    previous_link = soup.find("a", rel="prev")
    if previous_link and previous_link.get("href"):
        match = re.search(
            r"(?:^|/)page(\d+)\.html(?:$|[?#])",
            previous_link["href"],
        )
        if match:
            page_numbers.append(int(match.group(1)))

    for anchor in soup.find_all("a", href=True):
        match = re.search(
            r"(?:^|/)page(\d+)\.html(?:$|[?#])",
            anchor["href"],
        )
        if match:
            page_numbers.append(int(match.group(1)))

    return max(page_numbers, default=1)


def get_all_page_urls(start_url: str, first_soup: BeautifulSoup) -> list[str]:
    """Izveido visu kategorijas rezultātu lapu URL bez papildu HTTP pieprasījuma."""
    last_page = get_last_page_number(first_soup)

    if last_page == 1:
        return [start_url]

    parsed = urlsplit(start_url)
    base_path = re.sub(r"/page\d+\.html$", "", parsed.path.rstrip("/"))
    base_path = base_path.rstrip("/") + "/"

    urls = [start_url]

    for page_number in range(2, last_page + 1):
        page_path = f"{base_path}page{page_number}.html"
        page_url = urlunsplit(
            (
                parsed.scheme,
                parsed.netloc,
                page_path,
                parsed.query,
                "",
            )
        )
        urls.append(page_url)

    return urls


def process_all_pages(
    start_url: str,
    delay: float = DEFAULT_DELAY,
    timeout: float = DEFAULT_TIMEOUT,
) -> pd.DataFrame:
    """Lejupielādē katru rezultātu lapu vienu reizi un apvieno sludinājumus."""
    first_soup = fetch_soup(start_url, timeout=timeout)
    page_urls = get_all_page_urls(start_url, first_soup)

    print(f"Atrastas {len(page_urls)} rezultātu lapas.")

    first_df = process_page(first_soup)
    dataframes = [first_df]
    print(f"1/{len(page_urls)}: {len(first_df)} sludinājumi")

    for page_number, url in enumerate(page_urls[1:], start=2):
        sleep(delay)
        soup = fetch_soup(url, timeout=timeout)
        page_df = process_page(soup)
        dataframes.append(page_df)
        print(f"{page_number}/{len(page_urls)}: {len(page_df)} sludinājumi")

    result = pd.concat(dataframes, ignore_index=True)

    if "url" in result.columns:
        result = result.drop_duplicates(subset="url").reset_index(drop=True)

    return result


def parse_url_metadata(start_url: str) -> dict:
    """No SS.com URL iegūst valodu, kategoriju, kontekstu un darījuma tipu."""
    parsed = urlsplit(start_url)

    parts = [
        unquote(part).strip().lower()
        for part in parsed.path.split("/")
        if part.strip()
    ]

    if parts and re.fullmatch(r"page\d+\.html", parts[-1]):
        parts.pop()

    language = "unknown"
    if parts and parts[0] in {"en", "lv", "ru"}:
        language = parts.pop(0)

    if len(parts) < 3:
        raise ValueError(
            "START_URL ceļā nav pietiekami daudz daļu, lai noteiktu kategoriju "
            "un darījuma tipu."
        )

    section = parts[0]
    category = parts[1]
    transaction_raw = parts[-1]
    context = parts[2:-1]

    transaction_aliases = {
        "hand_over": "rent",
        "sell": "sell",
        "buy": "buy",
        "rent": "rent",
        "exchange": "exchange",
    }
    transaction = transaction_aliases.get(transaction_raw, transaction_raw)

    safe_context = [
        re.sub(r"[^a-z0-9_-]+", "_", part).strip("_") for part in context
    ]

    return {
        "language": language,
        "section": section,
        "category": category,
        "context": [part for part in safe_context if part],
        "transaction": transaction,
        "transaction_raw": transaction_raw,
    }


def build_output_paths(
    start_url: str,
    output: Path | None = None,
    save_csv: bool = True,
    save_xlsx: bool = True,
) -> dict[str, Path]:
    """Izveido CSV/XLSX ceļus no URL metadatiem vai lietotāja -o ceļa."""
    if output is None:
        metadata = parse_url_metadata(start_url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_parts = [
            "ss",
            metadata["category"],
            *metadata["context"],
            metadata["transaction"],
            timestamp,
        ]
        file_stem = "_".join(part for part in name_parts if part)
        base_path = DEFAULT_OUTPUT_DIR / file_stem
    else:
        output = Path(output)
        if output.suffix.lower() in {".csv", ".xlsx"}:
            base_path = output.with_suffix("")
        else:
            base_path = output

    paths = {}
    if save_csv:
        paths["csv"] = Path(str(base_path) + ".csv")
    if save_xlsx:
        paths["xlsx"] = Path(str(base_path) + ".xlsx")
    return paths


def save_results(df: pd.DataFrame, paths: dict[str, Path]) -> None:
    """Saglabā DataFrame izvēlētajos CSV un/vai XLSX failos."""
    for path in paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)

    if "csv" in paths:
        df.to_csv(paths["csv"], index=False, encoding="utf-8-sig")

    if "xlsx" in paths:
        df.to_excel(paths["xlsx"], index=False, engine="openpyxl")


def run_scraping_workflow(
    start_url: str,
    delay: float = DEFAULT_DELAY,
    timeout: float = DEFAULT_TIMEOUT,
    output: Path | None = None,
    save_csv: bool = True,
    save_xlsx: bool = True,
) -> pd.DataFrame:
    """Izpilda pilnu SS.com rasmošanas, apvienošanas un saglabāšanas plūsmu."""
    started_at = datetime.now()

    print("Sākam SS.com datu ieguvi:")
    print(start_url)
    print(f"Pauze starp pieprasījumiem: {delay} s")
    print()

    df = process_all_pages(
        start_url,
        delay=delay,
        timeout=timeout,
    )

    paths = build_output_paths(
        start_url,
        output=output,
        save_csv=save_csv,
        save_xlsx=save_xlsx,
    )
    save_results(df, paths)

    elapsed = (datetime.now() - started_at).total_seconds()

    print()
    print(f"Savākti {len(df):,} unikāli sludinājumi.")
    for format_name, path in paths.items():
        print(f"{format_name.upper():5}: {path}")
    print(f"Izpildes ilgums: {elapsed:.1f} s")

    return df


def main(argv: list[str] | None = None) -> int:
    """Komandrindas ieejas punkts; atgriež procesa exit kodu."""
    args = parse_arguments(argv)

    missing = check_dependencies(need_xlsx=args.xlsx)
    if missing:
        print_dependency_help(missing)
        return 2

    load_dependencies()

    try:
        run_scraping_workflow(
            args.url,
            delay=args.delay,
            timeout=args.timeout,
            output=args.output,
            save_csv=args.csv,
            save_xlsx=args.xlsx,
        )
    except KeyboardInterrupt:
        print("\nDatu ieguve pārtraukta ar Ctrl+C.", file=sys.stderr)
        return 130
    except requests.RequestException as exc:
        print(f"HTTP kļūda: {exc}", file=sys.stderr)
        return 1
    except (ValueError, OSError) as exc:
        print(f"Kļūda: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
