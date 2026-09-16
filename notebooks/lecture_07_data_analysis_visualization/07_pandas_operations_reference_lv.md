# Tipiskās Pandas operācijas

Šis materiāls ir praktiska atsauce biežāk lietotajām `pandas` operācijām. Mērķis nav uzskaitīt visu Pandas API, bet parādīt darba paņēmienus, kas visbiežāk vajadzīgi tabulāru biznesa datu analīzē.

Piemēros pieņemam, ka dati atrodas `DataFrame` objektā ar nosaukumu `df`.

---

## 1. Importēšana

```python
import pandas as pd
```

Parasti pietiek ar standarta saīsinājumu `pd`.

---

## 2. CSV faila ielāde

```python
df = pd.read_csv("data.csv")
```

No tīmekļa URL:

```python
df = pd.read_csv("https://example.com/data.csv")
```

Bieži noder parametri:

```python
df = pd.read_csv(
    "data.csv",
    encoding="utf-8",
    sep=",",
)
```

Ja datums jāielasa kā datums:

```python
df = pd.read_csv(
    "data.csv",
    parse_dates=["date"],
)
```

---

## 3. Excel faila ielāde

```python
df = pd.read_excel("data.xlsx")
```

Konkrēta lapa:

```python
df = pd.read_excel(
    "data.xlsx",
    sheet_name="Sales",
)
```

---

## 4. Pirmā datu apskate

```python
df.head()
```

```python
df.tail()
```

Nejauša izlase:

```python
df.sample(5)
```

Izmērs:

```python
df.shape
```

Kolonnu nosaukumi:

```python
df.columns
```

Datu tipu un `NaN` pārskats:

```python
df.info()
```

---

## 5. Aprakstošā statistika

Skaitliskām kolonnām:

```python
df.describe()
```

Arī teksta un kategoriskajām kolonnām:

```python
df.describe(include="all")
```

Vienai kolonnai:

```python
df["price_eur"].describe()
```

---

## 6. Vienas kolonnas izvēle

```python
prices = df["price_eur"]
```

Rezultāts ir `Series` objekts.

Alternatīva:

```python
prices = df.price_eur
```

Praksē drošāk un universālāk ir izmantot kvadrātiekavas, jo tās strādā arī ar kolonnu nosaukumiem, kuros ir atstarpes vai speciālie simboli.

---

## 7. Vairāku kolonnu izvēle

```python
subset = df[["street", "rooms", "area_m2", "price_eur"]]
```

Svarīgi: ārējās kvadrātiekavas izvēlas no `DataFrame`, bet iekšējais saraksts norāda kolonnu nosaukumus.

---

## 8. Rindu atlase ar nosacījumu

```python
cheap = df[df["price_eur"] < 500]
```

Divi nosacījumi:

```python
result = df[
    (df["rooms"] == 2) &
    (df["price_eur"] <= 700)
]
```

`AND` operatoram Pandas nosacījumos izmanto `&`, nevis `and`.

`OR`:

```python
result = df[
    (df["rooms"] == 1) |
    (df["rooms"] == 2)
]
```

Negācija:

```python
result = df[~(df["price_period"] == "day")]
```

---

## 9. `isin()` vairākiem iespējamiem variantiem

```python
result = df[df["rooms"].isin([1, 2, 3])]
```

Teksta kategorijām:

```python
result = df[
    df["building_series"].isin([
        "New",
        "Recon.",
        "Pre-war house",
    ])
]
```

Pretējais variants:

```python
result = df[~df["rooms"].isin([1, 2])]
```

---

## 10. `loc` — atlase pēc etiķetēm un nosacījumiem

```python
result = df.loc[
    df["price_eur"] < 500,
    ["street", "rooms", "price_eur"]
]
```

`loc` ir īpaši noderīgs, ja vienlaikus vēlamies atlasīt rindas un kolonnas.

Vērtību maiņa:

```python
df.loc[df["price_eur"] < 0, "price_eur"] = pd.NA
```

---

## 11. `iloc` — atlase pēc pozīcijām

Pirmās piecas rindas:

```python
df.iloc[:5]
```

Pirmās piecas rindas un pirmās trīs kolonnas:

```python
df.iloc[:5, :3]
```

Konkrēta šūna:

```python
df.iloc[0, 0]
```

`iloc` izmanto indeksu pozīcijas, nevis kolonnu vai rindu etiķetes.

---

## 12. Kārtošana

Augoši:

```python
df.sort_values("price_eur")
```

Dilstoši:

```python
df.sort_values(
    "price_eur",
    ascending=False,
)
```

