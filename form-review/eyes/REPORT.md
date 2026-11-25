# Visual Print Audit — All 43 Forms

- **Branch**: `try/forms-eyes` (no code changes)
- **Base commit**: `origin/main` @ `51609c0b`
- **Taxpayer**: Demo taxpayer (`SANTOS, JUANA MARIA DELA CRUZ-VILLANUEVA`, TIN `000-123-453-00000`, RDO `008`)
- **Method**: Opened each form in the NSH Linux desktop app (`just nsh-run-agent` with scratch DB), populated a realistic return through the form page (reusing official samples), saved draft, opened Print Preview (`fp-print`), saved PDF via headless Chrome, and compared every rendered page side-by-side (`compare-pN.png`: official BIR sheet on the left, our printed PDF on the right).
- **Grand Totals (43 Forms)**: **`6 clean`**, **`12 tweak`**, **`25 broken`**.
  - **Clean (6)**: `0619E`, `1700`, `1602Q`, `1603Q`, `1707A`, `2000OT`
  - **Tweak (12)**: `2551Q`, `1701A`, `2550Q`, `1601C`, `1601EQ`, `0619F`, `1601FQ`, `1604F`, `1706`, `1707`, `2552`, `2200AN`
  - **Broken (25)**: `2550M`, `1701`, `1701Q`, `0605`, `1701MS`, `1702Q`, `1702RT`, `1702EX`, `1702MX`, `1600WP`, `1600PT`, `1600VT`, `1604C`, `1604E`, `1606`, `1800`, `1801`, `2000`, `2553`, `2200A`, `2200C`, `2200M`, `2200P`, `2200S`, `2200T`

---

## Batch 1: First 10 Priority Forms

| # | Form | Version | Pages (Ours / Official) | Verdict | Highest Harm | Summary |
|---|---|---|---|---|---|---|
| 1 | **2551Q** | Jan 2018 (ENCS) | 2 / 2 | **tweak** | Looks wrong on paper | Page 2 omits Table 1 (ATC table); unused Items 16–17 print `0.00`. |
| 2 | **1701Q** | Jan 2018 (ENCS) | 2 / 2 | **broken** | Looks wrong on paper | Page 2 TIN crushed on far left with empty `00000` beside it; Page 2 omits Tax Rate Tables 1 & 2; unused Sched II & Spouse boxes print `0`. |
| 3 | **1701** | Jan 2018 (ENCS) | 4 / 4 | **broken** | Return cannot be completed / Wrong number filed | On `origin/main` (`51609c0b`), 31 Sched 3.A/4/6.A.2 boxes remain locked; Page 3 Sched 6 Item 8 total is vertically clipped/unreadable; Sched 6 prints `0.00` with centavos; Page 4 omits Tax Rate Tables 1 & 2. |
| 4 | **1701A** | Jan 2018 (ENCS) | 2 / 2 | **tweak** | Looks wrong on paper | Page 2 omits Tax Rate Tables 1 & 2; TIN branch `00000` slightly bold/doubled over preprint; otherwise crisp. |
| 5 | **2550Q** | Apr 2024 (ENCS) | 2 / 2 | **tweak** | Looks wrong on paper | Scaled to Letter with bottom whitespace vs Folio/Legal official sheet; unused Part V Schedules 1–4 cells print left-aligned `0.00`. |
| 6 | **2550M** | Feb 2007 (ENCS) | 2 / 2 (frozen HTML ref) | **broken** | Wrong number filed | On `origin/main` (`51609c0b`), Item 13B & 18F/H/J/L/O stay `0.00` (wrong totals in 16B/19/22/26); Item 9 address clipped at right edge; Sched 4 prints `5.00` when untouched; amounts left-aligned. |
| 7 | **1601C** | Jan 2018 (ENCS) | 2 / 2 | **tweak** | Looks wrong on paper | Page 2 omits Guidelines and Instructions (~70% blank page); unused Part II boxes print `0.00`. |
| 8 | **0619E** | Jan 2018 (ENCS) | 1 / 1 | **clean** | Cosmetic | Exact 1-page match; all boxes, totals, and penalties land cleanly (only unused Item 15 prints `0.00`). |
| 9 | **1601EQ** | Jan 2019 (ENCS) | 2 / 2 | **tweak** | Looks wrong on paper | Page 2 omits the entire Schedule of ATCs (prints only 1-inch header over a blank page); unused ATC rows 13–18 print `0.00` in Tax Withheld. |
| 10 | **0605** | Jul 1999 (ENCS) | 1 / 2 | **broken** | Looks wrong on paper | Item 15 address truncated/clipped at right edge (`...METRO M`); Page 2 (ATC/Tax Type tables & Guidelines) missing; Part II amounts left-aligned against item labels `20A`–`20D`. |

**Totals**: `1 clean`, `5 tweak`, `4 broken`.

---

## Findings Ranked by Harm

