# How to Add Items to index.html

All stock lives in one array in [index.html](index.html): `const ITEMS = [ ... ];`.
Add new items as objects at the end of that array, right before the closing `];`.

## Item format

```javascript
    {
      p: "90NB1553-M002R0",
      t: "ASUS VIVOBOOK S16 S5606CA-SB91 - 90NB1553-M002R0",
      s: "INTEL CORE ULTRA 9 285H | 16GB LPDDR5X | 1TB SSD | 16\" OLED WQ+ 120HZ DISPLAY | WINDOWS 11 | NEUTRAL BLACK | 90NB1553-M002R0",
      a: 4100,
      v: "Florence",
      c: "Laptops",
      f: "🔺 ASUS VIVOBOOK S16 S5606CA-SB91 - 90NB1553-M002R0 🔺BRAND NEW\n| INTEL CORE ULTRA 9 285H | 16GB LPDDR5X | 1TB SSD | 16\" OLED WQ+ 120HZ DISPLAY | WINDOWS 11 | NEUTRAL BLACK | 90NB1553-M002R0 | MANUFACTURE WARRANTY ONLY\nAED 4100 + VAT\n-------------------",
      cpu: "Intel Ultra 9",
      gpu: "Integrated",
    },
```

| Field | Meaning | Rule |
|---|---|---|
| `p` | Part number | Exactly as the supplier lists it. No trailing spaces. |
| `t` | Product **name** | `MODEL NAME - PARTNUMBER`. Brand + series + model code only. **No specs.** |
| `s` | **Specs** | Pipe-separated (` \| `), ending with the part number. **Never the same as `t`.** |
| `a` | Price | Number, AED, no quotes, no currency symbol, excl. VAT. |
| `v` | Vendor | Exact vendor name, e.g. `"Florence"`. |
| `c` | Category | One of the categories listed below — exact spelling. |
| `f` | Copy-paste block | Generated from the fields, see template below. |
| `cpu` | CPU filter tag | Only from the allowed list. Omit for non-compute items. |
| `gpu` | GPU filter tag | `"Integrated"` or a normalized card name. Omit for non-compute items. |

### The `t` / `s` split (most common mistake)

The full supplier title must be **split**, not copied into both fields.

Supplier title:
```
ASUS VIVOBOOK S16 S5606CA-SB91 ULTRA 9 285H 16GB LPDDR5X 1TB SSD 16" OLED WQ+ 120HZ WIN11 NEUTRAL BLACK
```

Becomes:
- `t`: `ASUS VIVOBOOK S16 S5606CA-SB91 - 90NB1553-M002R0`
- `s`: `INTEL CORE ULTRA 9 285H | 16GB LPDDR5X | 1TB SSD | 16" OLED WQ+ 120HZ DISPLAY | WINDOWS 11 | NEUTRAL BLACK | 90NB1553-M002R0`

Spec order to follow: **CPU → RAM → storage → display → graphics (if discrete) → OS → keyboard/extras → colour → part number.**

Expand shorthand: `CORI7` → `INTEL CORE i7`, `WIN11` → `WINDOWS 11`, `WIN11PRO` → `WINDOWS 11 PRO`,
`BACKLITE ENG_KB` → `BACKLIT ENGLISH KEYBOARD`, `FPR` → `FINGER PRINT READER`. Keep `DOS` as `DOS`.
Replace non-breaking hyphens (`‑`) with normal `-`.

### The `f` template

Always exactly:

```
🔺 {t} 🔺BRAND NEW\n| {s} | MANUFACTURE WARRANTY ONLY\nAED {a} + VAT\n-------------------
```

So `f` contains `t` once and `s` once. If you see the product title twice inside `f`, the item is wrong.
If quantity is known, add ` | N PCS AVAILABLE` as a segment inside `s` (before the part number).

## Allowed `cpu` values

Only these are picked up by the CPU filter — anything else silently disappears from the sidebar:

```
Intel Ultra 9   Intel Ultra 7   Intel Ultra 5   Intel Ultra 3
Intel Core i9   Intel Core i7   Intel Core i5   Intel Core i3
Intel Core 7    Intel Core 5    Intel Core 3
Intel Xeon
AMD Ryzen 9     AMD Ryzen 7     AMD Ryzen 5     AMD Ryzen 3
Snapdragon
Celeron / Pentium
```

Do **not** write `ULTRA 7`, `CORE I7`, `RYZEN 7`, `SNAPDRAGON X1`, or `Unknown`.
`AMD RYZEN AI 7 350` → `AMD Ryzen 7`. `SNAPDRAGON X ELITE` / `X PLUS` → `Snapdragon`.
If the CPU genuinely can't be determined, omit the `cpu` key entirely rather than writing `"Unknown"`.

## `gpu` values

