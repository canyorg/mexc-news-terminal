#!/usr/bin/env python3
"""
news_terminal.py - MEXC Futures one-line order terminal (ccxt) | EN / TR

Commands / Komutlar:
  BTC long 500   -> 500$ LONG  (10x => 50$ margin/teminat), take profit +1%
  ETH short 50   -> 50$ SHORT  (10x => 5$ margin/teminat),  take profit -1%
  pos            -> open positions / acik pozisyonlar
  bal            -> futures USDT balance / bakiye
  fund LIT       -> funding rate / funding orani
  close BTC      -> close at market / piyasadan kapat
  lang           -> switch language / dil degistir
  q              -> quit / cikis

Short form / Kisa yazim:  BTC l 500 | ETH s 50
One-shot / Tek seferlik:  python news_terminal.py BTC long 500

Language / Dil:  asked at start, or  --lang en | --lang tr  or  NT_LANG=en|tr
Settings / Ayarlar:  LEVERAGE (default 10), TP_PCT (default 1.0)
API keys / Anahtarlar:  MEXC_KEY, MEXC_SECRET  (environment variables / ortam degiskenleri)

NOTE: MEXC has no testnet - REAL MONEY.  |  MEXC'te test hesabi yok - GERCEK PARA.
"""
import os
import sys

try:
    import ccxt
except ImportError:
    sys.exit("ccxt missing / ccxt yok:  pip install -U ccxt")

# ====== API KEYS / API ANAHTARLARI ======================================================
# Prefer environment variables. NEVER commit real keys to GitHub.
# Ortam degiskeni kullan. Gercek anahtarlari ASLA GitHub'a yukleme.
MEXC_KEY = ""      # or env / ya da ortam degiskeni: MEXC_KEY
MEXC_SECRET = ""   # or env / ya da ortam degiskeni: MEXC_SECRET
# =======================================================================================

LEVERAGE = int(os.getenv("LEVERAGE", "10"))
TP_PCT = float(os.getenv("TP_PCT", "1.0")) / 100

LONG_WORDS = {"long", "l"}
SHORT_WORDS = {"short", "s"}

# MEXC: openType 1 = isolated, 2 = cross | positionType 1 = long, 2 = short
ISOLATED = 1

MSG = {
    "en": {
        "no_keys": "Set MEXC_KEY and MEXC_SECRET (environment variables or top of the file).",
        "connected": "[MEXC Futures] connected - REAL MONEY - {lev}x isolated - take profit {tp:g}%",
        "not_listed": "{s} is not listed on MEXC futures",
        "amount_pos": "amount must be positive",
        "warn_lev": "  warning (leverage): {e}",
        "too_small": "amount too small: at least ~{usd:.2f}$ ({n} contracts)",
        "tp_ok": "take profit {tp}",
        "tp_fail": "!!! TAKE-PROFIT ORDER FAILED: {e} - set it manually on MEXC !!!",
        "opened": "  {side} {s}  {amt:g} contracts  entry ~{entry}  position ~{real:.2f}$  "
                  "margin ~{margin:.2f}$  {tp}",
        "no_pos": "  no open positions",
        "pos_line": "  {s:<18} {side:<5} {c} contracts  entry {e}  PnL {pnl}  liq {liq}",
        "bal": "  balance: total {t}  available {f} USDT",
        "warn_bal": "  warning (balance): {e}",
        "fund_none": "  could not fetch funding for {s}",
        "longs_pay": "LONGs pay SHORTs",
        "shorts_pay": "SHORTs pay LONGs",
        "nobody": "nobody pays",
        "fund": "  {s} funding: {pct:.4f}%  ({who})  next payment: {nxt}",
        "fund_100": "  one payment on a 100$ position ~{v:.3f}$",
        "fund_high": "  !! high funding: the market is crowded on one side",
        "warn_cancel": "  warning (cancel orders): {e}",
        "no_pos_for": "  no open position for {s}",
        "closed": "  {s} {side} closed",
        "help": "  e.g.: BTC long 500 | ETH short 50 | pos | bal | fund LIT | close BTC | lang | q",
        "error": "  ERROR: {e}",
        "lang_set": "  language: English",
    },
    "tr": {
        "no_keys": "MEXC_KEY ve MEXC_SECRET tanimla (ortam degiskeni ya da dosyanin basi).",
        "connected": "[MEXC Futures] baglandi - GERCEK PARA - {lev}x izole - kar al %{tp:g}",
        "not_listed": "{s} MEXC futures'ta yok",
        "amount_pos": "tutar pozitif olmali",
        "warn_lev": "  uyari (kaldirac): {e}",
        "too_small": "tutar cok kucuk: en az ~{usd:.2f}$ ({n} kontrat)",
        "tp_ok": "kar al {tp}",
        "tp_fail": "!!! KAR AL EMRI ACILAMADI: {e} - MEXC'ten elle gir !!!",
        "opened": "  {side} {s}  {amt:g} kontrat  giris ~{entry}  pozisyon ~{real:.2f}$  "
                  "teminat ~{margin:.2f}$  {tp}",
        "no_pos": "  acik pozisyon yok",
        "pos_line": "  {s:<18} {side:<5} {c} kontrat  giris {e}  PnL {pnl}  likit {liq}",
        "bal": "  bakiye: toplam {t}  kullanilabilir {f} USDT",
        "warn_bal": "  uyari (bakiye): {e}",
        "fund_none": "  {s} funding bilgisi alinamadi",
        "longs_pay": "LONG'lar SHORT'lara oder",
        "shorts_pay": "SHORT'lar LONG'lara oder",
        "nobody": "kimse odemiyor",
        "fund": "  {s} funding: %{pct:.4f}  ({who})  sonraki odeme: {nxt}",
        "fund_100": "  100$ pozisyonda bir odeme ~{v:.3f}$",
        "fund_high": "  !! funding yuksek: piyasa tek tarafa yigilmis",
        "warn_cancel": "  uyari (emir iptali): {e}",
        "no_pos_for": "  {s} icin acik pozisyon yok",
        "closed": "  {s} {side} kapatildi",
        "help": "  ornek: BTC long 500 | ETH short 50 | pos | bal | fund LIT | close BTC | lang | q",
        "error": "  HATA: {e}",
        "lang_set": "  dil: Turkce",
    },
}

