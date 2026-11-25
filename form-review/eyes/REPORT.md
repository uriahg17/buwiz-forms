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

---

## Round 2 — Part C (All-43-Form Paper-Pattern Inventory)

Checked form by form across all 43 rendered PDFs (`ours-p*.png` / `*-ours.pdf`), official PDFs, and `rules/forms/*/fields.json`.

### 1. Continuation-page header where TIN runs into Name
- **4 forms (5 pages)** where unspaced 14-digit TIN touches the taxpayer's Last Name (`gap < 1 pt`):
  - **2000** — Page 2 (`gap = 0.7 pt`)
  - **2200A** — Pages 2, 3 (`gap = 0.7 pt`)
  - **2200C** — Page 2 (`gap = 0.8 pt`)
  - **2200P** — Page 2 (`gap = 0.8 pt`)
- *Related continuation-header TIN fault (does not touch Name)*: **1701Q** Page 2 crushes the 9-digit TIN on the far left beside an empty pre-printed `00000` branch box.

### 2. Raw place codes (PSGC) instead of place names
- **3 forms (all Page 1)** print 9-digit PSGC numeric codes instead of Region / Province / City names (bleeding across the boxes):
  - **2200A** — Page 1 (Items 12A–C `040000000`, `042100000`, `042103000`; Items 13A–C `130000000`, `137400000`, `137403000`)
  - **2200C** — Page 1 (Items 12A–C / 13A–C `130000000`, `137400000`, `137404000`)
  - **2200P** — Page 1 (Items 12A–C `040000000`, `042100000`, `042103000`; Items 13A–C `130000000`, `137400000`, `137403000`)
- *(Note: `2200S` Page 1 prints the text name, not a PSGC code, though Item 13 Region truncates `REGION IV-A` to `REG`; `2200AN`, `2200M`, `2200T` show no PSGC codes.)*

### 3. Registered name or address clipped or under 7.5 pt (measured PDF font size)
**10 forms** (all Page 1; demo taxpayer address is 142 chars):

| Form | Name (pt) | Address (pt) | Clipped? | What is cut off / observed |
|---|---:|---:|---|---|
| **0605** | 13.98 | **6.70** | **Yes** | Address `< 7.5 pt` and cut off at `...METRO M` |
| **1600WP** | 10.75 | 7.90 | **Yes** | Address cut off at `...METRO` |
| **1604E** | 10.08 | 10.08 (comb) | **Yes** | Comb address cut off at `...845 ARNAIZ AV` |
| **1604F** | 9.28 | 9.28 (comb) | **Yes** | Comb address cut off at `...845 ARNAIZ AV` |
| **1606** | **6.70** | **4.80** | **Yes** | Both Buyer Name (`6.70 pt`) & Address (`4.80 pt`) `< 7.5 pt`; address cut off at `...METRO` |
| **1702EX** | 12.00 | 12.00 (comb) | **Yes** | Comb address cut off at `...SAN LOREN` |
| **1706** | **6.70** | **4.69** | **Yes** | Both Name (`6.70 pt`) & Address (`4.69 pt`) `< 7.5 pt`; address cut off at `...METRO` |
| **1707** | 10.72 | **5.20** | No | Seller/Buyer addresses shrink to `5.20 pt` (`< 7.5 pt`) |
| **2550M** | 11.00 | **7.30** | **Yes** | Address `< 7.5 pt` and cut off at `...METRO MAN` |
| **2553** | 13.12 | 7.50 | **Yes** | Address cut off before `METRO MANILA` |

All other 33 forms render the demo name and address at `>= 7.5 pt` without clipping.

### 4. Amounts not right-aligned
**21 forms** have at least one numeric amount column left-aligned instead of right-aligned (verified by PDF charbox x-alignment across stacked amounts plus visual inspection for single-row/comb pages):
- **Page 1**: `0605` (Part II Items 20A–20D), `1600WP` (Part II), `1604C` (Part II), `1604E` (Part II), `1604F` (Part II), `1702Q` (Part II whole-peso combs shifted left with `.00`), `2550M` (Part II), `2553` (Part II).
- **Page 2**: `1600PT` (Sched 1), `1600VT` (Sched 1), `1606` (Sched 1), `1707A` (Sched 1), `1800` (Sched A), `1801` (Sched 1–4), `2000OT` (Sched 1), `2200A` (Sched 1), `2200AN` (Sched 1), `2200M` (Sched 1), `2200P` (Sched 1), `2200T` (Sched 1), `2550Q` (Part V Sched 1–4).
- **Page 3**: `2200A` (Sched 1 cont.), `2200T` (Sched 1 cont.).