### 1. Wrong number filed
- **2550M (Page 1, Part II)**: On `origin/main` (`51609c0b`, before #315 merges), entering Sales to Government (`13A = 250,000.01`) leaves `13B` at `0.00` (expected `30,000.00`), and entering Purchases (`18E/G/I/K/N`) leaves `18F/H/J/L/O` at `0.00`, causing wrong totals in `16B` (`0.00`), `19` (`1,600.24`), `22` (`-1,590.24`), and `26` (`-1,790.24`).
- **1701 (Pages 2–3, Schedules 3.A, 4, 6.A.2)**: On `origin/main` (`51609c0b`, before `try/forms-1701-locked` merges), 31 business income/deduction/spouse-NOLCO boxes remain locked at `0.00`, misstating business tax due.

### 2. Return cannot be completed
- **1701 (Pages 2–3)**: Self-employed / mixed-income graduated-rate filers cannot enter Sales (`8A/B`), Returns (`9A/B`), Cost of Sales (`11A/B`), or 18 Schedule 4 deduction lines on `origin/main` (`51609c0b`).

### 3. Looks wrong on paper
- **1701Q (Page 2 TIN header)**: `00012345300000` prints crushed/overlapping on the far left of the TIN box while the pre-printed `0 0 0 0 0` branch-code digits sit empty to the right (`1701Q/compare-p2.png`).
- **1701 (Page 3, Schedule 6.A.1 Item 8)**: `Total NOLCO - Taxpayer/Filer` column D (`0.00`) is vertically clipped into an unreadable smudge at the top border of row 8 (`1701/compare-p3.png`).
- **2550M (Page 1, Item 9) & 0605 (Page 1, Item 15)**: Long registered address prints on a single shrunk line and truncates at the right edge (`...METRO MAN` on 2550M; `...METRO M` on 0605) instead of wrapping (`2550M/compare-p1.png`, `0605/compare-p1.png`).
- **2550M (Page 2, Schedule 4)**: Untouched `Less: Standard Input Tax to sale to government` prints `5.00` in the peso box (`2550M/compare-p2.png`).
- **1701 (Pages 3–4, Schedule 6.A.1 & 6.A.2)**: Empty NOLCO cells print left-aligned `0.00` with centavos on a whole-peso form (`DO NOT enter Centavos`).
- **2550M (Pages 1–2) & 0605 (Page 1, Part II)**: Peso amounts are left-aligned instead of right-aligned; on 0605, `20A`–`20D` values sit flush against the item labels (`0605/compare-p1.png`).
- **Missing reference tables / instructions / Page 2**:
  - **1601EQ Page 2**: Omits the entire Schedule of ATCs, producing a nearly blank Page 2 with only the top header bar (`1601EQ/compare-p2.png`).
  - **2551Q Page 2**: Omits `Table 1 – Alphanumeric Tax Code (ATC)` (~70% blank bottom) (`2551Q/compare-p2.png`).
  - **1601C Page 2**: Omits `Guidelines and Instructions for BIR Form No. 1601-C` (~70% blank bottom) (`1601C/compare-p2.png`).
  - **1701Q Page 2, 1701 Page 4, 1701A Page 2**: Omit `TABLE 1` and `TABLE 2 – Tax Rates` at the bottom of the last page.
  - **0605 Page 2**: Missing entirely (1 page printed vs 2-page official sheet containing ATC/Tax Type tables and Guidelines) (`0605/compare-p2.png`).
- **2550Q (Pages 1–2)**: Printed scaled into Letter with bottom whitespace vs Folio/Legal official sheet; unused Part V Schedules 1–4 cells print left-aligned `0.00` (`2550Q/compare-p1.png`, `2550Q/compare-p2.png`).
- **Unused amount boxes printing `0` / `0.00`**: Observed across `2551Q`, `1701Q` (including unused Schedule II & Spouse column), `1701`, `2550Q`, `2550M`, `1601C`, `0619E` (Item 15), and `1601EQ` (empty ATC rows 13–18). (`1701A` cleanly leaves unused boxes blank.)

### 4. Cosmetic
- **Comb-tick drift on long names/addresses**: `SANTOS, JUANA MARIA DELA CRUZ-VILLANUEVA` and the 2-line registered address drift slightly across comb tick marks on `2551Q`, `1701Q`, `1701`, `2550Q`, `1601C`, `0619E`, `1601EQ` (all characters legible, no clipping).
- **1701A TIN branch `00000`**: Slightly bold/doubled over the pre-printed `00000` in Item 4 and Item 66.
- **Negative-sign spacing**: Minus sign sits tight against the leading digit in comb cells on overpayments (e.g., `1601EQ` Items 26/31 `-3,000.51`).

---

## Per-Form Evidence

- **2551Q**: `2551Q/compare-p1.png`, `2551Q/compare-p2.png` (`ours-p1.png`, `ours-p2.png`)
- **1701Q**: `1701Q/compare-p1.png`, `1701Q/compare-p2.png` (`ours-p1.png`, `ours-p2.png`)
- **1701**: `1701/compare-p1.png` – `1701/compare-p4.png` (`ours-p1.png` – `ours-p4.png`)
- **1701A**: `1701A/compare-p1.png`, `1701A/compare-p2.png` (`ours-p1.png`, `ours-p2.png`)
- **2550Q**: `2550Q/compare-p1.png`, `2550Q/compare-p2.png` (`ours-p1.png`, `ours-p2.png`)
- **2550M**: `2550M/compare-p1.png`, `2550M/compare-p2.png` (`ours-p1.png`, `ours-p2.png`)
- **1601C**: `1601C/compare-p1.png`, `1601C/compare-p2.png` (`ours-p1.png`, `ours-p2.png`)
- **0619E**: `0619E/compare-p1.png` (`ours-p1.png`)
- **1601EQ**: `1601EQ/compare-p1.png`, `1601EQ/compare-p2.png` (`ours-p1.png`, `ours-p2.png`)
- **0605**: `0605/compare-p1.png`, `0605/compare-p2.png` (`ours-p1.png`)

---

## Remaining 33 Forms (Batches 2–4)

| # | Form | Pages (Ours / Official) | Verdict | Highest Harm | Summary |
|---|---|---|---|---|---|
| 11 | **1700** | 2 / 2 (frozen HTML) | **clean** | Cosmetic | Exact 2-page match; whole-peso comb values (`(100)`) crisp, unused boxes blank; TIN branch `00000` slightly bold over preprint. |
| 12 | **1701MS** | 2 / 2 (frozen HTML) | **broken** | Wrong number filed | On `origin/main` (`51609c0b`, before #323), Items 2A/2B non-taxable compensation locked → overstated tax due; print layout itself is crisp (unused Part II boxes print `0`). |
| 13 | **1702Q** | 2 / 3 (official PDF) | **broken** | Wrong number filed / Looks wrong on paper | Whole-peso Part II prints `.00` shifted into peso combs (**100× overstated**: `875,000` prints as `87,500,000`); Item 2 `2025` collides with pre-printed `/20`; Page 3 (ATC table & Guidelines) missing. |
| 14 | **1702RT** | 4 / 4 (official PDF) | **broken** | Looks wrong on paper | Page 1 Item 2 `2025` collides with pre-printed `/20`; TIN branch `00000` doubled over preprint; otherwise whole-peso values align cleanly. |
| 15 | **1702EX** | 3 / 3 (frozen HTML) | **broken** | Looks wrong on paper | Page 1 Item 2 `2025` collides with pre-printed `/20`; Item 9 address truncated at `...SAN LOREN`; Item 6 `00000` & Item 18 `000` doubled over preprints. |
| 16 | **1702MX** | 4 / 4 (frozen HTML) | **broken** | Looks wrong on paper | Page 1 Item 2 `2025` collides with pre-printed `/20`; Part II Items 14–16 print blank while Item 21 carries `-79,000`; TIN `00000` doubled. |
| 17 | **0619F** | 1 / 1 (official PDF) | **tweak** | Cosmetic | Exact 1-page match; Item 5 Tax Type Code (`WF`) is tiny; unused Part II boxes print `0.00`. |
| 18 | **1601FQ** | 2 / 2 (frozen HTML) | **tweak** | Cosmetic | Exact 2-page match; totals and comb values crisp; unused Part II rows 14–19 & penalties print `0.00`. |
| 19 | **1602Q** | 3 / 3 (frozen HTML) | **clean** | Cosmetic | Exact 3-page match; all Part II totals (`282,175.38`) and schedules align cleanly (unused boxes print `0.00`). |
| 20 | **1603Q** | 2 / 2 (frozen HTML) | **clean** | Cosmetic | Exact 2-page match; all Part II totals (`112,788.34`) and schedules align cleanly (unused boxes print `0.00`). |
| 21 | **1600WP** | 1 / 1 (frozen HTML) | **broken** | Wrong number filed | Schedule 1.1 lists `4,000.00 + 2,010.01 = 6,010.01`, yet Schedule `TOTAL` & Part II rows are blank and Item 12 = `0.00` (Item 16 = `-1,000.00`); Item 9 address microscopic & clipped (`...METRO`); Part II amounts left-aligned. |
| 22 | **1600PT** | 2 / 2 (frozen HTML) | **broken** | Wrong number filed | Page 2 Schedule 1 computes `6,005.00`, yet Page 1 Item 3 = `No`, Part II rows 13–17 blank, Item 18 = `0.00` (Item 27 = `-250.50`); Item 1 `06 2025` collides with pre-printed `2 0`; unused Sched 1 rows print `0.00`. |
| 23 | **1600VT** | 2 / 2 (frozen HTML) | **broken** | Wrong number filed | Same twin defects as 1600PT: Page 2 Schedule 1 = `6,005.00` vs Page 1 Part II = `0.00` (Item 27 = `-250.50`); Item 1 `06 2025` collides with pre-printed `2 0`. |
| 24 | **1604C** | 1 / 1 (frozen HTML) | **broken** | Looks wrong on paper | Page 1 Item 1 `For the Year (20YY)` prints `25` over pre-printed `2 0` (garbled `225 0`); Part II amounts left-aligned with unused months printing `0.00`. |
| 25 | **1604E** | 2 / 2 (frozen HTML) | **broken** | Looks wrong on paper | Page 1 Item 1 prints `25` over pre-printed `2 0` (garbled `225 0`); Item 7 address truncated at `...845 ARNAIZ AV`; Part II amounts left-aligned (`0.00` on unused rows). |
| 26 | **1604F** | 2 / 2 (frozen HTML) | **tweak** | Looks wrong on paper | Page 1 Item 7 address truncated at `...845 ARNAIZ AV` (Item 1 `2025` is clean); Part II amounts left-aligned (`0.00` on unused rows). |
| 27 | **1606** | 2 / 2 (frozen HTML) | **broken** | Wrong number filed | Page 2 Schedule 1 FMVs (`4,200,000.00 + 1,500,000.00 = 5,700,000.00`) print `TOTAL = 0.00` and Sched 3 Item 1B = `0.00`, understating Taxable Base (`5,000,000.01` vs `5,700,000.00`); Buyer address microscopic & clipped (`...METRO`); empty Seller TIN prints `--00000`. |
| 28 | **1706** | 2 / 2 (frozen HTML) | **tweak** | Looks wrong on paper | Totals (`1,800,001.00`, tax `108,000.06`) clean; Seller address microscopic & clipped (`...METR`); empty Buyer TIN prints `--00000` (`00000` on Page 2); unused boxes print `0.00`. |
| 29 | **1707** | 2 / 2 (frozen HTML) | **tweak** | Looks wrong on paper | Totals (`573,222.22`) clean; Seller/Buyer names & addresses microscopic; TINs lack dashes; unused Schedule 1 (Installment) prints `0.00` in every box. |
| 30 | **1707A** | 2 / 2 (frozen HTML) | **clean** | Cosmetic | Exact 2-page match; all Part II (`176,570.06`) & Schedule 1/2 gain/loss rows crisp (TIN `00000` slightly bold; Sched 1/2 amounts left-aligned). |
| 31 | **1800** | 2 / 2 (frozen HTML) | **broken** | Looks wrong on paper | Page 1 Item 14 (`Total Net Gifts Subject to Tax`) is **blank** while Page 2 Item 38 = `2,934,567.90` and Page 1 Item 16 Tax Due = `176,074.07`; TIN `00000` & Item 37 `250,000.00` bold over preprints; unused rows print `0.00`. |
| 32 | **1801** | 2 / 2 (frozen HTML) | **broken** | Looks wrong on paper | Page 1 Item 5 **TIN is blank** (only pre-printed `00000` shows, though Page 2 header prints `00012345300000`); Page 1 Item 16 (`Net Taxable Estate`) is blank when Page 2 Item 40 is negative (`-3,489,999.38`). |
| 33 | **2000** | 2 / 2 (frozen HTML) | **broken** | Looks wrong on paper | Page 2 header TIN `00012345300000` crushed on far left colliding into `SANTOS, JUANA...`; Page 2 Sched 1 rows show `0.00` (blank ATC/rate) yet `TOTAL TAX DUE` = `20.00`. |
| 34 | **2000OT** | 2 / 2 (frozen HTML) | **clean** | Cosmetic | Exact 2-page match; Part II (`51,500.00`) & Schedule 1.A/2 (`3,500,000.00`) crisp (Item 7 name not comb-spaced; unused Sched 1.B prints `0.00`). |
| 35 | **2552** | 2 / 2 (frozen HTML) | **tweak** | Return cannot be completed | Print layout clean on both pages (unused cells print `0.00`, Sched 1 empty rows print `6/10 OF 1%`); on `origin/main` (`51609c0b`, before #323), Item 17 is locked for amended returns. |
| 36 | **2553** | 1 / 1 (frozen HTML) | **broken** | Looks wrong on paper | Item 11 address microscopic & clipped (`...MAKATI CITY`); Part II amounts (`1,000.00`, `-1,000.00`, `0.00`) left-aligned inside decimal-dotted boxes ignoring the pre-printed `.` separator. |
| 37 | **2200A** | 3 / 3 (frozen HTML) | **broken** | Wrong number filed / Looks wrong on paper | On `origin/main` (before #323), Others row 1 tax due stays `0.00` (`87,440.56` vs `87,451.56`); Pages 2–3 header TIN crushed into Name (`00012345300000SANTOS...`); Items 10–11 print raw PSGC codes (`130000000`...) bleeding across Region→Province. |
| 38 | **2200AN** | 2 / 2 (frozen HTML) | **tweak** | Looks wrong on paper | Totals (`1,592,000.11`) & Region/Province/City names clean; Page 2 Sched 1B empty Others row 2 prints doubled `XGXG`; unused rows print `0.00`. |
| 39 | **2200C** | 2 / 2 (frozen HTML) | **broken** | Looks wrong on paper | Page 2 header TIN crushed into Name (`00012345300000SANTOS...`); Item 11 prints raw PSGC codes (`130000000`...) bleeding across Region→Province; all 100 empty Sched 1 cells print `0.00`. |
| 40 | **2200M** | 2 / 2 (frozen HTML) | **broken** | Wrong number filed / Looks wrong on paper | Page 2 Sched 1 continuation Col L rows sum to `102,222.68` (`XM060` Others 1–2 print `0.00` despite `5.01`/`120.00` in Col F), yet `TOTAL EXCISE TAX DUE` = `107,664.37` (`5,441.69` discrepancy on paper); `XM060` top descriptions microscopic. |
| 41 | **2200P** | 2 / 2 (frozen HTML) | **broken** | Looks wrong on paper | Page 2 header TIN crushed into Name (`00012345300000SANTOS...`); Items 10–11 print raw PSGC codes (`130000000`...) bleeding across Region→Province; Sched 1 text tiny; unused cells print `0.00`. |
| 42 | **2200S** | 2 / 2 (frozen HTML) | **broken** | Looks wrong on paper | Page 2 Schedule 1 **drops every single line item** (`XB010`–`XB100` & Others all blank) while printing `GRAND TOTAL EXCISE TAX DUE = 135,277.02`; Item 13 Region truncates `REGION IV-A` to `REG`. |
| 43 | **2200T** | 3 / 3 (frozen HTML) | **broken** | Looks wrong on paper | Visible Schedule 1 rows sum to `60,163.47` (`60,030.01 + 123.46 + 10.00`) vs printed `TOTAL TAX DUE = 60,413.47` (`250.00` missing from `2024 Onwards` row); Page 3 Others `XT999` overlaps `XT` prefix; unused rows print `0.00`. |

---

## Systemic Patterns Across All 43 Forms (Ranked by Harm)

1. **Wrong number filed (on `origin/main` `51609c0b`)**
   - **Whole-peso `.00` 100× shift on paper**: `1702Q` Part II (every amount prints `.00` inside whole-peso combs).
   - **Schedule → Part II / Total disconnects on paper**: `1600PT`, `1600VT`, `1600WP` (Schedule tax withheld never lands in Part II), `1606` (Schedule 1 FMV `5.7M` prints `TOTAL = 0.00`, understating Taxable Base by `700k`), `2000` (Sched 1 rows `0.00` vs Total `20.00`), `2200M` (Col L sum `102,222.68` vs Total `107,664.37`), `2200S` (all Sched 1 rows blank vs Grand Total `135,277.02`), `2200T` (visible rows sum `60,163.47` vs Total `60,413.47`).
   - **Known `origin/main` compute / locked-input bugs** (fixed on PRs #315, #323, `try/forms-1701-locked`): `2550M`, `1701`, `1701MS`, `2200A`, `2552`.
2. **Looks wrong on paper**
   - **4-digit year / `25` colliding with pre-printed `20` or `/20`** (8 forms): `1702Q`, `1702RT`, `1702EX`, `1702MX`, `1600PT`, `1600VT`, `1604C`, `1604E`.
   - **Page 2+ header TIN crushed on far left colliding into Name** (5 forms): `1701Q`, `2000`, `2200A`, `2200C`, `2200P`.
   - **Key Page 1 summary / ID boxes left blank** (3 forms): `1800` (Item 14 Net Gifts), `1801` (Item 5 TIN & Item 16 Net Taxable Estate), `1702MX` (Part II Items 14–16).
   - **Raw PSGC numeric codes bleeding across Region/Province/City** (3 forms): `2200A`, `2200C`, `2200P` (and `2200S` truncates `REGION IV-A` to `REG`).
   - **Registered address clipped or shrunk to microscopic font** (9 forms): `2550M`, `0605`, `1702EX`, `1604E`, `1604F`, `1606`, `1706`, `1600WP`, `2553`.
   - **Missing official pages / omitted reference tables** (8 forms): `0605` (1/2), `1702Q` (2/3), `1601EQ`, `2551Q`, `1601C`, `1701`, `1701A`, `1701Q`.
   - **Left-aligned amounts in decimal-dotted or right-aligned boxes**: `2550M`, `0605`, `1600WP`, `2553`, `1604C`, `1604E`, `1604F`.
3. **Cosmetic**
   - Unused amount boxes printing `0` / `0.00` (widespread; cleanly blank on `1701A`, `1700`), slightly bold `00000` over pre-printed branch codes (`1701A`, `1700`, `1707A`, `1800`, `1702*`), and minor comb-tick drift on long names.

*Evidence for all 43 forms lives under `form-review/eyes/<CODE>/compare-pN.png` and `ours-pN.png`.*

---

## Round 2 — Part A (12 Forms Re-Verified with Consistent Returns)

**Summary (12 forms on `origin/main` `51609c0b`, demo taxpayer Juana Santos `000-123-453-00000`, dry-run/test env only, 0 code changes):**
- **`WRONG IN THE DATA` (0):** none of the 12 forms file a wrong number when entered consistently.
- **`WRONG ON PAPER ONLY` (6):** **`2200S`**, **`2200T`**, **`1800`**, **`1801`**, **`1702MX`**, **`1702Q`**. Each has a `<CODE>-flow.mp4` recording (<2 min, app window + rendered print preview), ~1,400 px `screen-crop.png` and `print-crop.png`, and `README.md` under `form-review/eyes/round2/<CODE>/`.
- **`NOT A FAULT` (6):** **`1600PT`**, **`1600VT`**, **`1600WP`**, **`1606`**, **`2000`**, **`2200M`**. Each has ~1,400 px `screen-crop.png` and `print-crop.png` under `form-review/eyes/round2/<CODE>/`.
- **Separate Q5 finding (invalid dependent entries allowed):** on `1600PT`, `1600VT`, and `1600WP`, the app/agent path accepts Schedule 1 / Schedule 1.1 payee rows even while Item 3 / Item 4 (`Any Tax Withheld?`) is `No`, whereas the official BIR program refuses schedule rows when Tax Withheld is `No`.

| # | Form | Classification | One-line reason | Evidence files (`form-review/eyes/round2/<CODE>/`) |
|---|---|---|---|---|
| 1 | **1600PT** | **NOT A FAULT** | With Item 3 = Yes, Item 10 = Government, ATC `WB030` (`100,000 × 3% = 3,000.00`), Part II and totals match across screen, saved XML data, and PDF; Batch 3 had Item 3 = No. *(Q5: Schedule 1 accepts rows while Item 3 = No.)* | `screen-crop.png`, `print-crop.png` |
| 2 | **1600VT** | **NOT A FAULT** | With Item 3 = Yes, Item 10 = Private, ATC `WV050` (`100,000 × 12% = 12,000.00`), Part II and totals match across screen, saved XML data, and PDF; Batch 3 had Item 3 = No. *(Q5: Schedule 1 accepts rows while Item 3 = No.)* | `screen-crop.png`, `print-crop.png` |
| 3 | **1600WP** | **NOT A FAULT** | With Item 4 = Yes, Item 7 = Private, ATC `WB194` (`100,000 × 10% = 10,000.00`), Part II Item 12/14/16 all match across screen, saved XML data, and PDF; Batch 3 had Item 4 = No. *(Q5: `form.fill` accepts Schedule 1.1 rows while Item 4 = No.)* | `screen-crop.png`, `print-crop.png` |
| 4 | **1606** | **NOT A FAULT** | With Cash Sale and FMVs (`TD 3M+1.5M=4.5M` vs `Zonal 4.2M+0=4.2M`), Schedule 1 TOTAL (`4,500,000.00`), Schedule 3 Item 1B, and Part II Item 12 match across screen, XML, and PDF; `4.5M` vs `5.7M` mirrors the official HTA's `compareFMVLI` (`calculations.json:20-43`). | `screen-crop.png`, `print-crop.png` |
| 5 | **2000** | **NOT A FAULT** | With ATC `DS101` selected and Tax Base `100,000.00`, Schedule 1 Tax Due (`1,000.00`), TOTAL TAX DUE (`1,000.00`), and Part II Item 14 match across screen, XML, and PDF; Batch 3 had left ATC unset (`-`). | `screen-crop.png`, `print-crop.png` |
| 6 | **2200M** | **NOT A FAULT** | Official BIR `computeTotalTaxDue` (`calculations.json:43-63`, `incorrect-official-behavior`) sums Col F (`LocallyExtractedTaxDueF`) and leaves Col L (`TotalTaxDueL`) as a separate filer-typed box, which the app mirrors identically in XML and PDF. | `screen-crop.png`, `print-crop.png` |
| 7 | **2200S** | **WRONG ON PAPER ONLY** | Saved data holds `beverages` (`XB010` `74,074.02`, `XB030` `60,003.00`, etc.) and `schedule_total = 135,277.02`, but Page 2 Schedule 1 prints every row (`XB010`–`XB100` & Others) completely blank above `GRAND TOTAL = 135,277.02`. | `2200S-flow.mp4`, `screen-crop.png`, `print-crop.png`, `README.md` |
| 8 | **2200T** | **WRONG ON PAPER ONLY** | `2200T v2020` data holds `txtSched1_5_1.23.2020_Due = 250.00` (and `4B_2023 = 60,030.01`, etc., `schedule_total = 60,413.47`), but the August 2022 print sheet omits 2020/2021 rows, leaving a `250.00` gap between visible rows (`60,163.47`) and printed `TOTAL TAX DUE` (`60,413.47`). | `2200T-flow.mp4`, `screen-crop.png`, `print-crop.png`, `README.md` |
| 9 | **1800** | **WRONG ON PAPER ONLY** | Saved data holds `net_gifts_subject_to_tax = 1,000,000.00` (`1,250,000 − 250,000`) and `tax_due = 60,000.00`, but Page 1 Part II prints Item 14 completely blank while Item 16 prints `60,000.00`. | `1800-flow.mp4`, `screen-crop.png`, `print-crop.png`, `README.md` |
| 10 | **1801** | **WRONG ON PAPER ONLY** | Saved data holds `tin = 00012345300000`, `net_taxable_estate = 10,000,000.00` (`15M − 5M`), and `tax_due = 600,000.00`, but Page 1 prints Item 5 TIN (digits 1–9), Item 16 (`NET TAXABLE ESTATE`), and Item 24 (`TOTAL AMOUNT PAYABLE`) blank while Item 18 prints `600,000.00`. | `1801-flow.mp4`, `screen-crop.png`, `print-crop.png`, `README.md` |
| 11 | **1702MX** | **WRONG ON PAPER ONLY** | With Item 13 = `Itemized`, saved data holds Part II `item_14 = -1,000`, `item_15 = 78,000`, `item_16 = -79,000`, `item_21 = -79,000`, but Page 1 prints Items 14, 15, and 16 blank while printing Item 21 `-79,000`. | `1702MX-flow.mp4`, `screen-crop.png`, `print-crop.png`, `README.md` |
| 12 | **1702Q** | **WRONG ON PAPER ONLY** | Saved data holds whole-peso `875,000` (aggregate `932,000`, net payable `738,265`, total `1,062,782`), but Page 1 Part II prints `.00` inside whole-peso combs (shifting digits left across boxes) and doubled commas on Item 25. | `1702Q-flow.mp4`, `screen-crop.png`, `print-crop.png`, `README.md` |

### Per-Form Round 2 Part A Details (Choices, Screen / XML Data / Print, Formula & Rule Citation, Q5)

1. **1600PT** (`NOT A FAULT`): Choices: Period `03/2025`, Item 3 `Any Tax Withheld = Yes`, Item 10 `Category = Government`, Part II ATC `WB030` (`3.0%`), Tax Base `100,000.00`. Screen = `3,000.00` (Item 18/22), `5,335.86` (Item 27 w/ penalties). Saved XML data (`txtAtcCd1=WB030`, `txtPg1P2TaxBase1=100,000.00`, `txtPg1P2TaxWithheld1=3,000.00`, `txtPg1P2I18TotTaxWithheld=3,000.00`). Print/PDF = `WB030 | 100,000.00 | 003% | 3,000.00`, Item 18 `3,000.00`, Item 22 `3,000.00`, Item 27 `5,335.86`. Expected: `100,000.00 × 3% = 3,000.00` (`rules/forms/1600pt-v2018/calculations.json` lines 2, 4, 6). **Q5**: setting Item 3 = `No` still allowed `form.fill` to populate Schedule 1 (`Pg2Sc1TIN1`/`Name1`/`ATC1`/`AmtOfIncPmt1`).
2. **1600VT** (`NOT A FAULT`): Choices: Period `03/2025`, Item 3 `Yes`, Item 10 `Private`, Part II ATC `WV050` (`12.0%`), Tax Base `100,000.00`. Screen = `12,000.00` (Item 18/22), `22,343.45` (Item 27). Saved XML data (`txtAtcCd1=WV050`, `txtPg1P2TaxBase1=100,000.00`, `txtPg1P2TaxWithheld1=12,000.00`, `txtPg1P2I18TotTaxWithheld=12,000.00`). Print/PDF = `WV050 | 100,000.00 | 0012% | 12,000.00`, Item 18/22 `12,000.00`, Item 27 `22,343.45`. Expected: `100,000.00 × 12% = 12,000.00` (`rules/forms/1600vt-v2018/calculations.json` lines 2, 4, 6). **Q5**: setting Item 3 = `No` still allowed `form.fill` to populate Schedule 1.
3. **1600WP** (`NOT A FAULT`): Choices: Period `11/2025`, Item 4 `Any Taxes Withheld = Yes`, Item 7 `Private`, Part II Row 1 ATC `WB194` (`10%`), Tax Base `100,000.00`. Screen = `10,000.00` (Items 12/14/16). Saved XML data (`AnyTaxHeld_1=true`, `CategoryAgent_P=true`, `txtAtcCode1=WB194`, `txtTaxBase1=100,000.00`, `txtTax12=10,000.00`). Print/PDF = `WB194 | 100,000.00 | 10% | 10,000.00`, Items 12/14/16 `10,000.00`. Expected: `100,000.00 × 10% = 10,000.00` (`rules/forms/1600wp-2010/calculations.json`). **Q5**: while the form page gates Schedule 1.1 on Item 4 = Yes, `form.fill` accepted Schedule 1.1 rows (`dtSched:txtTin1`/`amount1`) while `AnyTaxHeld_2 = true` (No).
4. **1606** (`NOT A FAULT`): Choices: Period `07/2025`, `txtGross=4,000,000.00`, `txtFMVLand=3,000,000.00`, `txtFMVImprovements=1,500,000.00`, `txtFMVZonal=4,200,000.00`, `txtFMVBIR=0.00`. Screen, XML (`txtFMVLI=4,500,000.00`, `txtTax=4,500,000.00`), and Print/PDF (Schedule 1 TOTAL `4,500,000.00`, Schedule 3 Item 1B `4,500,000.00`, Item 2 `4,500,000.00`, Part II Item 12 `4,500,000.00`) all agree. Expected per official HTA: `max(27A+27B, 27C+27D) = max(4.5M, 4.2M) = 4,500,000.00` (`rules/forms/1606-v2018/calculations.json` lines 20–43, `compareFMVLI`, `assessment: "incorrect-official-behavior"`).
5. **2000** (`NOT A FAULT`): Choices: Period `04/2025`, Schedule 1 Row 1 ATC `DS101`, Tax Base `100,000.00`. Screen, XML (`txtSched1TaxDue0=1,000.00`, `txtTotalTaxDue=1,000.00`, Item 14 `1,000.00`), and Print/PDF (`DS101 | 100,000.00 | 1,000.00`, `TOTAL TAX DUE = 1,000.00`) all agree. Expected: `100,000.00 × 1% = 1,000.00` (`rules/forms/2000-v2018/calculations.json` lines 690–699).
6. **2200M** (`NOT A FAULT`): Choices: Period `05/2025`, Row 1 (`XM010`) Place `PASIG YARD`, Col A `1,000.00`, Col F `10,000.00`. Screen, XML (`txtSched1_LocallyExtractedTaxDueF1=10,000.00`, `TotalExciseTaxDue=10,000.00`, `txtPg1P3I16ExciseTaxDue=10,000.00`, `TotalTaxDueL1=0.00`), and Print/PDF all agree. Expected per official HTA: `computeTotalTaxDue` sums Col F only and leaves Col L uncomputed (`rules/forms/2200m-v2018/calculations.json` lines 43–73, `assessment: "incorrect-official-behavior"`).
7. **2200S** (`WRONG ON PAPER ONLY`): Choices: Period `06/2025`, Schedule 1 `XB010` (`98,765.43` / `12,345.67 L` → `74,074.02`), `XB030` (`10,000.50 L` → `60,003.00`), plus Others (`schedule_total = 135,277.02`). Screen & XML hold all `beverages` rows and `schedule_total = 135,277.02` (`rules/forms/2200s-v2018/calculations.json` lines 69–100). Print/PDF prints every Schedule 1 row (`XB010`–`XB100` & Others) blank while printing `GRAND TOTAL EXCISE TAX DUE = 135,277.02`.
8. **2200T** (`WRONG ON PAPER ONLY`): Choices: Period `06/2025`, Schedule 1 `4B_2023` (`60,030.01`), `5_1.23.2020` (`10 × P25 = 250.00`), `123.46`, Others `10.00` → `schedule_total = 60,413.47`. Screen & XML hold all rows and `txtSched1_TotalDue = 60,413.47` (`rules/forms/2200t-v2020/calculations.json` lines 19–28). Print/PDF uses the August 2022 sheet (no 2020/2021 rows), so `250.00` disappears on paper while `TOTAL TAX DUE` prints `60,413.47`.
9. **1800** (`WRONG ON PAPER ONLY`): Choices: TY `2025`, Schedule A Personal Property `CASH GIFT` FMV `1,250,000.00`. Screen & XML hold `net_gifts_subject_to_tax = 1,000,000.00` (`1,250,000 − 250,000`) and `tax_due = 60,000.00` (`1,000,000 × 6%`, `rules/forms/1800-v2018/calculations.json` lines 167–197). Print/PDF prints Page 1 Item 14 completely blank while Item 16 prints `60,000.00`. *(Q5 note: on a blank 1800 with `0` gifts, `0 − 250,000 = -250,000` prints `-15,000.00` tax due.)*
10. **1801** (`WRONG ON PAPER ONLY`): Choices: TY `2025`, Schedule 1 Exclusive Real Property `15,000,000.00`, Standard Deduction `5,000,000.00`. Screen & XML hold `tin = 00012345300000`, `net_taxable_estate = 10,000,000.00`, `estate_tax_due = 600,000.00` (`10,000,000 × 6%`, `rules/forms/1801-v2018/calculations.json` lines 30–64, 229–383). Print/PDF prints Page 1 Item 5 TIN (digits 1–9), Item 16 (`NET TAXABLE ESTATE`), and Item 24 (`TOTAL AMOUNT PAYABLE`) blank while Item 18/20/22 print `600,000.00`.
11. **1702MX** (`WRONG ON PAPER ONLY`): Choices: TY `2025`, Item 13 `Method of Deduction = Itemized`, Schedule 2 sales populated. Screen & XML hold Part II `item_14 = -1,000`, `item_15 = 78,000`, `item_16 = -79,000`, `item_21 = -79,000` (`rules/forms/1702mx-v2018c/calculations.json` lines 72–125). Print/PDF prints Page 1 Items 14, 15, and 16 completely blank while printing Item 21 `-79,000`.
12. **1702Q** (`WRONG ON PAPER ONLY`): Choices: Q2 `2025`, regular income tax due `875,000`, special `57,000`, aggregate `932,000`, credits `193,735`, net payable `738,265`, penalties `324,517`, total payable `1,062,782`. Screen & XML hold exact whole-peso integers (`rules/forms/1702q-v2018c/calculations.json` lines 424–432, 519–623). Print/PDF prints `.00` inside whole-peso combs (shifting every Part II value left across boxes) and doubled commas on Item 25.

---

## Round 2 — Part B (Year-Collision Verification Across 8 Forms)

Tight side-by-side crops (official sheet left, our print right, 1,400 px wide) under `form-review/eyes/round2/part-b/<CODE>-year.png`:

**Summary:** **6 withdrawn** (`1702Q`, `1702RT`, `1702EX`, `1702MX`, `1600PT`, `1600VT`), **2 confirmed** (`1604C`, `1604E`).

| Form | Crop | Plain reading of our print | Verdict |
|---|---|---|---|
| **1702Q** | `part-b/1702Q-year.png` | `1 2 / 2 0 2 5` (two-digit `2 5` sits cleanly in the two slots after `/20`) | **WITHDRAWN** |
| **1702RT** | `part-b/1702RT-year.png` | `1 2 / 2 0 2 5` (clean in the two slots after `/20`) | **WITHDRAWN** |
| **1702EX** | `part-b/1702EX-year.png` | `1 2 / 2 0 2 5` (clean in the two slots after `/20`) | **WITHDRAWN** |
| **1702MX** | `part-b/1702MX-year.png` | `1 2 / 2 0 2 5` (clean in the two slots after `/20`) | **WITHDRAWN** |
| **1600PT** | `part-b/1600PT-year.png` | `0 6 | 2 0 2 5` (clean in the two slots after pre-printed `2 0`) | **WITHDRAWN** |
| **1600VT** | `part-b/1600VT-year.png` | `0 6 | 2 0 2 5` (clean in the two slots after pre-printed `2 0`) | **WITHDRAWN** |
| **1604C** | `part-b/1604C-year.png` | Unspaced `2025` overprints the pre-printed bold `2` left of `0`, leaving the two `YY` slots blank (reads as garbled `225 0`) | **CONFIRMED** |
| **1604E** | `part-b/1604E-year.png` | Unspaced `2025` overprints the pre-printed bold `2` left of `0`, leaving the two `YY` slots blank (reads as garbled `225 0`) | **CONFIRMED** |