`"Integrated"` for anything without a discrete card. Otherwise use spaced, title-cased names so they
merge with the existing filter entries:

```
RTX 5090   RTX 5080   RTX 5070 Ti   RTX 5070   RTX 5060 Ti   RTX 5060   RTX 5050
RTX 4070   RTX 4060   RTX 4050   RTX 3060   RTX 3050
RX 9070 XT   RX 9070
RTX Pro 3000   RTX 2000 Ada   RTX A400   RTX 500
```

Never `RTX5070TI`, `RTX4050`, `RTX5080` (no space / no case) — those create duplicate filter chips.

## Categories (`c`)

```
Laptops              Desktops        All-in-One      Workstations
Tablets              Watches & wearables
Servers              Monitors        Graphics cards  Printers
Networking           UPS & power     Scanners        Photocopiers
Plotters             Docks & accessories             Components & spares
```

Only `Laptops`, `Desktops`, `All-in-One` and `Workstations` show CPU/GPU tags on the card —
omit `cpu`/`gpu` for monitors, printers, accessories, etc.

Watch for items that aren't laptops even in a laptop price list: portable monitors → `Monitors`,
tower/desktop SKUs (Alienware Aurora, OMEN 45L, ThinkCentre, Dell Pro Tower) → `Desktops`.
iPads / Galaxy Tab → `Tablets`; Apple Watch, Fitbit and other wearables → `Watches & wearables`
(headphones, keyboards and chargers stay in `Docks & accessories`).

## Checklist before saving

- [ ] `t` ≠ `s`
- [ ] `s` is pipe-separated and ends with the part number
- [ ] `f` matches the template exactly (title appears once)
- [ ] `cpu` / `gpu` use values from the lists above
- [ ] `c` is the right category, spelled exactly
- [ ] Every item ends with `},`; the last one before `];` has no trailing comma
- [ ] Reload the page: no console errors, item count went up by the right number,
      and the vendor / CPU / GPU / category filters all show the new values

## Updating a vendor's daily stock list

Vendors (Lapcom Technologies, AGT, Florence, …) resend the **same list every day**. When a new
sheet arrives for a vendor that is already in `ITEMS`, do **not** append it — reconcile it, so the
vendor's items in `index.html` always mirror that vendor's latest sheet.

Match items by **part number** (`p`). Items with no part number (some Dell / used stock) match on
the model name in `t` instead.

| Case | Action |
|---|---|
| In the new sheet, not in `ITEMS` for that vendor | Add a new item, built per the rules above |
| In both, price changed | Update `a` **and** the `AED {a} + VAT` line inside `f` — they must always agree |
| In both, specs changed | Update `s` and rebuild `f` from the template |
| In `ITEMS` for that vendor, absent from the new sheet | Delete the whole item block |
| Marked `Sold` / `Out of stock` in the new sheet | Treat as absent — delete it, don't add it |

Only touch items whose `v` matches that vendor. The same part number often appears under other
vendors at a different price — leave those alone.

Notes on the sheets:

- Each row's `Description` cell is `MODEL NAME\nSPEC | SPEC | … | PARTNUMBER`. The first line is `t`,
  the rest is `s` — this is the same `t` / `s` split as above.
- The stock column (`Ready` / `Sold` / `Limited` / `Last Pcs` / a number) decides inclusion only.
  A quantity there can go into `s` as ` | N PCS AVAILABLE` before the part number.
- Ignore header rows, brand separator rows, and the trailing
  "Please note that this price is valid only for the mentioned date" row.
- A part number written inside the description as `P/no: 917881-002` is still the `p` value.
- A row with no part number (some used Dell / accessory stock) gets `p: ""`; put the model code in
  `t` so the item is still identifiable, and match it by `t` on the next update.
- A vendor may split their stock across several files (Florence sends *Gaming* and *Basic Models*).
  Reconcile **all** of that vendor's files together — an item missing from one file but present in
  the other must stay.

### Prices quoted in USD

Some vendors (TLM) send a list in US dollars. Convert at the peg **3.6725** and round the result
**up to the next 10**: `$920 -> 3378.7 -> AED 3380`, `$727 -> 2669.9 -> AED 2670`. The same
round-up-to-10 rule is what the in-page margin dialog applies, so quoted prices always end in a 0.

### Price on request

If the price column says `CALL` / `POA` instead of a number, write `a: "CALL"` (a string) and end
`f` with `PRICE ON REQUEST — CALL` in place of the `AED {a} + VAT` line. The rest of `f` is unchanged.

### After reconciling

- [ ] Vendor's item count in `index.html` equals the number of in-stock rows in the sheet
- [ ] No duplicate `p` values within that vendor
- [ ] Every changed price appears in both `a` and `f`
- [ ] Page reloads with no console errors and the vendor filter shows the new count
