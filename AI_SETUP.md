# Comnet B2B — Setup & Operating Manual (for the AI taking over this project)

Read this file top to bottom before touching anything. It has two halves:

- **Part 1 — Setup**: put this project on a fresh GitHub account and a fresh Vercel account.
- **Part 2 — Operating rules**: how stock items are added, updated and removed. These rules are
  strict. Follow them exactly; do not invent your own format, do not "improve" the data model.

---

# Part 1 — Setup on a new GitHub + Vercel account

## 1.1 What this project is

A **single static file**: `index.html` (~1.4 MB, ~2,500 products). No build step, no framework,
no package.json, no server, no database, no environment variables, no API keys.

Everything lives in that one file:

- HTML + CSS + JavaScript, all inline.
- All stock data is one JavaScript array, `const ITEMS = [ ... ];` (around line 764).
- The page renders the cards, search, filters (vendor / CPU / GPU / category) and the
  copy-to-clipboard blocks entirely in the browser from that array.

Consequence: **deploying = serving `index.html` at the site root.** Nothing else.

## 1.2 Files

| File | Committed? | Purpose |
|---|---|---|
| `index.html` | **Yes** — this is the whole site | The app + all stock data |
| `AI_SETUP.md` | Yes | This file |
| `INSTRUCTIONS.md` | Optional | Older copy of the item rules (Part 2 here supersedes it) |
| `*.xlsx` / `*.xls` / `*.csv` | **No** | Vendor price lists — source material, never committed |
| `.claude/` | No | Local tool settings |
| `.DS_Store` | No | macOS junk — keep it out of the new repo |

## 1.3 Create the GitHub repo

From the project folder, on the new account:

```bash
# if there is an old remote pointing at someone else's account, drop it
git remote remove origin 2>/dev/null

# make sure junk stays out
printf '.claude\n*.xlsx\n*.xls\n*.csv\n.DS_Store\n.vercel\n' > .gitignore
git rm --cached .DS_Store 2>/dev/null

git add -A
git commit -m "Comnet B2B stock list"

# create the repo on the new account (gh must be authenticated as that account)
gh auth status
gh repo create <new-account>/b2b_list --private --source=. --remote=origin --push
```

No `gh`? Create an empty repo in the GitHub UI, then:

```bash
git remote add origin https://github.com/<new-account>/b2b_list.git
git branch -M main
git push -u origin main
```

Confirm afterwards: `git remote -v` points at the new account, and `git ls-files` lists
`index.html`, `.gitignore`, `AI_SETUP.md` — **and no spreadsheets**.

## 1.4 Deploy on Vercel

This is a plain static site. Do **not** add a framework, a build command, or a `vercel.json`
unless something below actually requires it.

**Dashboard route (preferred):**

1. Vercel → *Add New…* → *Project* → import `b2b_list` from the new GitHub account.
2. Framework Preset: **Other**.
3. Build Command: **leave empty**. Output Directory: **leave empty** (repo root).
4. Install Command: leave empty. Environment variables: none.
5. Deploy. The site is live at `<project>.vercel.app`, serving `index.html` at `/`.

**CLI route:**

```bash
npm i -g vercel
vercel login          # as the new account
vercel link           # create a new project
vercel --prod
```

After the first deploy, every push to `main` auto-deploys to production, and every other branch
gets a preview URL. That is the whole release process: **commit → push → live**.

### Caching note

`index.html` changes on almost every update and must never be served stale. Vercel does not
long-cache HTML by default, so no config is needed. Only if you observe stale content add:

```json
{
  "headers": [
    { "source": "/index.html",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }] }
  ]
}
```

as `vercel.json` in the repo root. Nothing else belongs in that file.

## 1.5 Verify a deploy (do this every time)

- [ ] Page loads, no errors in the browser console
- [ ] The item count shown on the page matches what you expect
- [ ] Vendor, CPU, GPU and category filters all populate and filter correctly
- [ ] A product card's copy button copies the `f` block cleanly
- [ ] The deployed URL shows your latest commit hash in the Vercel dashboard

## 1.6 Working rules

- Edit `index.html` **in place**. Never regenerate it, never reformat the whole file, never
  reorder existing items, never change the CSS/JS unless explicitly asked. Surgical edits only.