### 5. Unused boxes printing `0` or `0.00` (compared with official BIR defaults)
- **All 43 forms** print `0` or `0.00` in unused numeric boxes on our rendered PDFs (from `3` boxes on `0605` up to `194` on `2200A` and `126` on `1701`).
- **Comparison against official BIR program defaults (`rules/forms/*/fields.json`)**:
  - **40 of 43 forms** initialize their amount fields to `0.00` or `0` in the official eBIRForms HTA itself (37 forms default to `0.00`, 3 whole-peso forms — `1700`, `1702MX`, `1702RT` — default to `0`, plus `1707A` with 4 default-`0` fields). On those 40 forms, printing `0` / `0.00` in unused numeric boxes **matches what the official BIR program prints** when left untouched.
  - **3 forms** have **no** `0` / `0.00` defaults in `rules/forms/*/fields.json` (blank at load in official eBIRForms), yet our print fills unused boxes with zeros: **`1701MS`** (31 zeros), **`2550Q`** (92 zeros, mainly Part V Schedules 1–4), and **`2551Q`** (17 zeros, e.g. Items 16–17).

### 6. Missing pages and omitted sections (8 forms)
Every missing page or omitted section across the 8 forms was checked directly against the official BIR PDF. **All 8 are reference tables / guidelines only — none contain any filer-entered fields:**

| Form | Missing / omitted part | Official PDF content | Filer-entered content? |
|---|---|---|---|
| **0605** | Page 2 (entire page; 1 vs 2 pages) | `ATC / NATURE OF PAYMENT` lookup table + `Guidelines and Instructions` | **No** (reference & guidelines only) |
| **1702Q** | Page 3 (entire page; 2 vs 3 pages) | `ATC / Description / Tax Rate / Tax Base` table + `Guidelines and Instructions for BIR Form No. 1702Q` | **No** (reference & guidelines only) |
| **1601EQ** | Page 2 body (~85% blank below header) | `Schedule of Alphanumeric Tax Codes (ATC)` (Nature of Income Payment & Tax Rate) | **No** (reference table only) |
| **2551Q** | Page 2 bottom (~70% blank below Sched 1) | `Table 1 – Alphanumeric Tax Code (ATC)` (Percentage Tax On & Tax Rate) | **No** (reference table only) |
| **1601C** | Page 2 bottom (~70% blank below Sched I) | `Guidelines and Instructions for BIR Form No. 1601-C` | **No** (guidelines only) |
| **1701** | Page 4 bottom | `TABLE 1 – Tax Rates (Jan 1, 2018 – Dec 31, 2022)` & `TABLE 2 – Tax Rates (Jan 1, 2023 and onwards)` | **No** (reference tables only) |
| **1701A** | Page 2 bottom | `TABLE 1` & `TABLE 2 – Tax Rates` | **No** (reference tables only) |
| **1701Q** | Page 2 bottom | `TABLE 1` & `TABLE 2 – Tax Rates` | **No** (reference tables only) |

---

## Round 3 — Full data-vs-paper audit (`origin/main` `93820d0f` vs `origin/feat/store-launch-field-rules` `8c3a7b53`)

### Batch 1 — First 10 priority forms (`2551Q`, `1701Q`, `1701`, `1701A`, `2550Q`, `2550M`, `1601C`, `0619E`, `1601EQ`, `0605`)

Every editable box, schedule row, spouse column, and mutually exclusive mode (`1701` joint itemized + OSD; `1701A` graduated + 8%; `1701Q` graduated + 8%) was filled with distinct traceable values through the form page, saved, printed to preview and PDF on both `origin/main` (`93820d0f`) and `origin/feat/store-launch-field-rules` (`8c3a7b53`), and checked both by machine and by eye on every page. Zero application code was changed.

**Clean on both commits (0 data-vs-paper mismatches)**: **`0619E`**, **`1601EQ`**, **`2551Q`**, **`1701Q`** (both `grad` and `8pct`).

**Mismatches found (6 forms)**:

| Form | Page | Box / Item | Data value | Printed on `main` (`93820d0f`) | On `main`? | On `rules` (`8c3a7b53`)? | Cause on `main` (file & entry) | Evidence (`form-review/eyes/round3/<CODE>/`) |
|---|---|---|---|---|---|---|---|---|
| **1701** | p1 | Part II Item 23A (`Total Tax Credits/Payments`) | `1,234,772,698` | Blank (empty 9-slot comb) | **yes** | **no** (`1,234,772,698`) | Value overflows 9-slot comb and is dropped: `crates/bir-print/src/frozen_html.rs:2632-2635` (`right_aligned_slot_values`: `if digits.len() > slots { return None; }`). | `main/p1-compare.png`, `rules/p1-compare.png`, `1701-flow.mp4` |
| **1701** | p1 | Part II Items 24A, 26A, 31A (`Tax Payable/(Overpayment)`) | `-803,331,202` | Blank (empty 9-slot comb; 10 chars with `-`) | **yes** | **no** (`(803,331,202)`) | Same comb overflow drop (`frozen_html.rs:2632-2635`, `signed_digits` emits `-803331202` = 10 chars > 9 slots). | `main/p1-compare.png`, `rules/p1-compare.png`, `1701-flow.mp4` |
| **1701** | p1 | Part II Item 32 (`Aggregate Amount Payable/(Overpayment)`) | `-803,566,841` | Blank (empty 9-slot comb) | **yes** | **no** (`(803,566,841)`) | Same comb overflow drop (`frozen_html.rs:2632-2635`). | `main/p1-compare.png`, `rules/p1-compare.png`, `1701-flow.mp4` |
| **1701** | p2 | Part IV Item 1 (`Spouse's TIN` branch code) | `000-987-654-00001` (`spouse.tin = "00098765400001"`) | `0 0 0 - 9 8 7 - 6 5 4 - 0 0 0 0 0` (branch prints `00000`) | **yes** | **yes** (still prints `00000`) | No cell for `frm1701:txtPg2I1BranchCode` in `html-frozen/1701-2018/writer-cells.json`; branch `0 0 0 0 0` is preprinted on the sheet. | `main/p2-compare.png`, `rules/p2-compare.png`, `1701-flow.mp4` |
| **1701** | p2 | Part V Sched 3.A Items 8A, 10A, 12A, 18A, 23A, 24A (6 boxes) | `1,234,567,890` .. `1,234,397,708` | Blank (all 6 empty 9-slot combs) | **yes** | **no** (all 6 print cleanly) | Same 9-slot comb overflow drop (`crates/bir-print/src/frozen_html.rs:2632-2635`). | `main/p2-sched3-compare.png`, `rules/p2-sched3-compare.png`, `1701-flow.mp4` |
| **1701** | p4 | Part VII Items 8A, 10A (2 boxes) | `1,234,567,890`, `1,234,772,698` | Blank (both empty 9-slot combs) | **yes** | **no** (both print cleanly) | Same 9-slot comb overflow drop (`crates/bir-print/src/frozen_html.rs:2632-2635`). | `main/p4-compare.png`, `rules/p4-compare.png`, `1701-flow.mp4` |
| **1701A** | p2 (add'l) | Part IV.B `Other Non-Operating Income` modal rows (`txtmodalPartIVBDesc_1C1..12C1` & `txtmodalPartIVB_1C2..12C2`, 24 values; both `grad` and `8pct`) | `V110`–`V121`, `22,234.00`–`23,345.00` | Omitted (only 2 pages printed) | **yes** | **no** (appended on Pages 3–4 `Add'l Sheet`, though right column prints stray `0 . 0 0` combs beside each amount) | No cells for `frm1701A:txtmodalPartIVB*` in `html-frozen/1701a-2018/writer-cells.json` and no continuation-sheet emitter on `main`. | `main/compare.png`, `rules/compare.png`, `1701A-flow.mp4` |
| **2550Q** | p1–p2 (add'l) | Attached-modal schedules Items 19, 42, 47, 56 (`totalTaxPayableNo{19,42,47,56}{Description,Amount}*`, 51 pairs = 102 values) | Distinct descriptions & amounts (sum `200,923.32` on Item 19) | Item 19 prints `VARIOUS` + sum; all 51 itemized rows omitted (2 pages) | **yes** | **yes** (still 2 pages, no detail sheet) | No cells for `frm2550q:totalTaxPayableNo{19,42,47,56}*` in `html-frozen/2550q-2024/writer-cells.json` and no continuation-sheet emitter on either commit. | `main/compare.png`, `rules/compare.png`, `2550Q-flow.mp4` |
| **1601C** | p1 | Item 5 (`ATC`) | `draft.atc = "V004"` (accepted by `form.fill`) | Preprinted `WW010` | **yes** | **yes** (prints `WW010`) | `html-frozen/1601c-2018/writer-cells.json` `not_joined` entry `frm1601c:txtATC` ("item 5 ATC is preprinted WW010 on the sheet; there is no box to fill"). | `main/compare.png`, `rules/compare.png`, `1601C-flow.mp4` |
| **0605** | p1 | Item 15 (`Registered Address`) | 123-char demo address (`...METRO MANILA`) | Clipped at `...METRO M` | **yes** | **no** (wraps onto 2 lines, full `METRO MANILA` shown) | Single-line `overflow:hidden` text cell in `html-frozen/0605-1999/sheet.html` / `frozen_html.rs` on `main`. | `main/compare.png`, `rules/compare.png`, `0605-flow.mp4` |
| **2550M** | p1 | Item 9 (`Registered Address`) | 123-char demo address (`...METRO MANILA`) | Clipped at `...METRO MAN` | **yes** | **no** (Page 1 shortens to `...ROXA...` and Page 3 `ADDITIONAL SHEET` prints full address; header shows `Taxpayer's Name: —`) | Single-line `overflow:hidden` text cell in `html-frozen/2550m-2007/sheet.html` on `main`. | `main/compare.png`, `rules/compare.png`, `2550M-flow.mp4` |

**Recordings committed (Batch 1)**:
- `form-review/eyes/round3/0605/0605-flow.mp4`
- `form-review/eyes/round3/1601C/1601C-flow.mp4`
- `form-review/eyes/round3/1701/1701-flow.mp4`
- `form-review/eyes/round3/1701A/1701A-flow.mp4`
- `form-review/eyes/round3/2550M/2550M-flow.mp4`
- `form-review/eyes/round3/2550Q/2550Q-flow.mp4`

---

### Batch 2 — Remaining 33 forms (`origin/main` `93820d0f` vs `origin/feat/store-launch-field-rules` `8c3a7b53`)

**Clean on both commits (0 data-vs-paper mismatches, 8 forms)**: **`0619F`**, **`1601FQ`**, **`1603Q`**, **`1700`**, **`2200AN`**, **`2200C`**, **`2552`**, **`2553`**.

**Mismatches found (25 forms)**:

| Form | Page | Box / Item(s) | Data vs Printed on `main` (`93820d0f`) | On `main`? | On `rules` (`8c3a7b53`)? | Cause on `main` (file & entry) | Evidence (`form-review/eyes/round3/<CODE>/`) |
|---|---|---|---|---|---|---|---|
| **1600PT** | p1–p2 | 93 Part II / Sched 1 ATC, tax base & rate values (`txtAtcCd1..31`, `txtPg1P2TaxBase1..31`, `txtPg1P2TaxRate1..31`) | Present in data, absent from paper | **yes** | **yes** (93 absent) | No `writer-cells.json` for `1600pt-2018` (`crates/bir-print/src/frozen_html.rs` falls back to limited map) | `main/compare.png`, `rules/compare.png`, `1600PT-flow.mp4` |
| **1600VT** | p1–p2 | 39 Part II / Sched 1 ATC, tax base & rate values (`txtAtcCd1..13`, `txtPg1P2TaxBase1..13`, `txtPg1P2TaxRate1..13`) | Present in data, absent from paper | **yes** | **yes** (39 absent) | No `writer-cells.json` for `1600vt-2018` | `main/compare.png`, `rules/compare.png`, `1600VT-flow.mp4` |
| **1600WP** | p1 (add'l) | 12 Sched 1.1 overflow rows (`dtSched:{txtFullname,drpAtcCode,amount}7..10`) + 12 `txtTaxBase1..12` | All 24 absent on `main` (1 page) | **yes** | **partial** (12 `dtSched` rows print on p2–3 Add'l Sheet; 12 `txtTaxBase*` still absent) | `html-frozen/1600wp-2010/writer-cells.json` (`not_joined` `hPartIITableSize`, no overflow cells on `main`) | `main/compare.png`, `rules/compare.png`, `1600WP-flow.mp4` |
| **1602Q** | p2–p3 | 13 values (`txt24`, `txt25`, `txtSched1{Rate,Amount,TreatyCode,ATC,Interest}*`) | Present in data, absent from paper | **yes** | **yes** (11 absent; 2 `Rate` cells fixed) | `html-frozen/1602q-2019/writer-cells.json` (`not_joined_cells=105`) | `main/compare.png`, `rules/compare.png`, `1602Q-flow.mp4` |
| **1604C** | p1 | Item 1 (`For the Year (20YY)`) | `2025` overprints preprinted `20` (reads `225 0`) | **yes** | **yes** (still `225 0`) | `html-frozen/1604c-2018/writer-cells.json` maps full 4-digit year over preprinted `20` | `main/compare.png`, `rules/compare.png`, `1604C-flow.mp4` |
| **1604E** | p1 | Item 1 (`For the Year (20YY)`) & Item 7 (`Registered Address`) | Year reads `225 0`; address truncates at `...845 ARNAIZ AV` | **yes** | **yes** (both persist) | `html-frozen/1604e-2018/writer-cells.json` (4-digit year over `20` + fixed comb address length) | `main/compare.png`, `rules/compare.png`, `1604E-flow.mp4` |
| **1604F** | p1 | Item 7 (`Registered Address`) | 123-char address truncates at `...845 ARNAIZ AV` | **yes** | **yes** (still truncated) | Fixed comb length in `html-frozen/1604f-2018/sheet.html` | `main/compare.png`, `rules/compare.png`, `1604F-flow.mp4` |
| **1606** | p1–p2 | 5 fields (`j_id393_7`, `txtOthers`, `txtOthers20`, `txtGross`, `txtBid`) | Present in data, absent from paper | **yes** | **yes** (same 5 absent; p3–4 address Add'l Sheet added) | `html-frozen/1606-2018/writer-cells.json` (`not_joined=12`) | `main/compare.png`, `rules/compare.png`, `1606-flow.mp4` |
| **1701MS** | p1–p2 | 3 fields (`txtTaxDueAllowedNo26a`, `printedName`, `authorizeRepresentative`) | Present in data, absent from paper | **yes** | **yes** (same 3 absent) | `html-frozen/1701ms-2024/writer-cells.json` (`not_joined=8`) | `main/compare.png`, `rules/compare.png`, `1701MS-flow.mp4` |
| **1702EX** | p2–p3 (add'l) | 135 Sched 1 attached rows (`txtPg3Pt6S1I17_*`) + `txtPg2Pt4I40TaxRate` | All 136 absent on `main` (3 pages) | **yes** | **no** for 135 rows (appended on p4–11 Add'l Sheets); **yes** for `txtPg2Pt4I40TaxRate` | `html-frozen/1702ex-2018/writer-cells.json` (`not_joined=17`, no overflow cells on `main`) | `main/compare.png`, `rules/compare.png`, `1702EX-flow.mp4` |
| **1702MX** | p1–p4 | Part II Items 14–19 blank above Item 21 `(371,221)` + Item 10 Date of Inc. + 119 Sched 2–8 values (`both itemized & OSD`) | Present in data, blank on paper | **yes** | **yes** (same 119 absent; Part II Items 14–19 still blank) | `html-frozen/1702mx-2018c/writer-cells.json` (`not_joined=9`, `not_joined_cells=59`) | `main/compare.png`, `rules/compare.png`, `1702MX-flow.mp4` |
| **1702Q** | p1 | Part II Items 14–25 (whole-peso combs) | Prints `.00` shifted into whole-peso combs (`0 . 0 0` even at zero; 100× shift on non-zero) | **yes** | **yes** (still prints `. 0 0` in whole-peso combs) | `crates/bir-core/src/forms/form_1702q.rs` formats Part II with centavos into whole-peso comb cells | `main/compare.png`, `rules/compare.png`, `1702Q-flow.mp4` |
| **1702RT** | p2–p4 | 66 Part IV/V/Sched values (`txtPg2Pt452SpecialTaxCredits`, `txtPg2Pt5I57..58`, Sched 1–7 rows; `itemized & OSD`) | Present in data, absent from paper | **yes** | **yes** (same 66 absent) | `html-frozen/1702rt-2018c/writer-cells.json` (`not_joined=7`) | `main/compare.png`, `rules/compare.png`, `1702RT-flow.mp4` |
| **1706** | p1–p2 | `txtSellerRAddress`, `txtOthers`, `txtOthers21`, `txtBid` + 20 `txtSchedModal*` rows (24 values) | Present in data, absent from paper | **yes** | **yes** (25 absent; p3–4 address Add'l Sheet added) | `html-frozen/1706-2018/writer-cells.json` (`not_joined=14`, `not_joined_cells=90`, explicit `not_joined` `frm1706:txtSellerRAddress`) | `main/compare.png`, `rules/compare.png`, `1706-flow.mp4` |
| **1707** | p2 (add'l) | 122 Sched 2/3 overflow rows (`txtPg2Pt4S2_*`, `txtPg2P4Sch2NoOfShares*`) | All 122 absent on `main` (2 pages) | **yes** | **no** for 120 rows (appended on p3–8 Add'l Sheets); **yes** for 2 `NoOfShares` cells | `html-frozen/1707-2021/writer-cells.json` (`not_joined=10`, `not_joined_cells=29`, no overflow emitter on `main`) | `main/compare.png`, `rules/compare.png`, `1707-flow.mp4` |
| **1707A** | p2 | 135 Sched 1 transaction rows (`txtS1C1{DateOfTransaction,SellingPrice,Cost,TaxPaid}_*`) | Present in data, absent from paper | **yes** | **yes** (same 135 absent) | `html-frozen/1707a-2021/writer-cells.json` (`not_joined=57`, `not_joined_cells=30`) | `main/compare.png`, `rules/compare.png`, `1707A-flow.mp4` |
| **1800** | p1–p2 | **p1 Item 14** (`Total Net Gifts Subject to Tax`) blank above Item 16 `31,311.27`; **p2 Sched A/B** 135 overflow rows (`schedA:*`, `schedB:*`) | Item 14 blank + 135 Sched A/B rows absent on `main` (2 pages) | **yes** | **yes** for p1 Item 14 (still blank); **no** for 135 Sched A/B rows (appended on p3–6 Add'l Sheets) | `html-frozen/1800-2018/writer-cells.json` (`not_joined=32`, `not_joined_cells=64`, Item 14 cell unmapped) | `main/compare.png`, `rules/compare.png`, `1800-flow.mp4` |
| **1801** | p1–p2 | **p1 Item 5 TIN** (digits 1–9), **Item 16** (`NET TAXABLE ESTATE`), **Item 24** (`TOTAL AMOUNT PAYABLE`) + Sched 1–6 rows | Blank on paper despite non-empty data | **yes** | **yes** (Items 5, 16, 24 all still blank) | `html-frozen/1801-2018/writer-cells.json` (`not_joined=30`, `not_joined_cells=22`) | `main/compare.png`, `rules/compare.png`, `1801-flow.mp4` |
| **2000** | p2 (add'l) | 48 Sched 1 overflow values (`drpATCCode*`, `txtTaxBase*`, `txtAmountPaid*`, `txtPaymentDate*`, `txtReceipt*`) | All 48 absent on `main` (2 pages) | **yes** | **partial** (29 print on p3–6 Add'l Sheets; 19 `drpATCCode*`/`txtPaymentDate*` still absent) | No continuation emitter on `main` (`html-frozen/2000-2018/writer-cells.json`) | `main/compare.png`, `rules/compare.png`, `2000-flow.mp4` |
| **2000OT** | p2 (add'l) | 143 Sched 1A/1B overflow values (`sched1A:*`, `sched1B:*`) | All 143 absent on `main` (2 pages) | **yes** | **no** (all 143 print cleanly on p3–6 Add'l Sheets, 0 misses) | `html-frozen/2000-ot-2018/writer-cells.json` (`not_joined_cells=31`, no overflow emitter on `main`) | `main/compare.png`, `rules/compare.png`, `2000OT-flow.mp4` |
| **2200A** | p1 | 15 Part IV payment-detail fields (`cashBank/Num/Date/Amt`, `check*`, `debit*`) | Present in data, absent from paper | **yes** | **yes** (same 15 absent) | `html-frozen/2200a-2020/writer-cells.json` (`not_joined=7`, `not_joined_cells=7`) | `main/compare.png`, `rules/compare.png`, `2200A-flow.mp4` |
| **2200M** | p2 (add'l) | 202 Sched 1 values (`VOMRITaxableA*`, `VOMRIExemptB*`, `Imported*`) | All 202 absent on `main` (2 pages) | **yes** | **partial** (160 print on p3–4 Add'l Sheets; 42 `VOMRI*` still absent) | `html-frozen/2200m-2018/writer-cells.json` (`not_joined=11`, no overflow emitter on `main`) | `main/compare.png`, `rules/compare.png`, `2200M-flow.mp4` |
| **2200P** | p2 (add'l) | 184 Sched 1 overflow values (`txtSched1{ATC,Description,Exports,BasicExciseTaxDue}*`) | All 184 absent on `main` (2 pages) | **yes** | **yes** (182 still absent despite p3–4 Add'l Sheets) | `html-frozen/2200p-2020/writer-cells.json` (`not_joined=11`, `not_joined_cells=5`) | `main/compare.png`, `rules/compare.png`, `2200P-flow.mp4` |
| **2200S** | p2 | 95 Sched 1 beverage rows (`XB010`–`XB100` & Others: `txtSalesValue*`, `txtVolumeRemovals*`, `txtsched1*`) | Every row blank above `GRAND TOTAL = 786,732.48` | **yes** | **yes** (all 95 still blank) | `html-frozen/2200s-2018/writer-cells.json` (`not_joined=8`, `not_joined_cells=44`) | `main/compare.png`, `rules/compare.png`, `2200S-flow.mp4` |
| **2200T** | p2–p3 | 88 values (2020/2021 Sched 1 rows `txtSched1_*_2020_*` / `2021` + `cashAmt`) | Absent on `main` (3 pages) | **yes** | **yes** (same 88 absent on `rules` 5 pages) | **Sheet revision mismatch**: `2200T` data uses `v2020` (`2020`/`2021` rows), while `html-frozen/2200t-2022/writer-cells.json` (`not_joined=30`, `not_joined_cells=49`) is the August 2022 sheet starting at Jan 2022 | `main/compare.png`, `rules/compare.png`, `2200T-flow.mp4` |

**Recordings committed (Batch 2, 25 `.mp4` files)**:
`1600PT/1600PT-flow.mp4`, `1600VT/1600VT-flow.mp4`, `1600WP/1600WP-flow.mp4`, `1602Q/1602Q-flow.mp4`, `1604C/1604C-flow.mp4`, `1604E/1604E-flow.mp4`, `1604F/1604F-flow.mp4`, `1606/1606-flow.mp4`, `1701MS/1701MS-flow.mp4`, `1702EX/1702EX-flow.mp4`, `1702MX/1702MX-flow.mp4`, `1702Q/1702Q-flow.mp4`, `1702RT/1702RT-flow.mp4`, `1706/1706-flow.mp4`, `1707/1707-flow.mp4`, `1707A/1707A-flow.mp4`, `1800/1800-flow.mp4`, `1801/1801-flow.mp4`, `2000/2000-flow.mp4`, `2000OT/2000OT-flow.mp4`, `2200A/2200A-flow.mp4`, `2200M/2200M-flow.mp4`, `2200P/2200P-flow.mp4`, `2200S/2200S-flow.mp4`, `2200T/2200T-flow.mp4`.

---

### Question 5 — Settling the `1800` zero-gifts `-15,000.00` note

- **Test return (`1800-zero`)**: blank `1800` draft saved through the form page with `total_gifts = 0.0`, `total_deductions = 0.0`, `prior_net_gifts = 0.0`.
- **Saved return data (`draft.json`, what would be filed)**: `net_gifts_subject_to_tax = -250000.0`, **`tax_due = -15000.0`**, **`total_amount_payable = -15000.0`** — yes, `-15,000.00` IS in the return's data as well as on screen and on both `main` (`93820d0f`) and `rules` (`8c3a7b53`) PDFs.
- **Official BIR program rule (`rules/forms/1800-v2018/calculations.json`)**:
  - **Line 175**: `"official_formula": "Item 38 = Item 36 - 250,000, without a zero floor; Item 14 copies Item 38."`
  - **Line 197**: `"official_formula": "Item 16 = Item 14 × 6%."`
- **Classification**: **`NOT A FAULT`** — the app matches the official BIR eBIRForms 1800-v2018 program (`0 - 250,000 = -250,000` without a zero floor; `-250,000 × 6% = -15,000.00`) in data, on screen, and on paper (while Item 14 itself remains blank on paper, which is already tracked above as a `WRONG ON PAPER ONLY` mismatch).


---

## Round 3 Redo — Part 1: 15 Priority Claimed Class F Forms + `1701` Spouse TIN

Re-audited box-by-box from persisted SQLite drafts (`r3-redo-g1.db`, reopened `form.fields`, demo taxpayer Juana Santos `000-123-453`, 0 code changes) at `origin/main` (`93820d0f`) vs `origin/feat/store-launch-field-rules` (`8c3a7b53`). Every form below has `round3/<CODE>/mismatches.tsv`, `round3/<CODE>/data-excerpt.txt`, and `round3/<CODE>/README.md`; every form with `F > 0` also has `main/compare.png`, `rules/compare.png` (1400 px crops of the actual filled form-page boxes beside the printed boxes), and `<CODE>-flow.mp4`.

**Classes**: `F` = drawn sheet box has saved data value and prints blank/wrong; `R` = extra rows beyond the rows drawn on the sheet; `D` = printed with different formatting/clipping; `N` = internal/helper/derived/signatory key not meant to print.

### Per-form class totals (`main` `93820d0f` / `rules` `8c3a7b53`)

| Form | Main `F` | Main `R` | Main `D` | Main `N` | Rules `F` | Rules `R` | Rules `D` | Rules `N` | Verdict & key Class F boxes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **1801** | **5** | 624 | 0 | 0 | **5** | 0 | 0 | 0 | **Class F confirmed**: p1 Item 5 TIN (digits 1–9), Item 16 Net Taxable Estate, Item 24 Total Payable, Item 37C & Sched 5 `Specify` blank on both. Rules prints all 624 `R` rows on p3–20 Add'l Sheets. |
| **1800** | **1** | 134 | 0 | 0 | **1** | 0 | 0 | 0 | **Class F confirmed**: p1 Item 14 Total Net Gifts (`-144,262.42`) prints blank above Item 16 (`-8,655.75`) on both. *(9A ZIP `1003` confirmed printed by eye.)* Rules prints all 134 `R` rows on p3–6 Add'l Sheets. |
| **1702MX** | **201** | 0 | 0 | 1 | **201** | 0 | 0 | 1 | **Class F confirmed**: p1 Part II Items 14–19 blank above Item 21; p2 Schedule 1 Items 1–3 misaligned/wrong values (`p2c21` prints `126358` instead of `VAL025`); p2 Schedule 2 Item 1 blank/`0`; Schedule 6 rows unmapped on both. |
| **2200S** | **98** | 0 | 0 | 1 | **98** | 0 | 0 | 1 | **Class F confirmed**: p2 Schedule 1 every beverage row (`XB010`–`XB100` & Others) prints blank above `GRAND TOTAL` on both; p1 Items 19A, 19B, 25A blank on both. |
| **2200T** | **48** | 0 | 0 | 12 | **48** | 0 | 0 | 12 | **Class F confirmed**: `v2020` data holds 2020/2021 Schedule 1 rows omitted on the Aug 2022 sheet (`2200t-2022`) on both commits. |
| **1606** | **0** | 0 | 0 | 3 | **0** | 0 | 0 | 3 | **Class F withdrawn**: all persisted boxes print cleanly; 3 `N` keys (`txtOthers` old 2000 layout; `txtGross`/`txtBid` shaped via `derived:sched3_1a`). |
| **1701MS** | **0** | 0 | 0 | 5 | **0** | 0 | 0 | 5 | **Class F withdrawn**: all persisted boxes print cleanly; 5 `N` keys (`txtAmended`, `txtReturnPeriod`, `civilStatus` select, `printedName`, `authorizeRepresentative`). |
| **2200A** | **15** | 0 | 0 | 0 | **15** | 0 | 0 | 0 | **Class F confirmed**: p1 Part IV payment-detail rows (Items 25–28) print blank on both (`not_joined` in `writer-cells.json`). |
| **1702RT** | **0** | 12 | 0 | 12 | **0** | 12 | 0 | 12 | **Class F withdrawn**: previous Batch 2 `compare.png` showed an unsaved/refused return; every value persisted in SQLite prints cleanly on both commits. Remaining 12 `R` are Sched 5 Item 3 add-more rows (`txtPg4Sc5I3.*`). |
| **1707A** | **1** | 101 | 0 | 0 | **1** | 0 | 0 | 0 | **Class F confirmed**: p1 Item 12A `Specify` (`VAL010`) prints blank on both. Rules prints all 101 `R` rows on p3–8 Add'l Sheets. |
| **1602Q** | **0** | 1 | 0 | 0 | **0** | 1 | 0 | 0 | **Class F withdrawn**: all drawn boxes print cleanly; 1 `R` (`txtSched1Amount15`, 15th row beyond the 14 rows drawn on the 2019 sheet). |
| **1601C** | **0** | 0 | 0 | 0 | **0** | 0 | 0 | 0 | **Class F withdrawn** (for valid `WW010` returns; Item 5 ATC is preprinted `WW010` on the sheet, `not_joined` in `writer-cells.json`). |
| **1604C** | **1** | 0 | 0 | 1 | **1** | 0 | 0 | 1 | **Class F confirmed**: p1 Item 1 Year (`2025`) overprints preprinted `20` as `225 0` on both. 1 `N` (`txt12` blank when overremittance = No). |
| **1604E** | **1** | 0 | 1 | 0 | **1** | 0 | 1 | 0 | **Class F confirmed**: p1 Item 1 Year (`2025`) overprints preprinted `20` as `225 0` on both. 1 `D` (Item 7 Address clipped at `...845 ARNAIZ AV`). |
| **1701** | **3** | 0 | 0 | 0 | **2** | 0 | 0 | 0 | **Class F confirmed**: (1) p2 Sched 3.A Item 8A (`1,234,567,890`) blank on `main` (9-slot comb overflow), fixed on `rules`; (2) p2 Part IV Item 1 Spouse TIN branch prints `00000` instead of `00001` on both; (3) p2 Part V Sched 1 Row 1 Employer Name (`ACME CORP EMPLOYER 1`) prints blank on both. |

### Question 5 — `1701` Joint Return Spouse TIN (Part IV Item 1) Settled
- **Form page (`round3/1701/rules/compare.png`, left)**: `✓ Saved`, Part IV Item 1 Spouse TIN entered as `000` | `987` | `654` | `00001` (with `DELA CRUZ, PEDRO 44`, RDO `044`).
- **Printed Page 2 (`round3/1701/main/compare.png` and `round3/1701/rules/compare.png`, right)**:
  - **Nine TIN digits (`000-987-654`)**: **DO PRINT** cleanly in the 9-digit comb (`p2c5`) on both `origin/main` (`93820d0f`) and `rules` (`8c3a7b53`).
  - **Five-digit branch code (`00001`)**: **DOES NOT PRINT** — remains preprinted `0 0 0 0 0` on both commits (`html-frozen/1701-2018/writer-cells.json` lists `frm1701:txtPg2I1BranchCode` as unfillable because the sheet preprints `0 0 0 0 0`).
