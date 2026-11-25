# Independent verification report — PR #350

## Commits tested

- MAIN `00a2003351ea56e7f7b585e1485ba31adf24514c` (`origin/main`; verified after checkout).
- HEAD `b1db7157193e80066a635bfc7b9164b22c40a76d` (verified after checkout).
- Real Linux windows in the mandated container/Xvfb, scratch test database, demo taxpayer only, dry-run/auth bypass/no keychain. No Queue control was pressed.

## Verdict

The central claim **holds everywhere I was able to test it in the production picker**: at HEAD, text, code, empty row area, right-hand chip, and leading box each toggle once per press at desktop/tablet/phone widths; at MAIN only the small box toggles. Save/reopen/cancel, filtered rows, frequency filters, Setups, physical keyboard Space/Return, focus ring, semantic-tree identity, and the draft fast lane all behaved as claimed in the tested paths.

I found **no production regression caused by the change** in these tests. The notable caveats/failures are test-environment or scope caveats, plus one missed checkbox+text pattern outside the picker:

1. **Missed survey item (low harm):** `nsh/shell/desktop/Desktop.tsx` still has `<Checkbox testID="close-ask-remember" label="Don't ask again">` followed by separate visible text `Don't ask again. You can change this in Settings.` This is the same checkbox+separate-label shape fixed in the draft dialog. I verified it in source at HEAD; I could not runtime-prove it because the test fixture mounts `Shell` without the outer desktop close host.
2. **Press-and-drag did not scroll at either commit (pre-existing, not a regression):** exact reproduction: in edit mode, unfiltered long list, start at logical `(x=row.x+170, y=center of checked 1601C row)` and `gpui-agent drag --dx 0 --dy -260`. Reply `ok:true`; row y stayed 727; count and checked state stayed unchanged. This happened identically at MAIN and HEAD. It may be normal mouse-drag behavior on Linux desktop rather than a touch-scroll failure, but it means the requested “does it scroll?” answer is **no in this environment**.
3. **True double click untestable here:** `xdotool` mouse clicks did not reach the Xvfb/GTK fixture window at all, even as single clicks. `gpui-agent` injected presses did reach. Therefore no true OS double-click evidence. In production two rapid injected presses ended back at the original state; in the CheckRow fixture each press incremented the toggle counter exactly once.
4. **No disabled production picker rows exist:** `FormsTab.tsx` never passes `disabled` to CheckRow. The disabled behavior was verified in the branch's `checkrow.fixture.tsx`: Gamma was dimmed, semantic `enabled:false`, exactly 52 pt high, and physical box/text/empty presses were rejected as disabled without changing state.

## 1. Picker presses, sequence, drag, save/cancel

### Per-width matrix

See `README.md` for the full table. Summary:

- At **MAIN**, every non-box area (text/code/empty/chip) returned `node ... is not pressable` and left 1601C checked and count `2 selected` at all three widths. The leading box toggled unchecked/checked and count `1 selected`/`2 selected`.
- At **HEAD**, every one of those same physical points toggled 1601C off then on and count `1 selected` then `2 selected` at all three widths.
- Actual viewport/row measurements:
  - desktop 1440×900, row 814×59;
  - tablet requested 834×1112, actual 834×1070, row 750×58;
  - phone requested 390×844, actual 420×844 (Linux minimum), row 386×58.

### Several rows in sequence

Starting count `1 selected` in edit mode:

- HEAD physical title presses on 0605, 0619E, 0619F selected each in turn: counts `2 selected`, `3 selected`, `4 selected`.
- MAIN the same title presses were rejected as non-pressable and count stayed `1 selected`.

### Press crossing rows and press-drag scroll

At both commits:

- drag starting on checked 1601C and ending one row lower: count stayed `2 selected`, 1601C stayed checked;
- drag upward by 260 pt: count/state unchanged, but row y did not move (`scrolled:false`). So no mistaken toggle; also no drag-scroll in this Linux driver environment.

### Save, reopen, Cancel

The test unticked 1601C using the leading box, then pressed Save:

- both commits saved exactly the still-ticked set: only 2551Q was listed;
- leaving to Templates and returning to Forms still showed only 2551Q;
- entering edit again, ticking 1601C, then Cancel left the saved list unchanged (still only 2551Q).

## 2. Search, filters, Setups

At both commits, search `vat` showed `1600VT`, `2550M`, `2550Q` and not 1601C. Frequency segmentation remained combined with the search: Monthly rows `1600VT/2550M`, Quarterly `2550Q`, Annual and As-needed none, All all three. The selected count stayed stable while changing frequency (HEAD `2 selected` in its run; MAIN `3 selected` after its checkbox fallback selection).

Filtered-row selection differed exactly as expected:

- HEAD: pressing the 2550Q title text changed it false→true.
- MAIN: the same press was rejected as non-pressable and did nothing; pressing the small box then selected it.

