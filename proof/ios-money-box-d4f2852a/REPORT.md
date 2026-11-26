# d4f2852a iOS money-box proof

Exact app commit: `d4f2852a28c323e3f6da85eae4f61d970d84ff0e`
NSH pin verified: `8c78cfd6d8ffcef260728ad2503d43c3bc9e86bf`
Devices: iPhone 17 Pro (`405F45A9-B471-47B7-A5D9-E545EA624713`), iPad Pro 13-inch (`41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3`)

Safety: all app launches used `SIMCTL_CHILD_BUWIZ_NO_KEYCHAIN=1`, `SIMCTL_CHILD_EBIR_TEST_ENV=1`, `SIMCTL_CHILD_BIR_AUTH_BYPASS=1`, `SIMCTL_CHILD_BIR_SFTP_DRY_RUN=1`. Queue was never pressed. Values are invented.

## Verdict

`B1/B2 at d4f2852a: iPhone B1 fail, B2 pass; iPad B1 fail, B2 pass`

B1 failure is strict and narrow: the deleted row is gone from the screen, remaining rows and totals are correct, and the old focused-delete `500` retention is gone. The draft still contains a blank deleted row object, and that object still has key `taxable_amount` with value `0.0`. If “NO amount” means the key must be absent, every B1 run fails. The deleted-slot object is exactly:

```json
{
  "atc": "",
  "atc_description": "",
  "taxable_amount": 0.0,
  "tax_rate": 0.0,
  "tax_due": 0.0
}
```

Keys in every deleted slot: `atc`, `atc_description`, `tax_due`, `tax_rate`, `taxable_amount`.

## B1 focused row-delete

Setup rows before deletion: `(PT010,1000,30)`, `(PT040,2000,60)`, `(PT010,3000,90)`. Row tuples below are `(atc,taxable_amount,tax_due)`.

| device | case | valid runs | rows after reopen | visible rows | totals | strict draft pass |
|---|---|---:|---|---|---|---|
| iPhone | row2 focused delete | 3/3 | `(PT010,1000,30)`, `("",0,0)`, `(PT010,3000,90)` | indexes 0 and 2; row2 gone | due/payable/total 120.0 | no |
| iPhone | row3 focused delete | 3/3 | `(PT010,1000,30)`, `(PT040,2000,60)`, `("",0,0)` | indexes 0 and 1; row3 gone | due/payable/total 90.0 | no |
| iPhone | row2 control, left first | 1/1 | same as row2 | indexes 0 and 2; row2 gone | due/payable/total 120.0 | no |
| iPad | row2 focused delete, docked keyboard | 3/3 | same as iPhone row2 | indexes 0 and 2; row2 gone | due/payable/total 120.0 | no |
| iPad | row3 focused delete, docked keyboard | 3/3 | same as iPhone row3 | indexes 0 and 1; row3 gone | due/payable/total 90.0 | no |
| iPad | row2 control, left first | 1/1 | same as row2 | indexes 0 and 2; row2 gone | due/payable/total 120.0 | no |

Delete was verified hittable before tapping in focused runs. iPad used the stable docked full-width software keyboard. Grouped machine-readable data: `b1-summary.json`. One video per device: `b1-strict/iphone/row2-r1/b1.mp4` and `b1-strict/ipad/row2-r1/b1.mp4`.

## B2 German comma, filled amount, print preview without leaving

| device | typed | keyboard state before print | preview item 15 | draft corroboration | result |
|---|---|---|---|---|---|
| iPhone | `1500,50` | German comma keypad visibly still up; no Done/blur/other field | `1,500.50`; item18 `1,500.50` | `creditable_tax_withheld=1500.5` | pass |
| iPad | `1500,50` | blue focus ring/caret still present after keypad disappeared during docking attempt; no manual field exit | `1,500.50`; item18 `1,500.50` | `creditable_tax_withheld=1500.5` | pass |

iPhone evidence: `b2-german-print/iphone/002-before-print-keyboard-still-up.jpg`, `003-print-preview.jpg`, `004-preview-crop-items14-19.png`.
iPad evidence: `b2-german-print/ipad/002-after-1500comma50.jpg`, `003-after-dock-attempt.jpg`, `006-after-print-tap.jpg`, `007-page1-preview-enlarged.png`.

## Plain middle-row delete, nothing focused

| device | keyboard visible at delete | rows after reopen | screen rows | totals | row preservation |
|---|---|---|---|---|---|
| iPhone | false | `(PT010,1000,30)`, `("",0,0)`, `(PT010,3000,90)` | indexes 0 and 2 | due/payable/total 120.0 | pass |
| iPad | false | `(PT010,1000,30)`, `("",0,0)`, `(PT010,3000,90)` | indexes 0 and 2 | due/payable/total 120.0 | pass |

The former row3 kept `3000.0`/`90.0` in the draft and on screen. The blank deleted slot representation is the same five-key zeroed object above.

## Caveats

- In the iPhone B2 result JSON, `keyboard_visible_before_print=false` is an instrumentation-ordering artifact because accessibility state was reread after the print tap. `002-before-print-keyboard-still-up.jpg` is the objective evidence that the German comma keypad was still visible with Print preview exposed before the tap.
- iPad B2 caveat: the floating decimal keypad disappeared during a docking attempt, but the amount retained its visible focus ring/caret and no other field or Done control was tapped before print.
- An earlier plain-delete harness run on iPhone inherited unrelated B2 credit/penalty values and was discarded as contaminated. The reported result is the final clean rerun.
