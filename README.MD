# Simplified Binance Futures Trading Bot (Testnet)

Overview
--------
This is a small, self-contained project to place orders on Binance Futures Testnet (USDT-M).

Features
--------
- Market, Limit and Stop-Limit orders
- Simple TWAP (time-weighted) order helper that slices a quantity into smaller market orders
- CLI: interactive and argument-based modes
- Logging of requests/responses/errors via `loguru`

Files
-----
- `bot.py` — `BasicBot` wrapper around `python-binance` futures calls
- `cli.py` — command-line interface (argparse + interactive fallback)
- `config.py` — testnet URL and `LOG_FILE` name
- `requirements.txt` — required Python packages
- `.env.example` — example for storing API keys

Setup (Windows PowerShell)
---------------------------
1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Provide API credentials

- Option A (recommended): create a `.env` file in this folder with:

```
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
```

- Option B: export environment variables `BINANCE_API_KEY` and `BINANCE_API_SECRET`.
- Option C: pass `--api-key` and `--api-secret` to the CLI (secret will show in process args — not recommended).

Usage
-----
Interactive mode (no args):

```powershell
python cli.py
```

Example: place a market order via args

```powershell
python cli.py --symbol BTCUSDT --side BUY --type market --quantity 0.001
```

TWAP example (5 slices, 2 second interval)

```powershell
python cli.py --symbol BTCUSDT --side SELL --type twap --quantity 0.01 --slices 5 --interval 2
```

Notes
-----
- Register and create API keys on Binance Futures Testnet and enable the required permissions.
- The client will attempt to use `https://testnet.binancefuture.com` as the futures endpoint (some `python-binance` versions require manual URL configuration).
- Logs are written to the filename defined in `config.py` (default `bot.log`). Include that log when you submit the assignment.
- Never commit real API keys to source control.

Limitations and testing
-----------------------
- This code performs live API calls when run; to test without network access, you can mock `bot.BasicBot` methods.

Next steps / Bonus ideas
------------------------
- Add OCO or native advanced order types (note: OCO is spot-only in Binance; for futures, implement conditional orders via stop/limit)
- Add a lightweight GUI using Flask or a simple TUI using `prompt_toolkit`
# Simplified Binance Futures Trading Bot (Testnet)

This repository contains a small, simplified trading bot wrapper and a CLI to place orders on the Binance Futures Testnet (USDT-M).

Files:
- `bot.py` — `BasicBot` wrapper that places market, limit, and stop-limit orders and logs requests/responses using `loguru`.
- `cli.py` — simple command-line interface to interact with `BasicBot`.
- `config.py` — testnet URL and log filename.
- `requirements.txt` — dependencies.

Setup (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Usage:

```powershell
python cli.py
```

Notes & Testnet setup:
- Register on Binance Futures Testnet and generate API key/secret.
- Use the Testnet base URL `https://testnet.binancefuture.com` (already in `config.py`).
- This code uses `python-binance` futures create order calls. Depending on the installed `python-binance` version, you may need to confirm that the library respects the `FUTURES_URL`/`API_URL` attributes used in `bot.py`.

Logging:
- All requests/responses and errors are recorded to the log file defined in `config.py` (default: `bot.log`).

Security:
- Never commit real API keys.
# Binance Futures Testnet Trading Bot

A simplified trading bot for Binance USDT-M Futures (Testnet).  
Created as part of a hiring assessment.

## Features
- Market Orders
- Limit Orders
- Stop-Limit Orders (Bonus)
- Logging (API requests, responses and errors)
- CLI interface with validation
- Clean and modular code structure

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
