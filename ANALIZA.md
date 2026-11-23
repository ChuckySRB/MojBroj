# Moj broj — analiza tri rešenja i predlog četvrtog

Za brojeve `9, 3, 8, 9, 20, 25` i cilj `992` izraz `((20 − 9) × 9 + 25) × 8` daje `124 × 8 = 992`. Prvi Python program na tom, svom podrazumevanom ulazu ispiše `Nema resenja :(`. Za poređenje algoritama zato su važna dva pitanja. Da li pretraga obuhvata svaki dozvoljeni izraz? Koliko puta računa nešto što je već izračunala?

**Pravila za poređenje.** Cilj iz README-a je tačan ili najbliži rezultat za šest ponuđenih brojeva. Svaku poziciju računam kao jednu pločicu koja se može upotrebiti najviše jednom. U gornjem primeru smeju da se koriste obe devetke i da se izostavi trojka. Pošto README ne precizira međurezultate, za analizu pretpostavljam pozitivne cele brojeve i deljenje bez ostatka. Opseg od 1 do 999 odnosi se na cilj. U procenama složenosti `n` je broj ponuđenih pločica, a `k` broj pločica u jednom izrazu. [Opis igre](./README.md)

## 1. MojBroj.c — prvo stabla, zatim operatori

`Nadji_Stabla` pokušava da spoji dva od raspoloživih stabala u jedno. `Resenje` kreće od nula spajanja, tako da i jedna ponuđena pločica može da bude odgovor. Binarno stablo je dobar izbor za prikaz izraza. Levo i desno dete određuju redosled operanada i zagrade, a isto stablo može da posluži i za računanje i za ispis. [MojBroj.c](./MojBroj.c#L22-L102)

Tri greške prekidaju put od te ideje do rezultata.

- **Nastala stabla ne stižu do pretrage.** Kada je stek prazan, bazni slučaj alocira lokalni `S` i izgubi pokazivač. U funkciji `Resenje` vrh ostaje `NULL`, pa petlja koja treba da proveri stabla nema šta da pročita.
- **Grane rekurzije nemaju ispravno skladište.** `M` ima mesta za jedan pokazivač. Za različite `i` i `j`, uslov `k != i || k != j` kopira sve elemente, uključujući oba odabrana. Uz to, `free(M)` je unutar petlje koja ga ponovo koristi, a različite grane prepisuju isti čvor `N`. Posledica je nedefinisano ponašanje.
- **Čak bi i ispravno stablo dobilo pogrešnu vrednost.** Sva četiri slučaja u `Calc_Tree` sabiraju. Operator se bira po dubini, pa bi dva unutrašnja čvora na istoj dubini morala da dele operator. Na kraju `main` preuzme koren i ništa ne ispiše. [Računanje i izlaz](./MojBroj.c#L64-L115)

**Složenost.** C kod je proveren statički. Zbog nedefinisanog ponašanja, procena važi za zamišljeni postupak sa ispravnim izborom para. Sa `m` preostalih stabala postoji `m(m−1)` uređenih parova. Do izraza sa svih `n` pločica vodi `H = n!(n−1)!` redosleda spajanja. Za šest pločica to je 86.400 redosleda, svaki sa još `4⁵` dodela operatora. Dve nezavisne grane mogu se izgraditi obrnutim redom i dati isto stablo. Računanje svih kandidata na ovaj način zahteva do `O(n · H · 4^(n−1))` vremena, a čuvanje zasebne kopije svakog stabla do `O(n · H)` prostora.

**Šta mu treba da bude koristan.** Birao bih parove sa `i < j` i računao vrednost odmah pri spajanju. Svaka grana treba da ima važeće čvorove do povratka iz rekurzije. Tada se može odmah odbaciti nedozvoljena operacija i sačuvati kopija najboljeg izraza čim se popravi rezultat. Time nestaje potreba za stekom svih stabala i zasebnim brojačem operatora. Za upotrebljiv program ostaju provera unosa i ispis izraza, vrednosti i odstupanja.

## 2. MojBroj.py — postfiksni šabloni i brojači

Ovde je dobra ideja funkcija `result`. U šablonu `ABoCo` prvo se spoje `A` i `B`, a zatim njihov rezultat i `C`. Stek tako obrađuje proizvoljne zagrade jednim prolazom. Program isprobava i kraće izraze i zaustavlja se na prvom pogotku. Slabost je u tri odvojena mehanizma koja treba da nabroje sva stabla, rasporede pločica i operatore. [MojBroj.py](./MojBroj.py#L23-L114)

| Šta se nabraja | Šta je pokazala provera |
|---|---|
| Oblici stabala | Za četiri pločice katalog sadrži četiri od pet oblika. Nedostaje `ABCooDo`, odnosno `(A op (B op C)) op D`. Za šest pločica sva 42 oblika postoje, ali se `ABCooDEFooo` javlja dvaput. |
| Rasporedi pločica | Za dve pločice `provera2` proizvede 25 različitih uređenih parova u 30 prolaza. Za pet pločica proizvede 32 od 720 rasporeda. Za šest pločica svih 720 prolaza koristi isti raspored indeksa. |
| Operatori | `provera(o, 0, 4)` prekida prenos na indeksu 3. Kada postoji pet operatora, peti ostaje `/`. Petlja od 1.024 prolaza ponovi istih 256 kombinacija četiri puta. |

**Složenost.** Ako je `Tₖ` broj upisanih šablona dužine `2k−1`, a `P(n,k) = n!/(n−k)!`, petlje bez ranog pogotka pozivaju evaluator tačno `Σₖ Tₖ · P(n,k) · 4^(k−1)` puta. U ovom fajlu to je **34.379.646 poziva**. Svaki čita do `2k−1` simbola i koristi stek od najviše `k` vrednosti. Memorijska prednost je što se završen kandidat odmah odbacuje. Ručni katalog zahteva još `O(Σₖ k · Tₖ)` prostora. Za poređenje, potpuna enumeracija bez ponavljanja istog zapisa ima 33.665.406 izraza za jednu do šest različito označenih pločica. Postojeće petlje rade više prolaza i ipak propuštaju pogodak za 992.

**Šta mu treba da bude koristan.** Zadržao bih evaluator kao referencu za proveru drugih rešenja na malim ulazima. Oblici se mogu generisati podelom stabla na levo i desno podstablo, rasporedi pomoću `itertools.permutations`, a operatori pomoću `itertools.product`. U evaluatoru treba proveriti deljivost i pozitivnost pre upisa na stek. Sada `/` uvodi `float`, a deljenje nulom vraća broj `-1` kao oznaku greške, što bi ometalo praćenje najbližeg rezultata. Funkcija koja prima brojeve i cilj, pamti najbolji pokušaj i vraća izraz sa zagradama omogućila bi proveru bilo koje partije bez izmene izvora.

## 3. MojBroj2026.py — spajanje već izračunatih izraza

Ova verzija najbolje povezuje pretragu sa onim što igrač želi da vidi. `Node` nosi i vrednost i postfiksni zapis, pa se rezultat dece koristi pri sledećem spajanju. Slova označavaju pozicije i pravilno razlikuju dve jednake pločice. `reconstruct_solution` vraća čitljiv izraz sa zagradama. Za brojeve iz uvoda i cilj 72, stari Python ispiše `[9, 8, '*']`, a ova verzija ispiše `9 * 8 = 72`. [Čvor i rekonstrukcija](./MojBroj2026.py#L22-L88)

- **Smer spajanja menja dostupne rezultate.** `merge_nodes` dvaput prosledi isti redosled dece. Petlja kroz dva nova čvora poseti i obrnuti par, ali za novi i ranije obrađen čvor dobija se samo smer `novi op stari`. To se vidi na malom ulazu koji `Solver` direktno prihvata. Za `[2, 3, 25]` i cilj `19` vraća `None`, iako je `25 − (2 × 3) = 19`. Za cilj `73` nalazi `(3 × 25) − 2`. [Spajanje i petlja pretrage](./MojBroj2026.py#L121-L170)
- **Jedna partija utiče na sledeću.** `Node.created_nodes` je lista na klasi. Dva uzastopna poziva `Solver([9, 3, 8, 9, 20, 25], 72).run()` u istom procesu daju najpre pogodak, zatim `None`. Drugi solver preskoči izraze koje je napravio prvi.
- **Pretraga pamti tekst izraza.** Na primer, `ab+` i `ba+` zauzimaju dva mesta iako koriste iste pločice i daju isti zbir. Provera članstva prolazi kroz listu, a unutrašnje petlje pokušavaju i parove koji dele pločice. Deljenje koristi `float`, negativni međurezultati prolaze, a kada nema pogotka `run` vrati `None` i glavni program ne prikaže najbliži rezultat.

**Složenost.** Neka je `P` broj pokušaja spajanja, `Q` broj pokušaja sa disjunktnim pločicama, a `E` broj zapamćenih zapisa u jednoj svežoj partiji. Spajanje proverava do `O(n)` simbola. Za pokušaje koji prođu tu proveru sledi pretraga liste sa do `E` poređenja stringova. Gornja granica vremena je `O(n · (P + Q · E))`, a prostora `O(n · (E + n))`. Već posle prvog kruga sa šest pločica na primeru za 72 čeka 120 izraza. Procena `6! · 4⁵` iz komentara u fajlu izostavlja 42 oblika zagrada. Potpuna sintaksna pretraga samo za šest pločica ima `6! · 42 · 4⁵ = 30.965.760` zapisa.

**Šta mu treba da bude koristan.** Prvo bih premestio evidenciju u instancu solvera i svaki neuređeni par obradio jednom. Za sabiranje i množenje dovoljan je jedan smer, a za oduzimanje i deljenje treba razmotriti oba i zadržati dozvoljene rezultate. Zamena liste skupom ubrzala bi proveru duplikata. Bit-maska potrošenih pozicija omogućila bi da se preklapanje odbaci pre sastavljanja stringa. Uz celobrojnu aritmetiku i pamćenje najbliže vrednosti, postojeći prikaz izraza može se direktno iskoristiti.

## 4. Predlog — dinamičko programiranje po podskupovima pločica

Za šest pločica izabrao bih tabelu sa **63 neprazna podskupa**. Svaki podskup predstavlja maska od šest bitova. Za svaku vrednost dostižnu baš tim pločicama tabela čuva jedan način da se vrednost dobije. Na primer, ako iste tri pločice daju 24 na dva načina, oba izraza imaju potpuno iste mogućnosti u nastavku partije. Dovoljno je sačuvati jedan. Vrednost 24 dobijena drugim pločicama ostaje zaseban unos jer su tada slobodni drugi brojevi.

1. Svaka pojedinačna pločica daje početni unos. Veći podskup se deli na dva neprazna, disjunktna dela na sve načine, svaki par delova jednom.
2. Kombinuju se vrednosti već poznate za ta dva dela. Zbir i proizvod računaju se jednom, a kod razlike i količnika ispituju se oba smera uz dogovorena pravila. Uz novu vrednost dovoljno je zapamtiti operaciju i dva prethodna unosa. Izraz sa zagradama se sastavi samo za pobednika.
3. Među rezultatima **svih** podskupova bira se najmanje apsolutno odstupanje od cilja. Pri istom odstupanju predlažem izraz sa manje pločica, jer ima i manje operacija. Ako se podskupovi obrađuju po veličini, prvi tačan pogodak već ispunjava taj kriterijum.

**Zašto pokriva celu igru.** Svaki složeni izraz ima poslednju operaciju koja deli upotrebljene pločice na dva disjunktna dela. Kada tabela stigne do tog podskupa, već ima obe vrednosti potrebne za poslednju operaciju. Time su obuhvaćene sve zagrade i dozvoljeni smerovi računanja. Važno je sačuvati i vrednosti iznad 999. Za legalno izvlačenje `1, 1, 1, 1, 10, 25` i cilj `999`, iscrpna provera po usvojenim pravilima daje jedinstvenu najbližu vrednost **1.000**, ostvarivu kao `(1 + 1) × (1 + 1) × 10 × 25`. Odstupanje je 1.

**Cena i izbor za ovaj projekat.** Za šest pločica ukupno postoji 301 neuređena podela kroz sve podskupove. Svaka podela `A | B` traži do šest operacija po paru vrednosti. Ako `r(S)` označava broj različitih vrednosti za podskup `S`, vreme je reda `Σ r(A) · r(B)` preko tih podela, uz očekivano konstantan pristup heš-tabeli. Memorija je reda `Σ r(S)` uz kratke reference za rekonstrukciju. To je cena čuvanja međurezultata, a stvarno trajanje zavisi od izvlačenja. Ovaj pristup bih izabrao za planiranu Rust verziju zato što isti prolaz daje proverljivo najbolji izraz i kada tačan pogodak postoji i kada ga nema.

**Najveći broj operacija u jednoj partiji.** Za četiri male pločice od 1 do 9 postoji 495 izbora kada se ponavljanja dozvole, a redosled zanemari. Sa tri srednje i četiri velike pločice iz generatora to daje `495 × 3 × 4 = 5.940` različitih izvlačenja. Provera tog prostora daje dva maksimuma, u zavisnosti od toga šta brojimo. [Generator brojeva](./MojBroj2026.py#L174-L179)

| Šta brojimo pri popunjavanju cele tabele | Maksimum | Pločice |
|---|---:|---|
| Dozvoljene aritmetičke operacije, kada se unapred preskoče nedozvoljeni smerovi | **116.193** | `2, 4, 6, 8, 20, 100` |
| Kandidati, ako se za svaki par ispitaju svih šest mogućnosti | **210.336** | `2, 4, 8, 9, 20, 100` |

U prvom redu svaki par daje zbir i proizvod. Za različite vrednosti računa se i pozitivna razlika, a količnik samo kada je deljenje tačno. Za jednake vrednosti količnik se računa jednom. Operacija se broji i ako njena vrednost već postoji u tabeli. Poređenja, provere deljivosti i pristup tabeli nisu uključeni. Sa pločicama iz prvog reda cilj **447** je nedostižan, pa svih 116.193 operacije treba obraditi i kada se pretraga prekida na tačnom pogotku. U drugom redu najzahtevnije izvlačenje daje 35.056 parova vrednosti, odnosno `35.056 × 6 = 210.336` kandidata. Sam izraz koji igrač vidi ima najviše pet operacija.
