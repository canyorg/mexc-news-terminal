# MEXC News Terminal

🇬🇧 English | 🇹🇷 [Türkçe](README.tr.md)

> ⚠️ **WARNING:** This tool opens **leveraged** futures positions **with real money**. It is meant only for people with **advanced market knowledge**. If you don't understand leverage, liquidation, funding and order-book liquidity, don't use it. Otherwise you **can lose all of your money.**

A terminal tool for opening futures positions **in one line, within seconds**, when big news breaks on Twitter/X or elsewhere, without clicking through an exchange UI.

```
> BTC long 500
  LONG BTC/USDT:USDT  50 contracts  entry ~66800  position ~500.00$  margin ~50.00$  take profit 67468
```

## Features

- **One-line orders:** `BTC long 500`, `ETH short 50`
- **10x isolated leverage** (default, configurable)
- Automatic **1% take profit** placed right after entry (reduce-only limit order; default, configurable)
- View positions, balance and funding rate; close a position with one command
- Built for **MEXC**, chosen for its low futures fees and zero-fee campaigns on some coins. Fees can vary by coin, campaign, and whether the order is placed via the API or the app; check the current rates on MEXC.
- **English and Turkish interface:** the language is asked at start; switch anytime with `lang`

## Installation

```bash
git clone https://github.com/canyorg/mexc-news-terminal.git
cd mexc-news-terminal
pip install -r requirements.txt
```

Requires Python 3.9+.

## Creating an API key (MEXC)

1. Log in to MEXC → profile → **API Management**.
2. Click **Create API**.
3. Tick only the **Futures** permissions:
   - ✅ View Account Details
   - ✅ View Order Details
   - ✅ Order Placing
   - ❌ **NEVER enable Withdraw**
4. If you can, **bind an IP address** (the key then only works from your IP).
5. Copy the **Access Key** and **Secret Key**. The Secret Key is shown only once.

### Why the API key matters

An API key is **like the password to your account.** Anyone who gets it can open and close trades in your name and deliberately drive your account into losses.

- **Never share it**, never send screenshots of it, never paste it into chats.
- **Never upload it to GitHub.** If you typed it into the file, remove it before sharing.
- Keep withdrawals disabled and bind an IP if possible.
- If you suspect the key has leaked, **delete it on MEXC immediately** and create a new one.

### Setting the key

The recommended way is **environment variables**, so the key never sits in the code:

```bash
# Linux / macOS
export MEXC_KEY="your_access_key"
export MEXC_SECRET="your_secret_key"

# Windows PowerShell
$env:MEXC_KEY="your_access_key"
$env:MEXC_SECRET="your_secret_key"
```

Alternatively, fill in `MEXC_KEY = ""` and `MEXC_SECRET = ""` at the top of `news_terminal.py`. In that case **don't share the file with anyone.**

## Usage

```bash
python news_terminal.py
```

| Command | What it does |
|---|---|
| `BTC long 500` | 500 $ LONG position (10x → 50 $ margin), take profit at +1% |
| `ETH short 50` | 50 $ SHORT position (10x → 5 $ margin), take profit at −1% |
| `BTC l 500` / `ETH s 50` | Short form |
| `pos` | Open positions (entry, PnL, liquidation price) |
| `bal` | Futures USDT balance |
| `fund LIT` | Funding rate and next funding time |
| `close BTC` | Close the position at market and cancel its orders |
| `lang` | Switch language (EN ⇄ TR) |
| `q` | Quit |

One-shot: `python news_terminal.py --lang en BTC long 500`

### Language

- At start the program asks `Language / Dil  [1] English  [2] Türkçe`.
- To skip the question: `python news_terminal.py --lang en` (or `--lang tr`).
- To make it permanent, use an environment variable: `export NT_LANG=en` (PowerShell: `$env:NT_LANG="en"`).
- Type `lang` while running to switch languages.
- Commands (`long`, `short`, `pos`, `bal`…) are the same in both languages.

> The number you type is the **position size**, not the margin. At 10x, `BTC long 500` uses about 50 $ of margin.

## Changing leverage and take profit

Defaults: **10x leverage, 1% take profit.**

**Option 1: environment variables (recommended)**

```bash
# Linux / macOS: 5x leverage, 0.5% take profit
LEVERAGE=5 TP_PCT=0.5 python news_terminal.py

# Windows PowerShell
$env:LEVERAGE="5"; $env:TP_PCT="0.5"; python news_terminal.py
```

**Option 2: change the defaults in the file**

Find these lines in `news_terminal.py` and change the number in quotes:

```python
LEVERAGE = int(os.getenv("LEVERAGE", "10"))        # "10" → your leverage
TP_PCT = float(os.getenv("TP_PCT", "1.0")) / 100   # "1.0" → your take-profit percent
```

> The higher the leverage, the closer the liquidation price is to your entry. At 10x isolated, liquidation comes after roughly a **9-9.5%** adverse move; about 4.5% at 20x, about 1.5% at 50x.

## Recommendations

- **Trade high-volume coins.** On low-volume coins the price slips very fast when news hits, your order fills worse than expected, and liquidation risk goes up. Prefer BTC, ETH and the top coins by 24h volume.
- Keep position size small relative to the coin's 24h volume.
- The tool **does not set a stop loss.** If you want one, set it manually on MEXC.
- Markets can whipsaw both ways on news; the first move isn't always the lasting one.
- MEXC has no testnet. Make your first tests with **very small amounts**.
- MEXC may not be available in every country; check the legal situation where you live.

## Disclaimer

This software is provided **"as is"**, without any warranty. **It is not investment advice.** Leveraged futures trading carries high risk and can result in the loss of all invested funds. The developer accepts **no liability** for any use of this tool, software bugs, exchange or API issues, delays, or any financial loss that may occur. By using this tool you accept all risk yourself.

## License

[MIT](LICENSE)
