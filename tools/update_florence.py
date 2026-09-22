import re
from pathlib import Path

VENDOR = "Florence"
ROWS = [('90NR0NJ7-M002W0', 'Asus ROG Strix G16 G614PR-G16.R95070TI Ryzen 9 8940HX 16GB DDR5 1TB SSD 16" WUXGA IPS 165Hz Win11 RTX 5070Ti 12GB', 7300.0, 'Laptops'), ('90NR0L91-M000H0', 'Asus ROG Strix G16 G615JPR-AS96 Cori9-14900HX 32GB DDR5 1TB SSD 16" WUXGA 165Hz Win11 RTX 5070 8GB Gray RGB', 7050.0, 'Laptops'), ('90NR0MD1-M007H0', 'Asus Tuf A16 FA608PP Ryzen 9 8940HX 16GB DDR5 512GB SSD 16" WUXGA 165Hz Win11 RTX 5070 8GB Jaeger Gray RGB KB', 6550.0, 'Laptops'), ('90NR0NM1-M00050', 'Asus TUF A18 FA808UH‑RS74 AMD Ryzen 7 260 16GB DDR5 1TB SSD 18" WUXGA 144Hz Win11 RTX 5050 8GB RGB KB', 4400.0, 'Laptops'), ('90PF0561-M02MF0', 'Desktop Asus ROG G700TF-WS766 Core Ultra 7-265KF 32GB DDR5 1TB SSD Win11 RTX 5060 8GB Black Keyboard + Mouse', 5550.0, 'Desktops'), ('9S7-182432-420', 'MSI Raider 18 HX AI A2XWIG Ultra 9 285HX 32GB DDR5 1TB SSD 18" QHD+ IPS 240Hz Win11 Core Black RTX 5080 16GB', 10550.0, 'Laptops'), ('9S7-15M352-414', 'MSI Vector 16 HX AI A2XWIG Ultra 9 275HX 16GB DDR5 1TB SSD 16" QHD+ IPS 240Hz Win11 RTX 5080 16GB Cosmos Gray', 8550.0, 'Laptops'), ('9S7-15M352-413 / 9S7-15M352-275', 'MSI Vector 16 HX AI A2XWHG Ultra-7-255HX 16GB 1TB SSD 16" FHD+ IPS 144Hz Win11 RTX 5070Ti 12GB Cosmo Gray RGB_KB', 6100.0, 'Laptops'), ('9S7-15Q342-409 / 9S7-15Q342-415', 'MSI Cyborg 15 B13WFKG Core 7-240H 16GB DDR5 1TB SSD 15.6" FHD 144Hz DOS RTX 5070 8GB Black RGB_KB', 4800.0, 'Laptops'), ('9S7-15Q342-256', 'MSI Cyborg 15 B2RWFKG Core 7 240H 16GB 512GB SSD 15.6" FHD 144Hz Win11 RTX 5060 8GB Black RGB Backlit_KB', 4200.0, 'Laptops'), ('9S6-B0Y221-682', 'MSI Codex R2 AI MS-B0Y2 Desktop C2NVP7-682US Core Ultra 7-256F 16GB DDR5 1TB SSD Win11 Black RTX 5070 12GB', 6575.0, 'Desktops'), ('9S6-B0Y221-469', 'MSI Codex R2 Desktop MSI Codex R2 A2NVM7-469US Core Ultra 7-265 32GB DDR5 2TB SSD Win11 RTX 5060Ti 8GB', 6575.0, 'Desktops'), ('8X38D', 'Dell Alienware 18 Area-51 AA18250 Ultra 9 275HX 64GB DDR5 2TB SSD 18" QHD+ 300Hz Win11 RTX 5090 24GB', 17650.0, 'Laptops'), ('VW5KT', 'Dell Alienware 15 DA15265 AMD Ryzen 5 220 16GB DD5 512GB SSD 15.3" WUXGA 165Hz Win11 Nvidia RTX 4050 6GB', 3650.0, 'Laptops'), ('10JGT', 'Desktop Dell Alienware Aurora ACT1250 Ultra 9-285K 32GB DDR5 2TB SSD Win11 Eng_Kb&Mouse RTX 5080 16GB Black', 12500.0, 'Desktops'), ('70DP8', 'Desktop Dell Alienware Aurora ACT1250 Ultra 9-285K 32GB DDR5 1TB SSD Win11 Eng_Kb&Mouse RTX 5070Ti 16GB Black', 9700.0, 'Desktops'), ('PHK5H', 'Desktop Dell Tower ECT1250 DECT1250-7274BLK-PUS Ultra 7-265F 32GB DDR5 1TB SSD Win11 KB&Mouse RTX 5060 8GB', 5750.0, 'Desktops'), ('0MH1PT', 'Dell Alienware AW2723DF 27" QHD | 2560×1440 | 240Hz', 1950.0, 'Monitors'), ('83LU0052US', 'Legion Pro 5 Ultra 9 275HX 32GB DDR5 1TB SSD 16" WQXGA OLED 240Hz Win11 RTX 5070Ti 12GB Eclipse Black RGB KB', 9550.0, 'Laptops'), ('83Q70003US', 'Lenovo Legion 5 15AHP11 Ryzen 7 250 16GB 1TB SSD 15.3" WQXGA OLED 165Hz Win11 RTX 5060 8GB Eclipse Black RGB KB', 5400.0, 'Laptops'), ('83DX00F1PB', 'Lenovo LOQ 15AHP9 AMD Ryzen 7 7445HS 16GB DDR5 512GB SSD 15.6" FHD 144Hz DOS RTX 3050 6GB Luna Grey Backlit_KB', 3150.0, 'Laptops'), ('B98D2UA', 'HP Omen Transcend 14‑FB1047NR Ultra 7‑255H 16GB DDR5 1TB SSD 14" 3K OLED 120Hz White Win11 RTX 5060 8GB', 5250.0, 'Laptops'), ('B9HT7AA#ABA', 'Gaming Desktop HP Omen 45L GT22-3060 Core Ultra 7-265K 32GB DDR5 1TB SSD RTX 5070Ti 12GB Win11Pro', 9500.0, 'Desktops'), ('90NB1511-M00BU0', 'Asus Vivobook 16 Flip TP3607SA-IS77T Ultra 7 258V 32GB DDR5 1TB SSD 16" WUXGA OLED Touch Win11 Matte Gray', 4700.0, 'Laptops'), ('90NB14Y1-M005E0', 'Asus Vivobook Flip TP3407SA‑DS74T Ultra 7 256V 16GB LPDDR5X 1TB SSD 14" OLED Touch x360 Matte Grey Win11', 3700.0, 'Laptops'), ('90NB13Y1-M02660', 'Asus Vivobook 15 X1504VA Core 7-150U 16GB DDR 512GB SSD 15.6" FHD DOS Quite Blue Full Backlite Eng_KB', 2350.0, 'Laptops'), ('90NB13Y2-M01TV0', 'Asus Vivobook X1504VA-BQ4173 Core 7-150U 8GB 512GB SSD 15.6" FHD DOS COOL SILVER ENG/ARABIC', 2125.0, 'Laptops'), ('90NB10J2-M00H50', 'Asus VivoBook X1504VA-NJ379 13th Gen Cori7-1355U 8GB 512GB SSD 15.6" FHD DOS ENG SILVER', 2125.0, 'Laptops'), ('90NB15Z2-M007H0', 'Asus VivoBook 16 X1607QA Snapdragon X1‑26‑100 16GB LPDDR5 1TB SSD 16" WUXGA Cool Silver Win11 Backlit_KB', 2100.0, 'Laptops'), ('90NB13Y2-M033T0', 'Asus Vivobook 15 A1504VA-BQ541 Core™ 5 120U 8GB DDR5 512GB SSD 15.6" FHD DOS Cool Silver Baklit Eng_KB', 1875.0, 'Laptops'), ('90NB0ZR2-M06560', 'Asus Vivobook Go 15 E1504FA-BQ2909 AMD Ryzen 5 40 8GB DDR5 512GB SSD 15.6" FHD DOS Mix Black Backlit Eng_Kb', 1700.0, 'Laptops'), ('90LM07D3-B031B0', 'Asus Zenscreen MB166C Portable USB Monitor 15.6" FHD IPS Display USB Type-C Connector', 525.0, 'Monitors'), ('NX.DGCEX.007', 'Acer Aspire Lite AL15-53P-58SY (14th) Core 5-120U 16GB 512GB SSD 15.6" FHD DOS Light Silver Eng-KB', 2050.0, 'Laptops'), ('B5UH1UA', 'HP OmniBook X Flip 16‑AS0023DX Ultra 7 256V 16GB LPDDR5 1TB SSD 16" 2K IPS Touch Intel Arc 140V Win11 Eng KB', 3100.0, 'Laptops'), ('D0VF2UA', 'HP OmniBook 3 14-HZ0015dx AI Qualcomm Snapdragon X X1-26-100 16GB 512GB SSD 14" 2K IPS Touchs Eng_KB Win11', 2350.0, 'Laptops'), ('95GTJ', 'Dell 14 Premium DA14250 (XPS 14) Ultra 7 255H 16GB 512GB SSD 14.5" Display Win11 Platinum Backlit_Kb', 4775.0, 'Laptops'), ('IDP3091V04B', 'Dell XPS 13 9345 Snapdragon X Elite 32GB LPDDR5X 512GB SSD 13.4" FHD+ IPS 120Hz Win11 Graphite Backlit_Kb', 4750.0, 'Laptops'), ('KDP3091V0NG', 'DELL XPS 13 9350 Ultra 7‑256V 16GB LPDDR5X 1TB SSD 13.4" NoN-Touch 2K IPS 120Hz Win11 Platinum Backlit_KB', 4850.0, 'Laptops'), ('KDP3091V0MD', 'DELL XPS 13 9350 Ultra 7‑256V 16GB LPDDR5X 512GB SSD 13.4" FHD IPS 120Hz DOS Platinum Backlit_KB', 4550.0, 'Laptops'), ('127N0', 'Dell XPS-13 LDX13260 Core 5-320 8GB DDR5 512GB SSD 13.4" 3K (2880x1800) Touch Intel Graphics Win11 Eng_KB Sky', 2775.0, 'Laptops'), ('5M6GY', 'Dell 16 PLUS DB06250 2‑in‑1 Core Ultra-7-256V 16GB DDR5 1TB SSD 16" FHD+ Touch Win11 Ice Blue Backlit Eng_KB', 3100.0, 'Laptops'), ('G8MK9', 'Dell Inspiron LDC15255‑A117BLK‑PUS AMD Ryzen 7‑7730U 16GB DDR4 512GB SSD 15.6" FHD Touch Carbon Black Win11', 2200.0, 'Laptops'), ('LDH519100HM', 'Dell Pro 15 Essential PV15250 Core 3-100U 8GB 512GB SSD 15.6" FHD DOS ENG_KB Carbon Black', 1650.0, 'Laptops'), ('QCT1250-8GB512GB', 'Dell PRO Tower QCT1250 14th Gen Core i7-14700 8GB DDR5 512GB SSD DOS Eng/Arabic_KB+Mouse Black', 2850.0, 'Desktops'), ('', 'Dell PRO Tower QCT1250 14th Gen Core i5-14500 8GB DDR5 512GB SSD DOS Eng/Arabic_KB+Mouse Black', 2300.0, 'Desktops'), ('21Y6002NGR', 'Lenovo ThinkPad E14 Gen 8 Ultra 7 355 16GB DDR5 512GB SSD 14" WUXGA IPS DOS Backlit E/A_KB Black With C. Case', 4250.0, 'Laptops'), ('83DU004VUS', 'Lenovo IdeaPad 5i 2-in-1 Core 5-120U 16GB 512GB SSD 16” WUXGA (1920x1200) IPS Touch X360 Win11 FPR Luna Grey', 2475.0, 'Laptops'), ('83K1008BAX', 'Lenovo IdeaPad Slim 3 15IRH10 Cori5-13420H 8GB DDR5 512GB SSD 15.3" WUXGA IPS DOS Luna Grey Eng_Arabic KB', 1875.0, 'Laptops'), ('12UD00C2GP', 'Lenovo ThinkCentre Neo 50T Gen 5 Tower 14th Gen Core i3-14100 8GB DDR5 512GB SSD DOS USB KeyBoard & Mouse', 1750.0, 'Desktops'), ('EP2-65380', 'Microsoft Surface Pro 12th Edition Copilot+ PC Snapdragon X Elite 32GB 1TB SSD 13" OLED Touch Win11 Platinum', 8100.0, 'Tablets'), ('ZID-00001', 'Microsoft Surface Pro 11th Edition Snapdragon X Elite 32GB 1TB SSD 13" OLED Touch Win11 Platinum', 7500.0, 'Tablets'), ('EP2-23855', 'Microsoft Surface Pro 11 Combo With KB+Slim Pen Snapdragon X Elite 16GB 1TB SSD 13" OLED Touch Win11 Graphite', 5950.0, 'Tablets'), ('EP2-73275', 'Microsoft Surface Pro 13" 12th Edition Copilot+ PC Snapdragon X Plus CPU 16GB 512GB 13" 3K (2880x1920) PixelSense Flow Touchscreen Qualcomm Adreno Graphics Win11Home Black', 4950.0, 'Tablets'), ('EP2-05006', 'Microsoft Surface Pro 12 11th Edition Copilot+ PC Snapdragon X Elite CPU 16GB 265GB 13" 3K (2880x1920) PixelSense Flow Touchscreen Qualcomm Adreno Graphics Win11Home Black', 4200.0, 'Tablets'), ('EP2-33671', 'Microsoft Surface Pro 12th Edition Copilot+ PC Snapdragon X Plus CPU 16GB 512GB 12" Touchscreen Win11Home Platinum', 4150.0, 'Tablets'), ('8X6-00214', 'Microsoft Surface KeyBoard With Slim Pen Platinum', 800.0, 'Docks & accessories'), ('8X6-00168', 'Microsoft Surface KeyBoard With Slim Pen Black', 800.0, 'Docks & accessories'), ('', 'Surface Adapter Model: JTY-00013 USB-C to USB 3.0', 55.0, 'Docks & accessories'), ('866724-0200/866724-0100', 'BOSE Quietcomfort-45 Noise Cancelling Headphone White Smoke/ Black', 'CALL', 'Docks & accessories'), ('MXJ92LL/A', 'BEATS Studio-3 Wireless Noise Cancelling Headphone Gray', 'CALL', 'Docks & accessories'), ('MX432LL/A  MT293LL/A', 'BEATS Solo-3 Wireless Headphone Black/Silver', 'CALL', 'Docks & accessories'), ('', 'JBL Flex True Wireless Noise Cancelling Earphone', 250.0, 'Docks & accessories')]