`Non-VAT professional` still applied at both commits. The resulting saved forms list was `1701`, `1701Q`, `2551Q`, with toast `Non-VAT professional: 3 forms for 2026.` The count/list followed the setup. In this app flow applying a setup leaves edit mode; that was identical at both commits.

## 3. Widths and target size

- Narrowest accepted phone width was **420 logical pt**, although 390 was requested; this is the Linux window minimum. Tablet actual height was 1070 rather than requested 1112.
- Production rows measured 58–59 pt high at both commits and all widths, exceeding 52 pt.
- At HEAD the semantic checkbox control itself is the full row width. At MAIN the semantic checkbox control is 16×16 inside a generic row.

## 4. Keyboard

Physical xdotool key events did reach the window. From the search field, ten Tab presses put focus on 1601C in this fixture.

- HEAD: screenshot shows the focus ring around the **whole row**. Space once: `2 selected`→`1 selected`, checked true→false. Space twice: back to `2 selected`, true. Return behaved the same.
- MAIN: screenshot shows the focus ring only around the **small box**. Space and Return also toggled it off/on. Thus keyboard toggling existed before, but the focused control representation/target changed as claimed.
- `gpui-agent key ... --delivery virtual` could not target the row directly on Linux (`node ... cannot receive native focus`) at either commit. The semantic tree's `focused` field also stayed false even when the visual focus ring was obvious. These are control-plane/semantic exposure limitations; the physical key result above is the meaningful app result.

## 5. Accessibility tree exposed by the driver

MAIN editing row:

- row `tp-form-1601C`: role `generic`, name `tp-form-1601C`, row bounds 814×58;
- child `tp-form-1601C-check`: role `checkbox`, name `File 1601C in 2026`, bounds 16×16, checked state.

HEAD editing row:

- row `tp-form-1601C`: itself role `checkbox`, name `File 1601C in 2026`, bounds 814×58/59, checked state;
- exactly one checkbox node in the row subtree.

So HEAD really does expose one row-sized checkbox control. MAIN did not expose two checkbox controls, but it exposed a generic row plus a small separate checkbox; assistive output would not treat the whole row as the control.

## 6. Open-existing draft fast lane

The seeded January/February 1601C drafts produced the draft-existing dialog at both commits.

MAIN:

- clicking the visible text point twice: rejected `node ... is not pressable`; checkbox stayed false;
- clicking the 16×16 box toggled false→true→false.

HEAD:

- clicking the visible text point toggled false→true→false;
- clicking the box also toggled false→true→false;
- the semantic control was one checkbox named `Don't ask again for drafts (this session)` spanning the label line (378×22).

With the box left on and “Keep this form” chosen, saving the same sample as February did **not** show the dialog again at either commit. Both showed `Loaded your saved February 2026 draft (you chose not to be asked again).` Thus the fast-lane preference itself already worked; HEAD fixes the label hit target/control shape.

## 7. Survey for missed checkbox+label rows

`git grep '<Checkbox'` at HEAD over production `nsh/screens`/`nsh/shell` found the other production uses already using `CheckboxLabel` or row-wide checkbox bases. The one missed production pattern I found is:

- `nsh/shell/desktop/Desktop.tsx` close dialog: a bare `Checkbox testID="close-ask-remember" label="Don't ask again"` next to separate visible text `Don't ask again. You can change this in Settings.`

I did not find additional raw checkbox+separate-label patterns in taxpayer, templates, settings, attachments, schedules, or filings filter source. The MultiCombo options already use row-wide `CheckboxBase`. The close dialog was source-verified only, for the fixture limitation stated above.

## Disabled CheckRow fixture

At HEAD, `ui/checkrow.fixture.tsx` exposed:

- Alpha: role checkbox, enabled, 666×52;
- Beta: role checkbox, enabled/checked, 666×52;
- Gamma: role checkbox, **enabled:false**, dimmed visually, 666×52, states `disabled`,`unchecked`.

Pressing Alpha's text twice changed the live counter `a:off/0` → `a:on/1` → `a:off/2` — exactly one toggle per press. Pressing Gamma's box/text/empty end was rejected as disabled and left state/counter unchanged.

## Exact reproduction of the main misfire/environment limitation

Press-drag scroll probe (same result both commits):

```text
Edit forms, unfiltered long list.
1601C row bounds x=433 y=727 w=814 h=59.
gpui-agent drag --x 603 --y 756 --dx 0 --dy -260
```

Result: `ok:true`; y remained 727; count remained `2 selected`; 1601C remained checked. Interpretation: no accidental toggle, but no drag scroll in this Linux environment.

## Bottom line

I would not block PR #350 on anything proven here. The production picker behavior claimed by the PR was reproducible at HEAD and contrasted cleanly with MAIN. The only product-facing gap found is the missed close-dialog checkbox label, outside the picker and low harm; the drag-scroll and true-double-click items are environment-limited or pre-existing rather than regressions.