- The file is large. Locate the region with `grep -n` and edit that region; do not rewrite the file.
- Commit per vendor update with a clear message, e.g. `Update Florence list 21-Sep-2026`.
- Never commit vendor spreadsheets. They are the supplier's, and they are gitignored for a reason.
- If a change breaks the page (a stray comma is enough), fix it before pushing —
  a broken `ITEMS` array means a blank site.

---

# Part 2 — Operating rules: adding and updating stock

**These rules are mandatory.** Every item in `ITEMS` follows the same shape. An item that deviates
either disappears from the filters or renders wrong. When in doubt, copy the shape of a
neighbouring item from the same vendor.

New items go at the **end** of the array, right before the closing `];`.

## 2.1 Item format

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
| `c` | Category | One of the categories in 2.5 — exact spelling. |
| `f` | Copy-paste block | Generated from the fields, template in 2.3. |
| `cpu` | CPU filter tag | Only from the list in 2.4. Omit for non-compute items. |
| `gpu` | GPU filter tag | `"Integrated"` or a normalized card name. Omit for non-compute items. |

Existing vendor names in the file (use the exact spelling, never a variant):

```
Solid Solution   Mussallam Trading   AGT        Supertech    GPCD
Gulf Micro       Blue Bill           Torontech  Xcell Computers
Florence         BNI                 Mohammad Mirza          Smile Computer LLC
Al Tawfiq        Lapcom Technologies Welinx     RTX Computers           TLM
```

## 2.2 The `t` / `s` split (the most common mistake)

The supplier's full title must be **split**, not copied into both fields.

Supplier title:
```
ASUS VIVOBOOK S16 S5606CA-SB91 ULTRA 9 285H 16GB LPDDR5X 1TB SSD 16" OLED WQ+ 120HZ WIN11 NEUTRAL BLACK
```

Becomes:
- `t`: `ASUS VIVOBOOK S16 S5606CA-SB91 - 90NB1553-M002R0`
- `s`: `INTEL CORE ULTRA 9 285H | 16GB LPDDR5X | 1TB SSD | 16" OLED WQ+ 120HZ DISPLAY | WINDOWS 11 | NEUTRAL BLACK | 90NB1553-M002R0`

Spec order: **CPU → RAM → storage → display → graphics (if discrete) → OS → keyboard/extras →
colour → part number.**

Expand shorthand: `CORI7` → `INTEL CORE i7`, `WIN11` → `WINDOWS 11`, `WIN11PRO` → `WINDOWS 11 PRO`,
`BACKLITE ENG_KB` → `BACKLIT ENGLISH KEYBOARD`, `FPR` → `FINGER PRINT READER`. Keep `DOS` as `DOS`.
Replace non-breaking hyphens (`‑`) with normal `-`.

## 2.3 The `f` template

Always exactly:

```
🔺 {t} 🔺BRAND NEW\n| {s} | MANUFACTURE WARRANTY ONLY\nAED {a} + VAT\n-------------------
```

`f` contains `t` once and `s` once. **If the product title appears twice inside `f`, the item is wrong.**
If quantity is known, add ` | N PCS AVAILABLE` as a segment inside `s`, before the part number.

## 2.4 Allowed `cpu` and `gpu` values

Only these `cpu` values are picked up by the filter — anything else silently disappears from the sidebar:

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
If the CPU genuinely can't be determined, **omit the `cpu` key entirely** rather than writing `"Unknown"`.

`gpu` is `"Integrated"` for anything without a discrete card. Otherwise spaced, title-cased names
so they merge with existing filter entries:

```
RTX 5090   RTX 5080   RTX 5070 Ti   RTX 5070   RTX 5060 Ti   RTX 5060   RTX 5050
RTX 4070   RTX 4060   RTX 4050   RTX 3060   RTX 3050
RX 9070 XT   RX 9070
RTX Pro 3000   RTX 2000 Ada   RTX A400   RTX 500
```

Never `RTX5070TI`, `RTX4050`, `RTX5080` (no space / wrong case) — those create duplicate filter chips.

## 2.5 Categories (`c`)