def clean(s):
    return re.sub(r"\s+", " ", str(s).replace("\u2011","-").replace("\u202f"," ").replace("\u201d", '"').replace("\u00d7","x")).strip()

def cpu_tag(text):
    t=text.lower().replace("cori","core i")
    for n in ("9","7","5","3"):
        if re.search(rf"\bultra[ -]?{n}\b|\bcore ultra[ -]?{n}\b", t): return f"Intel Ultra {n}"
    for n in ("9","7","5","3"):
        if re.search(rf"\bcore i{n}\b", t): return f"Intel Core i{n}"
    for n in ("7","5","3"):
        if re.search(rf"\bcore(?:™)?[ -]?{n}\b", t): return f"Intel Core {n}"
    for n in ("9","7","5","3"):
        if re.search(rf"\bryzen(?: ai)?[ -]?{n}\b", t): return f"AMD Ryzen {n}"
    if "snapdragon" in t: return "Snapdragon"
    return None

def gpu_tag(text):
    t=text.upper().replace(" ","")
    for model in ("5090","5080","5070TI","5070","5060TI","5060","5050","4070","4060","4050","3060","3050"):
        if ("RTX"+model) in t: return "RTX " + model.replace("TI"," Ti")
    return "Integrated"

CPU_RE = re.compile(r"\b(?:(?:12th|13th|14th)\s+Gen\s+)?(?:Core\s+Ultra|Ultra|Core™?|Cori|AMD\s+Ryzen|Ryzen|(?:AI\s+Qualcomm\s+)?Snapdragon)\b", re.I)

