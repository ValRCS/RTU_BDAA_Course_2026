# Datu analīzes un vizualizācijas principi

Šis materiāls apkopo praktiskus principus darbam ar **divdimensionāliem jeb tabulāriem datiem**: rindas parasti apzīmē novērojumus, bet kolonnas — pazīmes jeb mainīgos. Tieši šādā formā dati visbiežāk nonāk `pandas.DataFrame`, CSV failos, Excel tabulās un datubāzu vaicājumu rezultātos.

Lekcijas piemēros izmantojam SS.com dzīvokļu sludinājumus, taču zemāk aprakstītie principi attiecas arī uz pārdošanas datiem, klientu sarakstiem, sensoriem, aptaujām, finanšu datiem un citiem biznesa datiem.

---

## 1. Sāc ar jautājumu, nevis ar grafiku

Pirms rakstīt kodu, formulē, **ko tieši vēlies noskaidrot**.

Piemēri:

- Kāda ir tipiska dzīvokļa īres cena?
- Kā cena mainās atkarībā no dzīvokļa platības?
- Kurām ēku sērijām ir augstāka cena par kvadrātmetru?
- Vai datos ir aizdomīgi vai ļoti ekstrēmi sludinājumi?
- Kāds ir piedāvājumu sadalījums pēc istabu skaita?

Labs analīzes jautājums nosaka:

1. kuras kolonnas mums vajadzīgas;
2. kā dati jātīra;
3. kādu statistiku aprēķināt;
4. kādu vizualizāciju izvēlēties.

> Vizualizācija nav mērķis pati par sevi. Tā ir instruments, kas palīdz atbildēt uz konkrētu jautājumu.

---

## 2. Saprot datu struktūru

Tipiskā tabulā:

- **rinda** = viens novērojums;
- **kolonna** = viena pazīme;
- **šūna** = konkrētās pazīmes vērtība konkrētam novērojumam.

SS.com piemērā viena rinda var būt viens dzīvokļa sludinājums, bet kolonnas var būt:

- `street` — iela;
- `rooms` — istabu skaits;
- `area_m2` — platība;
- `building_series` — ēkas tips;
- `price_eur` — cena;
- `price_per_m2` — cena par m².

Pirms analīzes pārbaudi:

```python
print(df.shape)
print(df.columns)
df.head()
df.info()
```

Īpaši svarīgi ir noskaidrot:

- cik ir rindu un kolonnu;
- vai kolonnas satur to, ko sagaidām;
- kādi ir datu tipi;
- cik daudz ir trūkstošu vērtību.

---

## 3. Nosaki mainīgo tipus

Vizualizācijas un statistikas izvēle ir atkarīga no mainīgā veida.

### Skaitliski mainīgie

Piemēri:

- cena;
- platība;
- vecums;
- ieņēmumi;
- temperatūra.

Ar tiem var aprēķināt vidējo, mediānu, standartnovirzi, korelāciju u.c.

### Kategoriski mainīgie

Piemēri:

- ēkas sērija;
- pilsēta;
- produkta kategorija;
- klienta tips.

Tiem parasti analizē biežumus, proporcijas vai skaitlisko rādītāju sadalījumu pa grupām.

### Ordināli mainīgie

Kategorijas ar dabisku secību:

- zems / vidējs / augsts;
- 1–5 vērtējums;
- junior / middle / senior.

### Teksts un identifikatori

Piemēri:

- apraksts;
- URL;
- klienta ID.

Identifikatorus parasti neizmanto statistiskai analīzei kā skaitļus. Teksts bieži prasa atsevišķas teksta apstrādes metodes.

---

## 4. Datu tīrīšana ir daļa no analīzes

Reāli dati gandrīz nekad nav pilnīgi gatavi analīzei.

Pārbaudi vismaz šīs problēmas:

### Trūkstošas vērtības

```python
df.isna().sum()
```

Jāizlemj, vai:

- trūkstošo rindu izņemt;
- vērtību aizstāt;
- atstāt kā `NaN`;
- analizēt, kāpēc vērtība vispār trūkst.

### Dublikāti

```python
df.duplicated().sum()
```

Ja ir stabils identifikators, piemēram, URL:

```python
df.duplicated(subset="url").sum()
```

### Nepareizi datu tipi

Cena `"650 €/mon."` ir teksts, kaut semantiski tā satur skaitli.

