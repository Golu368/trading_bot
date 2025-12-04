from typing import Any, Dict, List
import traceback
import time

from binance.client import Client
from binance.exceptions import BinanceAPIException
from loguru import logger

from config import TESTNET_URL, LOG_FILE


logger.add(LOG_FILE, rotation="500 KB")


class BasicBot:
    """Simplified Binance Futures (USDT-M) bot wrapper.

    Provides market, limit, stop-limit, and TWAP helpers with logging.
    """

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret)

        if testnet:
            # Try to set common attributes that affect endpoints in some python-binance versions
            try:
                self.client.FUTURES_URL = TESTNET_URL
            except Exception:
                pass
            try:
                self.client.API_URL = TESTNET_URL
            except Exception:
                pass

        logger.info("Initialized BasicBot (testnet={})", testnet)

    def _log_order_call(self, method: str, params: Dict[str, Any]):
        logger.info("Request -> {}: {}", method, params)

    def _log_response(self, method: str, resp: Any):
        logger.info("Response <- {}: {}", method, resp)

    def _safe_execute(self, fn, *args, **kwargs):
        method = fn.__name__ if hasattr(fn, "__name__") else str(fn)
        try:
            self._log_order_call(method, {**kwargs})
            start = time.time()
            resp = fn(*args, **kwargs)
            elapsed = time.time() - start
            self._log_response(method, {"elapsed_s": round(elapsed, 4), "result": resp})
            return resp
        except BinanceAPIException as e:
            logger.error("BinanceAPIException in {}: {}", method, getattr(e, 'message', str(e)))
            return {"error": getattr(e, 'message', str(e))}
        except Exception as e:
            logger.error("Unexpected error in {}: {}", method, str(e))
            logger.debug("Traceback:\n{}", traceback.format_exc())
            return {"error": str(e)}

    # Market
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        params = dict(symbol=symbol, side=side, type="MARKET", quantity=quantity)
        return self._safe_execute(self.client.futures_create_order, **params)

    # Limit
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
        params = dict(symbol=symbol, side=side, type="LIMIT", timeInForce="GTC", price=price, quantity=quantity)
        return self._safe_execute(self.client.futures_create_order, **params)

    # Stop-Limit
    def place_stop_limit(self, symbol: str, side: str, quantity: float, price: float, stop_price: float) -> Dict[str, Any]:
        params = dict(symbol=symbol, side=side, type="STOP", timeInForce="GTC", price=price, stopPrice=stop_price, quantity=quantity)
        return self._safe_execute(self.client.futures_create_order, **params)

    # TWAP (simple): split into N market orders spaced by `interval_s`
    def place_twap(self, symbol: str, side: str, total_quantity: float, slices: int = 5, interval_s: int = 1) -> List[Dict[str, Any]]:
        if slices <= 0:
            raise ValueError("slices must be >= 1")
        results: List[Dict[str, Any]] = []
        base = float(total_quantity) / slices
        for i in range(slices):
            # For last slice, ensure rounding doesn't drop quantity
            qty = round(base, 8) if i < slices - 1 else round(total_quantity - base * (slices - 1), 8)
            logger.info("TWAP slice {}/{} placing market order qty={}", i + 1, slices, qty)
            res = self.place_market_order(symbol, side, qty)
            results.append(res)
            if i < slices - 1:
                time.sleep(interval_s)
        return results
from binance.client import Client
from binance.exceptions import BinanceAPIException
from loguru import logger
from config import TESTNET_URL, LOG_FILE

logger.add(LOG_FILE, rotation="500 KB")

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        self.client.FUTURES_URL = TESTNET_URL  # ensure testnet usage

        logger.info("Initialized bot with testnet mode: {}", testnet)

    # ---------------------- MARKET ORDER ---------------------- #
    def place_market_order(self, symbol, side, quantity):
        try:
            logger.info(
                "Market order request: symbol={}, side={}, qty={}",
                from typing import Any, Dict
                import traceback
                import time

                from binance.client import Client
                from binance.exceptions import BinanceAPIException
                from loguru import logger

                from config import TESTNET_URL, LOG_FILE


                logger.add(LOG_FILE, rotation="500 KB")


                class BasicBot:
                    """Simplified Binance Futures (USDT-M) bot wrapper.

                    Notes:
                    - Uses `python-binance` client; the repo should set `TESTNET_URL` in `config.py`.
                    - This class provides methods for market, limit, and stop-limit orders.
                    - All calls are logged to `LOG_FILE` configured in `config.py`.
                    """

                    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
                        self.client = Client(api_key, api_secret)

                        # Configure client's base URL for futures testnet if requested.
                        # The library internals may differ across versions; setting both
                        # known attributes helps ensure usage of the testnet endpoint.
                        if testnet:
                            try:
                                # `FUTURES_URL` is used in some python-binance builds
                                self.client.FUTURES_URL = TESTNET_URL
                            except Exception:
                                pass
                            try:
                                # Try setting API_URL as well (affects spot endpoints in some builds)
                                self.client.API_URL = TESTNET_URL
                            except Exception:
                                pass

                        logger.info("Initialized BasicBot (testnet={})", testnet)

                    def _log_order_call(self, method: str, params: Dict[str, Any]):
                        logger.info("Request -> {}: {}", method, params)

                    def _log_response(self, method: str, resp: Any):
                        logger.info("Response <- {}: {}", method, resp)

                    def _safe_execute(self, fn, *args, **kwargs):
                        """Execute a client function with logging and error handling."""
                        method = fn.__name__ if hasattr(fn, "__name__") else str(fn)
                        try:
                            self._log_order_call(method, {**kwargs})
                            start = time.time()
                            resp = fn(*args, **kwargs)
                            elapsed = time.time() - start
                            self._log_response(method, {"elapsed_s": round(elapsed, 4), "result": resp})
                            return resp
                        except BinanceAPIException as e:
                            logger.error("BinanceAPIException in {}: {}", method, e.message)
                            return {"error": e.message}
                        except Exception as e:
                            logger.error("Unexpected error in {}: {}", method, str(e))
                            logger.debug("Traceback:\n{}", traceback.format_exc())
                            return {"error": str(e)}

                    # ---------------------- MARKET ORDER ---------------------- #
                    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
                        """Place a market order on USDT-M futures."""
                        params = dict(symbol=symbol, side=side, type="MARKET", quantity=quantity)
                        return self._safe_execute(self.client.futures_create_order, **params)

                    # ---------------------- LIMIT ORDER ----------------------- #
                    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
                        """Place a limit order on USDT-M futures."""
                        params = dict(symbol=symbol, side=side, type="LIMIT", timeInForce="GTC", price=price, quantity=quantity)
                        return self._safe_execute(self.client.futures_create_order, **params)

                    # ---------------------- STOP-LIMIT ORDER ------------------ #
                    def place_stop_limit(self, symbol: str, side: str, quantity: float, price: float, stop_price: float) -> Dict[str, Any]:
                        """Place a stop-limit (STOP) order on USDT-M futures."""
                        params = dict(symbol=symbol, side=side, type="STOP", timeInForce="GTC", price=price, stopPrice=stop_price, quantity=quantity)
                        return self._safe_execute(self.client.futures_create_order, **params)