def make_title_specs(p, desc, cat):
    p=clean(p).replace(" /  / "," / "); d=clean(desc)
    if cat in ("Docks & accessories","Monitors"):
        if cat=="Monitors":
            m=re.search(r'\b\d+(?:\.\d+)?\"', d); title=(d[:m.start()].strip() if m else d); specs=(d[m.start():].strip() if m else "MONITOR")
        else: title=d; specs="ACCESSORY"
    else:
        m=CPU_RE.search(d); title=d[:m.start()].strip(" ,-") if m else d; specs=d[m.start():].strip() if m else "SEE DESCRIPTION"
    title=clean(title).upper(); specs=clean(specs).upper()
    specs=re.sub(r"\bCORI([3579])\b", r"INTEL CORE i\1", specs, flags=re.I)
    specs=re.sub(r"\bWIN11PRO\b", "WINDOWS 11 PRO", specs, flags=re.I); specs=re.sub(r"\bWIN11HOME\b", "WINDOWS 11 HOME", specs, flags=re.I); specs=re.sub(r"\bWIN11\b", "WINDOWS 11", specs, flags=re.I)
    specs=specs.replace("BACKLITE", "BACKLIT").replace("ENG_KB","ENGLISH KEYBOARD").replace("ENG-KB","ENGLISH KEYBOARD").replace("BACKLIT_KB","BACKLIT KEYBOARD")
    specs=re.sub(r"\s+(?=\d+(?:GB|TB)\s+(?:DDR\d|LPDDR\d|SSD)\b)", " | ", specs); specs=re.sub(r'\s+(?=\d+(?:\.\d+)?\"\s)', " | ", specs); specs=re.sub(r"\s+(?=WINDOWS\s+11|DOS\b|RTX\s*\d{4})", " | ", specs); specs=re.sub(r"\s*\|\s*", " | ", specs)
    if p:
        if p.upper() not in title: title=f"{title} - {p}"
        if p.upper() not in specs: specs=f"{specs} | {p}"
    return p,title,specs