Tīrīšanas mērķis ir iegūt atsevišķas strukturētas vērtības, piemēram:

- `price_eur = 650`;
- `price_period = "month"`.

### Nesalīdzināmas mērvienības

`35 €/day` un `650 €/month` nedrīkst vienkārši salīdzināt kā vienu un to pašu mainīgo.

Ja vērtības pārveido uz vienotu mērvienību, skaidri dokumentē pieņēmumu.

---

## 5. Saglabā izejas datus un izveido tīrās kolonnas

Drošs princips ir nepārrakstīt izejas informāciju bez vajadzības.

Piemēram:

- `price_raw` — sākotnējais teksts;
- `price_eur` — iztīrīts skaitlis;
- `price_period` — cenas periods.

Tas ļauj vēlāk pārbaudīt, vai tīrīšana bijusi korekta.

Tipiska plūsma:

```text
raw data → cleaning → validated data → analysis
```

nevis:

```text
raw data → overwrite everything → cerēt, ka nekas nav pazaudēts
```

---

## 6. Vispirms veic vienas kolonnas analīzi

Pirms pētīt sakarības starp vairākiem mainīgajiem, saproti katru svarīgo kolonnu atsevišķi.

Skaitliskam mainīgajam pārbaudi:

```python
df["price_eur"].describe()
```

Svarīgākie rādītāji:

- `count` — novērojumu skaits;
- `mean` — aritmētiskais vidējais;
- `std` — standartnovirze;
- `min`, `max`;
- `25%`, `50%`, `75%` — kvartiles;
- `50%` ir mediāna.

Kategoriskam mainīgajam:

```python
df["building_series"].value_counts()
```

---

## 7. Vidējais nav vienmēr “tipiskā” vērtība

Aritmētiskais vidējais ir jutīgs pret ekstrēmām vērtībām.

Ja vairums dzīvokļu maksā 400–900 €, bet daži maksā 3000 €, vidējā cena var būt ievērojami augstāka par cenu, ko redz tipiskā sludinājumā.

Tāpēc bieži salīdzina:

```python
series.mean()
series.median()
```

### Praktisks princips

- simetrisks sadalījums bez ekstrēmiem novērojumiem → vidējais bieži ir labs kopsavilkums;
- šķībs sadalījums vai ekstrēmas vērtības → mediāna bieži ir informatīvāka.

---

## 8. Grupēšana: salīdzini ne tikai kopējo datu kopu

Daudzos biznesa jautājumos svarīgas ir atšķirības starp grupām.

Piemēram:

```python
df.groupby("rooms")["price_eur"].median()
```

vai vairāki rādītāji vienlaikus:

```python
(
    df.groupby("rooms")
      .agg(
          listings=("price_eur", "count"),
          median_price=("price_eur", "median"),
          mean_area=("area_m2", "mean"),
      )
)
```

Pirms interpretācijas pārbaudi arī grupas lielumu. Grupas mediāna, kas balstīta uz 2 novērojumiem, nav tik stabila kā mediāna, kas balstīta uz 200 novērojumiem.

---

## 9. Izvēlies grafiku pēc jautājuma

### Viena skaitliska mainīgā sadalījums → histogramma

Piemērs: dzīvokļu cenu sadalījums.

```python
df["price_eur"].plot.hist(bins=30)
```

Histogramma palīdz redzēt:

- tipisko diapazonu;
- sadalījuma formu;
- asimetriju;
- vairākas iespējamās grupas;
- ekstrēmas vērtības.

### Kategoriju biežumi vai kopsavilkumi → stabiņu diagramma

Piemērs: sludinājumu skaits pēc istabu skaita.

```python
df["rooms"].value_counts().sort_index().plot.bar()
```

Stabiņu diagramma ir laba atsevišķu kategoriju salīdzināšanai.

### Divi skaitliski mainīgie → izkliedes diagramma

Piemērs: platība pret cenu.

```python
plt.scatter(df["area_m2"], df["price_eur"], alpha=0.5)
```

Tā palīdz pamanīt:

- pozitīvu vai negatīvu sakarību;
- nelineāru sakarību;
- klasterus;
- ekstrēmus novērojumus.

### Skaitlisks mainīgais pa kategorijām → boxplot

Piemērs: cena par m² dažādiem ēku tipiem.

```python
df.boxplot(column="price_per_m2", by="building_series")
```

Boxplot parāda ne tikai vienu vidējo vērtību, bet arī izkliedi un potenciālos ekstrēmus novērojumus.