```
Laptops              Desktops        All-in-One      Workstations
Tablets              Watches & wearables
Servers              Monitors        Graphics cards  Printers
Networking           UPS & power     Scanners        Photocopiers
Plotters             Docks & accessories             Components & spares
```

Only `Laptops`, `Desktops`, `All-in-One` and `Workstations` show CPU/GPU tags on the card —
omit `cpu`/`gpu` for monitors, printers, accessories, etc.

Watch for items that aren't laptops even inside a laptop price list: portable monitors → `Monitors`;
tower/desktop SKUs (Alienware Aurora, OMEN 45L, ThinkCentre, Dell Pro Tower) → `Desktops`;
iPads / Galaxy Tab → `Tablets`; Apple Watch, Fitbit and other wearables → `Watches & wearables`
(headphones, keyboards and chargers stay in `Docks & accessories`).

## 2.6 Checklist before saving

- [ ] `t` ≠ `s`
- [ ] `s` is pipe-separated and ends with the part number
- [ ] `f` matches the template exactly (title appears once)
- [ ] `cpu` / `gpu` use values from the lists above
- [ ] `c` is the right category, spelled exactly
- [ ] Every item ends with `},`; the last one before `];` has no trailing comma
- [ ] Reload the page: no console errors, item count went up by the right number, and the
      vendor / CPU / GPU / category filters all show the new values

## 2.7 Updating a vendor's daily stock list

Vendors resend the **same list every day**. When a new sheet arrives for a vendor already in
`ITEMS`, do **not** append it — **reconcile** it, so that vendor's items in `index.html` always
mirror that vendor's latest sheet.

Match items by **part number** (`p`). Items with no part number (some Dell / used stock) match on
the model name in `t` instead.

| Case | Action |
|---|---|
| In the new sheet, not in `ITEMS` for that vendor | Add a new item, built per the rules above |
| In both, price changed | Update `a` **and** the `AED {a} + VAT` line inside `f` — they must always agree |
| In both, specs changed | Update `s` and rebuild `f` from the template |
| In `ITEMS` for that vendor, absent from the new sheet | Delete the whole item block |
| Marked `Sold` / `Out of stock` in the new sheet | Treat as absent — delete it, don't add it |

**Only touch items whose `v` matches that vendor.** The same part number often appears under other
vendors at a different price — leave those alone.

Notes on the sheets:

- Each row's `Description` cell is `MODEL NAME\nSPEC | SPEC | … | PARTNUMBER`. The first line is `t`,
  the rest is `s` — the same split as 2.2.
- The stock column (`Ready` / `Sold` / `Limited` / `Last Pcs` / a number) decides inclusion only.
  A quantity there can go into `s` as ` | N PCS AVAILABLE` before the part number.
- Ignore header rows, brand separator rows, and the trailing
  "Please note that this price is valid only for the mentioned date" row.
- A part number written inside the description as `P/no: 917881-002` is still the `p` value.
- A row with no part number gets `p: ""`; put the model code in `t` so the item is still
  identifiable, and match it by `t` on the next update.
- A vendor may split stock across several files (Florence sends *Gaming* and *Basic Models*).
  Reconcile **all** of that vendor's files together — an item missing from one file but present in
  the other must stay.

### Prices quoted in USD

Some vendors (TLM) send lists in US dollars. Convert at the peg **3.6725** and round **up to the
next 10**: `$920 → 3378.7 → AED 3380`, `$727 → 2669.9 → AED 2670`. The same round-up-to-10 rule is
what the in-page margin dialog applies, so quoted prices always end in a 0.

### Price on request

If the price column says `CALL` / `POA` instead of a number, write `a: "CALL"` (a string) and end
`f` with `PRICE ON REQUEST — CALL` in place of the `AED {a} + VAT` line. The rest of `f` is unchanged.

### After reconciling

- [ ] Vendor's item count in `index.html` equals the number of in-stock rows in the sheet
- [ ] No duplicate `p` values within that vendor
- [ ] Every changed price appears in both `a` and `f`
- [ ] Page reloads with no console errors and the vendor filter shows the new count
- [ ] Commit and push — Vercel deploys `main` automatically; verify the live URL per 1.5