def jsq(s): return '"' + str(s).replace("\\","\\\\").replace('"','\\"').replace("\n","\\n") + '"'

def make_block(p, desc, price, cat, is_last=False):
    p,t,s=make_title_specs(p,desc,cat)
    if isinstance(price,str) and price.upper()=="CALL": a='"CALL"'; price_line="PRICE ON REQUEST — CALL"
    else: n=int(float(price)); a=str(n); price_line=f"AED {n} + VAT"
    f=f"🔺 {t} 🔺BRAND NEW\n| {s} | MANUFACTURE WARRANTY ONLY\n{price_line}\n-------------------"
    lines=["    {",f"      p: {jsq(p)},",f"      t: {jsq(t)},",f"      s: {jsq(s)},",f"      a: {a},",f"      v: {jsq(VENDOR)},",f"      c: {jsq(cat)},",f"      f: {jsq(f)},"]
    if cat in ("Laptops","Desktops"):
        cpu=cpu_tag(desc)
        if cpu: lines.append(f"      cpu: {jsq(cpu)},")
        lines.append(f"      gpu: {jsq(gpu_tag(desc))},")
    lines.append("    }" + ("" if is_last else ",")); return "\n".join(lines)+"\n"

path=Path("index.html"); text=path.read_text(encoding="utf-8"); anchor="  const ITEMS = ["; start=text.index(anchor)+len(anchor); end=text.index("\n  ];", start); body=text[start:end]
lines=body.splitlines(keepends=True); kept=[]; cur=[]; old_count=0
for line in lines:
    if not cur:
        if re.match(r"^\s{4}\{\s*$", line): cur=[line]
        else: kept.append(line)
    else:
        cur.append(line)
        if re.match(r"^\s{4}\},?\s*$", line):
            block="".join(cur)
            if 'v: "Florence"' in block: old_count += 1
            else: kept.append(block)
            cur=[]
if cur: raise RuntimeError("Unclosed item block while parsing ITEMS")
kept_body="".join(kept).rstrip()
if kept_body and re.search(r"\n\s{4}\}$", kept_body): kept_body += ","
new_blocks="\n" + "".join(make_block(*row, is_last=(i==len(ROWS)-1)) for i,row in enumerate(ROWS)); new_body=kept_body+new_blocks; updated=text[:start]+new_body+text[end:]
new_count=updated.count('v: "Florence"')
if new_count != len(ROWS): raise RuntimeError(f"Florence count check failed: {new_count}")
if len(ROWS)!=62: raise RuntimeError(f"Expected 62 Florence items, got {len(ROWS)}")
path.write_text(updated, encoding="utf-8")
print(f"Replaced {old_count} Florence items with {len(ROWS)} items.")