LANG = "en"


def t(key, **kw):
    return MSG[LANG][key].format(**kw)


def pick_language():
    """--lang en|tr  >  NT_LANG env  >  ask (interactive)  >  en"""
    global LANG
    args = sys.argv[1:]
    if "--lang" in args:
        i = args.index("--lang")
        if i + 1 < len(args):
            LANG = "tr" if args[i + 1].lower().startswith("tr") else "en"
            del args[i:i + 2]
        sys.argv = [sys.argv[0]] + args
        return
    env = os.getenv("NT_LANG", "").lower()
    if env in ("en", "tr"):
        LANG = env
        return
    if len(args) == 0 and sys.stdin.isatty():
        ans = input("Language / Dil  [1] English  [2] Türkçe : ").strip().lower()
        LANG = "tr" if ans in ("2", "tr", "türkçe", "turkce") else "en"


def connect():
    key = MEXC_KEY or os.getenv("MEXC_KEY")
    secret = MEXC_SECRET or os.getenv("MEXC_SECRET")
    if not key or not secret:
        sys.exit(t("no_keys"))
    ex = ccxt.mexc({
        "apiKey": key,
        "secret": secret,
        "enableRateLimit": True,
        "options": {"defaultType": "swap"},
    })
    # Spot coin list (fetch_currencies) needs spot API permission; not needed for futures
    ex.has["fetchCurrencies"] = False
    ex.options["fetchMarkets"] = ["swap"]
    ex.load_markets()
    print(t("connected", lev=LEVERAGE, tp=TP_PCT * 100))
    show_balance(ex)
    return ex


def sym(ex, coin):
    s = f"{coin.upper()}/USDT:USDT"
    if s not in ex.markets:
        raise ValueError(t("not_listed", s=s))
    return s


def order_params(extra=None):
    p = {"marginMode": "isolated", "openType": ISOLATED, "leverage": LEVERAGE}
    if extra:
        p.update(extra)
    return p


