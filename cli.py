"""CLI for the simplified Binance Futures bot.

Supports interactive mode and command-line arguments. Uses .env or environment variables
for API keys (or prompts for them securely). Provides market, limit, stop-limit and TWAP.
"""
import argparse
import os
import sys
import time
import getpass
from typing import Any

from dotenv import load_dotenv

from bot import BasicBot


def parse_args():
    p = argparse.ArgumentParser(description="Binance Futures Testnet Trading CLI")
    p.add_argument("--api-key", help="API key (or set BINANCE_API_KEY or use .env)")
    p.add_argument("--api-secret", help="API secret (or set BINANCE_API_SECRET or use .env)")
    p.add_argument("--symbol", help="Trading pair symbol, e.g. BTCUSDT")
    p.add_argument("--side", choices=["BUY", "SELL"], help="BUY or SELL")
    p.add_argument("--type", choices=["market", "limit", "stop_limit", "twap"], default="market", help="Order type")
    p.add_argument("--quantity", type=float, help="Quantity to trade")
    p.add_argument("--price", type=float, help="Price for limit/stop-limit")
    p.add_argument("--stop-price", type=float, help="Stop price for stop-limit")
    p.add_argument("--slices", type=int, default=5, help="TWAP slices")
    p.add_argument("--interval", type=int, default=1, help="TWAP interval seconds")
    p.add_argument("--testnet", action="store_true", default=True, help="Use testnet URL (default: True)")
    return p.parse_args()


def get_credentials(args) -> tuple[str, str]:
    # Load .env if present
    load_dotenv()

    api_key = args.api_key or os.getenv("BINANCE_API_KEY")
    api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET")

    if not api_key:
        api_key = input("Enter API Key: ")
    if not api_secret:
        # prefer hidden input
        api_secret = getpass.getpass("Enter API Secret (hidden): ")

    return api_key.strip(), api_secret.strip()


def interactive_flow(bot: BasicBot):
    print("\n=== Binance Futures Trading Bot (Testnet) ===\n")
    symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
    side = input("Side (BUY/SELL): ").strip().upper()
    if side not in {"BUY", "SELL"}:
        print("Invalid side; must be BUY or SELL")
        sys.exit(1)
    print("Order Types:\n1. Market\n2. Limit\n3. Stop-Limit\n4. TWAP")
    choice = input("Select (1/2/3/4): ").strip()
    qty = float(input("Quantity: "))

    if choice == "1":
        print(bot.place_market_order(symbol, side, qty))
    elif choice == "2":
        price = float(input("Limit price: "))
        print(bot.place_limit_order(symbol, side, qty, price))
    elif choice == "3":
        price = float(input("Limit price: "))
        stop_price = float(input("Stop price: "))
        print(bot.place_stop_limit(symbol, side, qty, price, stop_price))
    elif choice == "4":
        slices = int(input("TWAP slices (e.g., 5): "))
        interval = int(input("Interval seconds between slices (e.g., 1): "))
        print(bot.place_twap(symbol, side, qty, slices=slices, interval_s=interval))
    else:
        print("Invalid choice")


def cli_mode(args):
    api_key, api_secret = get_credentials(args)
    bot = BasicBot(api_key, api_secret, testnet=args.testnet)

    if not args.symbol:
        return interactive_flow(bot)

    symbol = args.symbol.upper()
    side = (args.side or "BUY").upper()
    if side not in {"BUY", "SELL"}:
        print("Invalid side; choose BUY or SELL")
        sys.exit(1)

    if args.type == "market":
        if not args.quantity:
            print("--quantity is required for market order")
            sys.exit(1)
        res = bot.place_market_order(symbol, side, args.quantity)
        print(res)

    elif args.type == "limit":
        if not args.quantity or not args.price:
            print("--quantity and --price are required for limit order")
            sys.exit(1)
        res = bot.place_limit_order(symbol, side, args.quantity, args.price)
        print(res)

    elif args.type == "stop_limit":
        if not args.quantity or not args.price or not args.stop_price:
            print("--quantity, --price and --stop-price are required for stop-limit")
            sys.exit(1)
        res = bot.place_stop_limit(symbol, side, args.quantity, args.price, args.stop_price)
        print(res)

    elif args.type == "twap":
        if not args.quantity:
            print("--quantity is required for TWAP")
            sys.exit(1)
        print("Starting TWAP: slices=%s interval=%ss" % (args.slices, args.interval))
        res = bot.place_twap(symbol, side, args.quantity, slices=args.slices, interval_s=args.interval)
        print(res)


def main():
    args = parse_args()
    try:
        cli_mode(args)
    except KeyboardInterrupt:
        print("\nInterrupted by user")


if __name__ == "__main__":
    main()