Pēc vairākām kolonnām:

```python
df.sort_values(
    ["rooms", "price_eur"],
    ascending=[True, True],
)
```

---

## 13. Indeksa pārnumurēšana

Pēc filtrēšanas vai kārtošanas indekss var kļūt neregulārs.

```python
df = df.reset_index(drop=True)
```

`drop=True` nozīmē, ka vecais indekss netiks saglabāts kā jauna kolonna.

---

## 14. Jaunas kolonnas izveide

```python
df["price_per_room"] = (
    df["price_eur"] / df["rooms"]
)
```

Boolean kolonna:

```python
df["is_expensive"] = df["price_eur"] > 1000
```

Teksta kolonnas transformācija:

```python
df["street_upper"] = df["street"].str.upper()
```

---

## 15. Kolonnu pārdēvēšana

```python
df = df.rename(columns={
    "R.": "rooms",
    "m²": "area_m2",
    "Price": "price_raw",
})
```

Lielākiem projektiem ir vērts kolonnu nosaukumus normalizēt jau analīzes sākumā.

---

## 16. Kolonnas dzēšana

```python
df = df.drop(columns=["temporary_column"])
```

Vairākas kolonnas:

```python
df = df.drop(columns=["a", "b", "c"])
```

---

## 17. Trūkstošo vērtību pārbaude

```python
df.isna()
```

Kopsavilkums pa kolonnām:

```python
df.isna().sum()
```

Procentuāli:

```python
(df.isna().mean() * 100).round(1)
```

---

## 18. Rindu izmešana ar `NaN`

```python
clean = df.dropna()
```

Tikai tad, ja konkrētās kolonnas trūkst:

```python
clean = df.dropna(
    subset=["price_eur", "area_m2"]
)
```

Nevajag automātiski izmantot `dropna()` visai tabulai, jo tā var izdzēst pārāk daudz derīgu rindu.

---

## 19. Trūkstošo vērtību aizpildīšana

Ar konstanti:

```python
df["building_series"] = (
    df["building_series"]
    .fillna("Unknown")
)
```

Ar mediānu:

```python
median_area = df["area_m2"].median()
df["area_m2"] = df["area_m2"].fillna(median_area)
```

Aizvietošanas metode ir analītisks lēmums, nevis tikai tehniska darbība.

---

## 20. Datu tipu pārbaude

```python
df.dtypes
```

Konkrēta kolonna:

```python
df["rooms"].dtype
```

---

## 21. Datu tipu konvertēšana

Uz veselu skaitli:

```python
df["rooms"] = df["rooms"].astype(int)
```

Drošāks variants netīriem datiem:

```python
df["rooms"] = pd.to_numeric(
    df["rooms"],
    errors="coerce",
)
```

`errors="coerce"` nekorektas vērtības pārvērš par `NaN`.

---

## 22. Darbs ar tekstu: `.str`

Mazie burti:

```python
df["street"] = df["street"].str.lower()
```

Atstarpju noņemšana:

```python
df["street"] = df["street"].str.strip()
```

Teksta aizvietošana:

```python
df["price_clean"] = (
    df["price_raw"]
    .str.replace("€", "", regex=False)
    .str.strip()
)
```

Teksta meklēšana:

```python
mask = df["description"].str.contains(
    "balkon",
    case=False,
    na=False,
)

with_balcony = df[mask]
```

---

## 23. Teksta sadalīšana

Ja kolonnā ir:

```text
4/8
```

var sadalīt divās daļās:

```python
parts = df["floor"].str.split(
    "/",
    expand=True,
)

parts.head()
```

Pēc tam:

```python
df["floor_number"] = pd.to_numeric(
    parts[0],
    errors="coerce",
)

df["building_floors"] = pd.to_numeric(
    parts[1],
    errors="coerce",
)
```

---

## 24. Regulārās izteiksmes ar `str.extract()`

No cenas teksta:

```text
1,800 €/mon.
```

var izvilkt skaitlisko daļu:

```python
numeric_text = df["price_raw"].str.extract(
    r"([\d,.]+)",
    expand=False,
)
```

Pēc tam noņemt tūkstošu atdalītāju:

```python
numeric_text = numeric_text.str.replace(
    ",",
    "",
    regex=False,
)
```

un konvertēt:

```python
df["price_eur"] = pd.to_numeric(
    numeric_text,
    errors="coerce",
)
```

---

## 25. Unikālās vērtības

```python
df["building_series"].unique()
```

Unikālo vērtību skaits:

```python
df["building_series"].nunique()
```

Tas ir ļoti noderīgi, lai pamanītu nekonsekventas kategorijas, piemēram:

```text
New
new
New 
NEW
```

---

## 26. `value_counts()`

```python
df["building_series"].value_counts()
```

Arī `NaN` vērtības:

```python
df["building_series"].value_counts(
    dropna=False
)
```

Proporcijas:

```python
df["building_series"].value_counts(
    normalize=True
)
```

---

## 27. Dublikātu meklēšana

Pilnīgi identiskas rindas:

```python
df.duplicated().sum()
```

Pēc URL:

```python
df.duplicated(subset="url").sum()
```

Apskatīt dublikātus:

```python
duplicates = df[
    df.duplicated(
        subset="url",
        keep=False,
    )
]
```

---

## 28. Dublikātu noņemšana

```python
df = df.drop_duplicates()
```

Pēc konkrētas kolonnas:

```python
df = df.drop_duplicates(
    subset="url"
)
```

Saglabāt pēdējo ierakstu:

```python
df = df.drop_duplicates(
    subset="url",
    keep="last",
)
```

---

## 29. Pamata statistiskās funkcijas

```python
df["price_eur"].count()
df["price_eur"].min()
df["price_eur"].max()
df["price_eur"].mean()
df["price_eur"].median()
df["price_eur"].std()
df["price_eur"].sum()
```

Kvartiles:

```python
df["price_eur"].quantile([0.25, 0.5, 0.75])
```

---

## 30. `nlargest()` un `nsmallest()`

Pieci dārgākie:

```python
df.nlargest(5, "price_eur")
```

Pieci lētākie:

```python
df.nsmallest(5, "price_eur")
```

Tas bieži ir ērtāk nekā `sort_values(...).head()`.

---

## 31. Grupēšana ar `groupby()`

Vidējā cena pēc istabu skaita:

```python
df.groupby("rooms")["price_eur"].mean()
```

Mediāna:

```python
df.groupby("rooms")["price_eur"].median()
```

Vairākas kolonnas:

```python
df.groupby("rooms")[[
    "price_eur",
    "area_m2",
]].mean()
```

`groupby()` pamatideju bieži apraksta kā:

```text
split → apply → combine
```

1. sadala datus grupās;
2. katrai grupai izpilda operāciju;
3. rezultātus apvieno.

---

## 32. Vairāku statistiku aprēķins ar `agg()`

```python
stats = (
    df.groupby("rooms")
      .agg(
          listings=("url", "count"),
          mean_price=("price_eur", "mean"),
          median_price=("price_eur", "median"),
          mean_area=("area_m2", "mean"),
      )
)
```

Šī forma ir īpaši ērta, jo gala kolonnu nosaukumus norādām paši.

---

## 33. Grupēšana pēc vairākām kolonnām

```python
stats = (
    df.groupby([
        "rooms",
        "building_series",
    ])["price_eur"]
    .median()
)
```

Rezultātam būs vairāku līmeņu indekss (`MultiIndex`).

Parastam `DataFrame`:

```python
stats = stats.reset_index()
```

---

## 34. `transform()` — grupas statistiku atgriež katrai rindai

Pieņemsim, ka vēlamies katram dzīvoklim zināt attiecīgās istabu grupas mediānas cenu:

```python
df["room_median_price"] = (
    df.groupby("rooms")["price_eur"]
      .transform("median")
)
```

Tad var aprēķināt novirzi:

```python
df["difference_from_room_median"] = (
    df["price_eur"] -
    df["room_median_price"]
)
```

`transform()` atšķiras no `agg()` ar to, ka rezultāts saglabā sākotnējo rindu skaitu.

---

## 35. `query()` kā alternatīva filtrēšanai

```python
result = df.query(
    "rooms == 2 and price_eur <= 700"
)
```

Tas var būt labi salasāms vienkāršiem nosacījumiem.

Tradicionālā forma:

```python
result = df[
    (df["rooms"] == 2) &
    (df["price_eur"] <= 700)
]
```

Abas pieejas ir korektas.

---

## 36. `assign()` jaunu kolonnu izveidei

```python
result = df.assign(
    price_per_room=(
        df["price_eur"] / df["rooms"]
    )
)
```

Īpaši ērti metožu ķēdēs.

---

## 37. Metožu ķēdes

Pandas bieži raksta kā secīgu transformāciju plūsmu:

```python
result = (
    df
    .dropna(subset=["price_eur"])
    .query("price_period == 'month'")
    .sort_values("price_eur")
    .reset_index(drop=True)
)
```

Priekšrocības:

- labi redzama transformāciju secība;
- nav nepieciešami daudzi pagaidu mainīgie;
- kods atgādina datu apstrādes cauruļvadu.

Tomēr pārāk gara ķēde var kļūt grūti atkļūdojama. Sarežģītu procesu ir vērts sadalīt loģiskos posmos.

---

## 38. Kopijas un `SettingWithCopy`

Pēc filtrēšanas, ja plānojam mainīt rezultātu, droši izveidot kopiju:

```python
monthly = df[
    df["price_period"] == "month"
].copy()
```

Tad:

```python
monthly["price_per_room"] = (
    monthly["price_eur"] /
    monthly["rooms"]
)
```

`.copy()` skaidri pasaka, ka jaunais `DataFrame` jāapstrādā neatkarīgi no sākotnējā.

---

## 39. Datumu konvertēšana

```python
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce",
)
```

Pēc tam pieejams `.dt`:

```python
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["weekday"] = df["date"].dt.day_name()
```

---

## 40. Kategoriskais datu tips

Ja kolonnā atkārtojas neliels kategoriju skaits:

```python
df["building_series"] = (
    df["building_series"]
    .astype("category")
)
```

Tas semantiski norāda, ka kolonna satur kategorijas, nevis brīvu tekstu.

---

## 41. Korelācija

```python
df[[
    "rooms",
    "area_m2",
    "price_eur",
    "price_per_m2",
]].corr()
```

Atceries: korelācija nerāda cēloņsakarību un galvenokārt raksturo lineāru saistību.

---

## 42. Pivot tabula

`pivot_table()` ir līdzīga Excel PivotTable.

```python
pivot = pd.pivot_table(
    df,
    index="rooms",
    columns="building_series",
    values="price_eur",
    aggfunc="median",
)
```

Tas ir noderīgi, ja vēlamies salīdzināt divas kategoriju dimensijas.

---

## 43. `crosstab()` kategoriju kombinācijām

```python
pd.crosstab(
    df["rooms"],
    df["building_series"],
)
```

Proporcijas:

```python
pd.crosstab(
    df["rooms"],
    df["building_series"],
    normalize="index",
)
```

---

## 44. Divu tabulu savienošana ar `merge()`

Pieņemsim, ka ir divi `DataFrame`:

```python
apartments
streets
```

un abiem ir `street` kolonna.

```python
result = apartments.merge(
    streets,
    on="street",
    how="left",
)
```

Biežākie `how` varianti:

- `inner` — tikai sakrītošās rindas;
- `left` — visas kreisās tabulas rindas;
- `right` — visas labās tabulas rindas;
- `outer` — visas rindas no abām tabulām.

---

## 45. Tabulu apvienošana ar `concat()`

Ja ir vairāki vienādas struktūras faili:

```python
all_data = pd.concat(
    [df_january, df_february, df_march],
    ignore_index=True,
)
```

Tas ir tipisks veids, kā apvienot vairākus periodiskus eksportus.

---

## 46. `apply()` — lieto tikai tad, ja nav vienkāršākas vektorizētas operācijas

Piemērs:

```python
def classify_price(price):
    if price < 500:
        return "low"
    if price < 1000:
        return "medium"
    return "high"


df["price_category"] = (
    df["price_eur"]
    .apply(classify_price)
)
```

`apply()` ir elastīgs, bet bieži lēnāks un mazāk elegants nekā Pandas iebūvētās vektorizētās operācijas.

Pirms `apply()` vienmēr pajautā, vai to nevar izdarīt ar:

- aritmētiku;
- `.str`;
- `.dt`;
- `where()`;
- `map()`;
- `cut()`;
- `groupby()`.

---

## 47. `map()` vienas kolonnas vērtību pārveidošanai

```python
labels = {
    "New": "Jaunais projekts",
    "Recon.": "Renovēta ēka",
    "Pre-war house": "Pirmskara ēka",
}


df["series_lv"] = (
    df["building_series"]
    .map(labels)
)
```

Ja vārdnīcā nav attiecīgās vērtības, rezultāts būs `NaN`.

---

## 48. `replace()`

```python
df["building_series"] = (
    df["building_series"]
    .replace({
        "Recon": "Recon.",
        "New project": "New",
    })
)
```

Tas ir noderīgi kategoriju standartizēšanai.

---

## 49. Skaitliska mainīgā sadalīšana intervālos ar `cut()`

```python
df["price_band"] = pd.cut(
    df["price_eur"],
    bins=[0, 500, 800, 1200, float("inf")],
    labels=[
        "līdz 500",
        "501–800",
        "801–1200",
        "virs 1200",
    ],
)
```

Pēc tam:

```python
df["price_band"].value_counts()
```

---

## 50. Kvantiļu grupas ar `qcut()`

```python
df["price_quartile"] = pd.qcut(
    df["price_eur"],
    q=4,
    labels=["Q1", "Q2", "Q3", "Q4"],
)
```

Atšķirība:

- `cut()` — mēs nosakām intervālu robežas;
- `qcut()` — Pandas cenšas sadalīt novērojumus vienāda izmēra grupās.

---

## 51. Vienkārša vizualizācija no Pandas

Histogramma:

```python
df["price_eur"].plot.hist(bins=30)
```

Stabiņu diagramma:

```python
df["rooms"].value_counts().sort_index().plot.bar()
```

Horizontāla stabiņu diagramma:

```python
df["building_series"].value_counts().plot.barh()
```

Pandas `.plot()` izmanto Matplotlib kā vizualizācijas backend, tāpēc pēc tam var izmantot arī:

```python
import matplotlib.pyplot as plt

plt.title("Virsraksts")
plt.xlabel("X ass")
plt.ylabel("Y ass")
plt.show()
```

---

## 52. Rezultātu saglabāšana CSV

```python
df.to_csv(
    "apartments_clean.csv",
    index=False,
)
```

`index=False` parasti ir nepieciešams, lai tehniskais Pandas indekss netiktu saglabāts kā atsevišķa CSV kolonna.

---

## 53. Rezultātu saglabāšana Excel

```python
df.to_excel(
    "apartments_clean.xlsx",
    index=False,
)
```

---

## 54. Ērts analīzes darba stils

Tipisku datu analīzes plūsmu var organizēt šādi:

```python
import pandas as pd

# 1. Ielāde
raw_df = pd.read_csv("data.csv")

# 2. Kopija tīrīšanai
clean_df = raw_df.copy()

# 3. Kolonnu nosaukumu normalizēšana
clean_df = clean_df.rename(columns={
    "Price": "price_raw",
})

# 4. Tīrīšana un tipu konvertēšana
# ...

# 5. Analīzes populācijas izvēle
analysis_df = clean_df[
    clean_df["price_period"] == "month"
].copy()

# 6. Aprakstošā analīze
print(analysis_df.describe())

# 7. Grupēšana
stats = (
    analysis_df.groupby("rooms")
    .agg(
        listings=("price_eur", "count"),
        median_price=("price_eur", "median"),
    )
)

# 8. Eksports
clean_df.to_csv(
    "data_clean.csv",
    index=False,
)
```

Šāda struktūra palīdz nodalīt:

- izejas datus;
- tīrīšanu;
- analīzes izlasi;
- rezultātus.

---

# Īsā Pandas špikerlapa

| Uzdevums | Pandas operācija |
|---|---|
| Ielādēt CSV | `pd.read_csv()` |
| Pirmās rindas | `df.head()` |
| Izmērs | `df.shape` |
| Datu tipi | `df.info()`, `df.dtypes` |
| Kolonna | `df["column"]` |
| Vairākas kolonnas | `df[["a", "b"]]` |
| Filtrēt rindas | `df[condition]` |
| Kārtot | `df.sort_values()` |
| Trūkstošās vērtības | `df.isna().sum()` |
| Dzēst `NaN` | `df.dropna()` |
| Aizpildīt `NaN` | `df.fillna()` |
| Konvertēt uz skaitli | `pd.to_numeric()` |
| Teksta operācijas | `df["col"].str...` |
| Unikālās vērtības | `unique()`, `nunique()` |
| Biežumi | `value_counts()` |
| Dublikāti | `duplicated()`, `drop_duplicates()` |
| Vidējais | `mean()` |
| Mediāna | `median()` |
| Grupēšana | `groupby()` |
| Vairākas agregācijas | `agg()` |
| Grupas statistika katrai rindai | `transform()` |
| Pivot tabula | `pivot_table()` |
| Divu tabulu savienošana | `merge()` |
| Vairāku tabulu salikšana | `concat()` |
| Jauna kolonna | `df["new"] = ...` |
| Saglabāt CSV | `to_csv()` |
| Saglabāt Excel | `to_excel()` |

---

## Galvenais princips

Pandas kods kļūst daudz vieglāk saprotams, ja uz katru operāciju skatās kā uz vienu no dažiem pamatuzdevumiem:

```text
ielādēt → apskatīt → atlasīt → filtrēt → tīrīt → transformēt → grupēt → apkopot → vizualizēt → saglabāt
```

Lielākā daļa reālu datu analīzes darbu ir šo operāciju kombinācijas.