def open_trade(ex, coin, side, notional):
    if notional <= 0:
        raise ValueError(t("amount_pos"))
    s = sym(ex, coin)
    m = ex.markets[s]

    # Set leverage for this side (MEXC keeps long/short leverage separately)
    try:
        ex.set_leverage(LEVERAGE, s, {"openType": ISOLATED,
                                      "positionType": 1 if side == "long" else 2})
    except Exception as e:
        print(t("warn_lev", e=e))

    price = ex.fetch_ticker(s)["last"]
    csize = m.get("contractSize") or 1          # BTC_USDT: 1 contract = 0.0001 BTC
    amount = float(ex.amount_to_precision(s, notional / (price * csize)))
    min_amt = (m.get("limits", {}).get("amount", {}) or {}).get("min") or 1
    if amount < min_amt:
        raise ValueError(t("too_small", usd=min_amt * price * csize, n=min_amt))

    open_side = "buy" if side == "long" else "sell"
    tp_side = "sell" if side == "long" else "buy"

    order = ex.create_order(s, "market", open_side, amount, None, order_params())

    entry = order.get("average") or order.get("price")
    if not entry:
        try:
            entry = ex.fetch_order(order["id"], s).get("average")
        except Exception:
            pass
    entry = entry or price

    tp = entry * (1 + TP_PCT) if side == "long" else entry * (1 - TP_PCT)
    tp = float(ex.price_to_precision(s, tp))
    try:
        ex.create_order(s, "limit", tp_side, amount, tp, order_params({"reduceOnly": True}))
        tp_txt = t("tp_ok", tp=tp)
    except Exception as e:
        tp_txt = t("tp_fail", e=e)

    real = amount * entry * csize
    print(t("opened", side=side.upper(), s=s, amt=amount, entry=entry, real=real,
            margin=real / LEVERAGE, tp=tp_txt))


def show_positions(ex):
    pos = [p for p in ex.fetch_positions() if float(p.get("contracts") or 0) != 0]
    if not pos:
        print(t("no_pos"))
        return
    for p in pos:
        print(t("pos_line", s=p["symbol"], side=p.get("side", "?"), c=p.get("contracts"),
                e=p.get("entryPrice"), pnl=p.get("unrealizedPnl"), liq=p.get("liquidationPrice")))


def show_balance(ex):
    try:
        b = ex.fetch_balance({"type": "swap"}).get("USDT", {})
        print(t("bal", t=b.get("total"), f=b.get("free")))
    except Exception as e:
        print(t("warn_bal", e=e))


def show_funding(ex, coin):
    s = sym(ex, coin)
    f = ex.fetch_funding_rate(s)
    rate = f.get("fundingRate")
    nxt = f.get("fundingDatetime") or f.get("nextFundingDatetime")
    if rate is None:
        print(t("fund_none", s=s))
        return
    pct = rate * 100
    who = t("longs_pay") if rate > 0 else (t("shorts_pay") if rate < 0 else t("nobody"))
    print(t("fund", s=s, pct=pct, who=who, nxt=nxt))
    print(t("fund_100", v=abs(rate) * 100))
    if abs(pct) >= 0.05:
        print(t("fund_high"))


def close(ex, coin):
    s = sym(ex, coin)
    try:
        ex.cancel_all_orders(s)
    except Exception as e:
        print(t("warn_cancel", e=e))
    pos = [p for p in ex.fetch_positions([s]) if float(p.get("contracts") or 0) != 0]
    if not pos:
        print(t("no_pos_for", s=s))
        return
    for p in pos:
        side = "sell" if p["side"] == "long" else "buy"
        ex.create_order(s, "market", side, float(p["contracts"]), None,
                        order_params({"reduceOnly": True}))
        print(t("closed", s=s, side=p["side"]))


def handle(ex, line):
    global LANG
    parts = line.strip().split()
    if not parts:
        return True
    cmd = parts[0].lower()
    if cmd in ("q", "quit", "exit"):
        return False
    if cmd == "lang":
        LANG = "tr" if LANG == "en" else "en"
        print(t("lang_set"))
    elif cmd == "pos":
        show_positions(ex)
    elif cmd == "bal":
        show_balance(ex)
    elif cmd == "fund" and len(parts) == 2:
        show_funding(ex, parts[1])
    elif cmd == "close" and len(parts) == 2:
        close(ex, parts[1])
    elif len(parts) == 3 and parts[1].lower() in LONG_WORDS | SHORT_WORDS:
        side = "long" if parts[1].lower() in LONG_WORDS else "short"
        open_trade(ex, parts[0], side, float(parts[2]))
    else:
        print(t("help"))
    return True


def main():
    pick_language()
    ex = connect()
    if len(sys.argv) > 1:
        handle(ex, " ".join(sys.argv[1:]))
        return
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        try:
            if not handle(ex, line):
                break
        except Exception as e:
            print(t("error", e=e))


if __name__ == "__main__":
    main()