### Laika dati → līniju diagramma

Ja x ass ir laiks un secība ir būtiska, parasti izmanto līniju diagrammu.

---

## 10. Histogramma un stabiņu diagramma nav viens un tas pats

Šī ir bieža kļūda.

### Histogramma

- paredzēta skaitliskam, bieži nepārtrauktam mainīgajam;
- x ass tiek sadalīta intervālos (`bins`);
- blakus esošie stabiņi reprezentē blakus esošus vērtību intervālus.

### Stabiņu diagramma

- paredzēta kategorijām;
- katrs stabiņš ir atsevišķa kategorija;
- kategoriju secība ne vienmēr ir skaitliski nepārtraukta.

---

## 11. Korelācija nav cēloņsakarība

Korelācija raksturo divu skaitlisku mainīgo lineāras sakarības stiprumu.

```python
df[["area_m2", "price_eur"]].corr()
```

Tomēr:

> korelācija pati par sevi nepierāda, ka viens mainīgais izraisa otru.

Dzīvokļa platība un cena var būt saistītas, taču cenu vienlaikus ietekmē arī:

- atrašanās vieta;
- ēkas tips;
- remonta stāvoklis;
- stāvs;
- mēbeles;
- tirgus situācija.

Turklāt Pearson korelācija galvenokārt raksturo **lineāru** sakarību.

---

## 12. Ekstrēms novērojums nav automātiski kļūda

Ļoti augsta vai zema vērtība var būt:

1. datu ievades kļūda;
2. scraping kļūda;
3. cita mērvienība;
4. cita piedāvājuma kategorija;
5. pilnīgi korekts, bet neparasts novērojums.

Pārbaudi ekstrēmos novērojumus:

```python
df.nlargest(10, "price_eur")
df.nsmallest(10, "price_eur")
```

Ja datos ir URL uz avotu, tas ir īpaši noderīgi — var atvērt oriģinālo ierakstu un pārbaudīt interpretāciju.

---

## 13. Labs grafiks ir vienkāršs un salasāms

Grafikā parasti jābūt:

- skaidram virsrakstam;
- saprotamiem asu nosaukumiem;
- mērvienībām;
- pietiekami lielam izmēram;
- leģendai tikai tad, ja tā tiešām nepieciešama.

Piemērs:

```python
plt.figure(figsize=(8, 5))
plt.scatter(df["area_m2"], df["price_eur"], alpha=0.5)
plt.xlabel("Platība (m²)")
plt.ylabel("Mēneša īres cena (€)")
plt.title("Dzīvokļa platība un īres cena")
plt.show()
```

Grafikam jābūt saprotamam arī cilvēkam, kurš neredzēja kodu, ar kuru tas tika izveidots.

---

## 14. Neizmanto 3D grafiku, ja dati nav trīsdimensionāli

3D efekti bieži:

- apgrūtina salīdzināšanu;
- deformē uztveri;
- aizņem vairāk vietas;
- reti pievieno informāciju.

Divdimensionāliem biznesa datiem parasti pietiek ar:

- histogrammu;
- stabiņu diagrammu;
- līniju diagrammu;
- izkliedes diagrammu;
- boxplot.

---

## 15. Ass sākumpunkts var mainīt iespaidu

Stabiņu diagrammām y ass parasti jāsākas no nulles, jo stabiņa garums reprezentē lielumu.

Līniju diagrammās y ass ne vienmēr obligāti sākas no nulles, jo galvenais var būt izmaiņu dinamika. Tomēr saīsināta ass jāizmanto apzināti, lai nepārspīlētu atšķirības.

Vienmēr pajautā:

> Vai grafika mērogs godīgi reprezentē datus?

---

## 16. Pārāk daudz kategoriju samazina grafika vērtību

Ja `building_series` ir 20–30 kategorijas, grafiks var kļūt nelasāms.

Iespējamās stratēģijas:

- atlasīt biežākās kategorijas;
- apvienot reti sastopamās kategorijas grupā `Other`;
- izmantot horizontālu stabiņu diagrammu;
- sakārtot kategorijas pēc vērtības.

Piemērs:

```python
series_stats = (
    df.groupby("building_series")["price_per_m2"]
      .median()
      .sort_values()
)

series_stats.plot.barh()
```

---

## 17. Filtrēšana ir analītisks lēmums

