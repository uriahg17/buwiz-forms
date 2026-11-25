# 2000OT independent print check

Verdict: **tweak**.

`before.*` is main 92b3e201 built with target-355main; `after.*` is head 3e8b1212 built with target-355head. `run-*.log` contains the saved-data excerpt and print probe. `preview-*-pN.png` are preview-window captures; `before/after-pN.png` are 1400px PDF renders; bbox/text/pdffonts/pdfinfo files are poppler output. `head-run.mp4` records the head run.

Main behavior is materially worse (no additional-sheet continuations and full long text crammed on the form). Head preserves values; only continuation-header cosmetics are suspect.