Filtrs nav tikai tehniska Pandas operācija.

Piemēram:

```python
monthly = df[df["price_period"] == "month"]
```

nozīmē, ka esam definējuši analīzes populāciju kā **mēneša īres sludinājumus**.

Līdzīgi:

```python
two_room = df[df["rooms"] == 2]
```

maina jautājumu no “kādi ir visi dzīvokļi?” uz “kādi ir divistabu dzīvokļi?”.

Vienmēr dokumentē svarīgus filtrēšanas kritērijus.

---

## 18. Atšķir “datus” no “secinājuma”

Piemērs:

**Dati:**

> 2 istabu dzīvokļu mediānas cena šajā datu kopā ir 620 €.

**Interpretācija:**

> Šajā SS.com izlasē 620 € var kalpot kā orientieris tipiskai 2 istabu dzīvokļa cenai.

**Pārāk plašs secinājums:**

> Visi 2 istabu dzīvokļi Rīgā maksā ap 620 €.

Scraping dati parasti ir **novērojumu izlase konkrētā laikā**, nevis pilnīgs tirgus modelis.

---

## 19. Reproducējamība

Labai analīzei jābūt atkārtojamai.

Tas nozīmē:

- datu ielāde ir kodā;
- tīrīšana ir kodā;
- filtri ir kodā;
- aprēķini ir kodā;
- grafiki ir kodā;
- svarīgi pieņēmumi ir dokumentēti Markdown tekstā.

Jupyter Notebook ir īpaši piemērots šādai darba formai, jo vienā failā var saglabāt gan skaidrojumus, gan kodu, gan rezultātus.

---

# Praktiska datu analīzes kontrolsaraksta versija

## A. Pirms analīzes

- [ ] Kādu jautājumu es gribu atbildēt?
- [ ] Kas ir viena datu rindas novērojuma vienība?
- [ ] Kuras kolonnas vajadzīgas?
- [ ] Vai šo kolonnu nozīme ir skaidra?
- [ ] Kādas ir mērvienības?

## B. Datu kvalitāte

- [ ] Pārbaudīts `df.shape`.
- [ ] Pārbaudīts `df.info()`.
- [ ] Pārbaudītas trūkstošās vērtības.
- [ ] Pārbaudīti dublikāti.
- [ ] Skaitļi tiešām ir skaitliski datu tipi.
- [ ] Kategoriju nosaukumi ir konsekventi.
- [ ] Mērvienības ir salīdzināmas.
- [ ] Ekstrēmi novērojumi ir apskatīti.

## C. Pamata analīze

- [ ] Apskatīts `describe()`.
- [ ] Salīdzināts vidējais ar mediānu, ja tas ir būtiski.
- [ ] Kategorijām apskatīts `value_counts()`.
- [ ] Vajadzības gadījumā veikta grupēšana ar `groupby()`.
- [ ] Pārbaudīts grupu novērojumu skaits.

## D. Vizualizācija

- [ ] Grafiks atbilst jautājumam un mainīgo tipiem.
- [ ] Ir skaidrs virsraksts.
- [ ] Asīm ir nosaukumi un mērvienības.
- [ ] Kategoriju etiķetes ir salasāmas.
- [ ] Mērogs nav maldinošs.
- [ ] Nav nevajadzīgu 3D efektu vai dekorāciju.
- [ ] Grafiks papildina analīzi, nevis vienkārši atkārto tabulu.

## E. Secinājumi

- [ ] Secinājums tiešām izriet no datiem.
- [ ] Nav sajaukta korelācija ar cēloņsakarību.
- [ ] Ir skaidrs, uz kādu datu kopu secinājums attiecas.
- [ ] Ir minēti svarīgi filtri vai pieņēmumi.
- [ ] Analīzi var atkārtot, palaižot kodu vēlreiz.

---

## Īsais princips

Tipiska kvalitatīva datu analīzes plūsma ir:

```text
1. Jautājums
2. Datu izpratne
3. Datu kvalitātes pārbaude
4. Tīrīšana un tipu sakārtošana
5. Izpētes analīze
6. Grupēšana un salīdzināšana
7. Atbilstoša vizualizācija
8. Rezultātu interpretācija
9. Pieņēmumu un ierobežojumu dokumentēšana
10. Reproducējams gala rezultāts
```

Svarīgākais princips: **vispirms saproti, ko dati nozīmē, un tikai tad aprēķini un zīmē.**
