"""
╔══════════════════════════════════════════════════════════╗
║       STOCK PORTFOLIO TRACKER — CodeAlpha Internship     ║
║                        Task 2                            ║
╚══════════════════════════════════════════════════════════╝
"""

import csv
import os
from datetime import datetime


# ──────────────────────────────────────────────────────────
# Hardcoded stock price dictionary  (price in USD)
# ──────────────────────────────────────────────────────────
STOCK_PRICES: dict[str, float] = {
    "AAPL":  182.50,   # Apple Inc.
    "TSLA":  248.75,   # Tesla Inc.
    "GOOGL": 175.30,   # Alphabet Inc.
    "MSFT":  415.20,   # Microsoft Corp.
    "AMZN":  195.60,   # Amazon.com Inc.
    "META":  505.10,   # Meta Platforms
    "NFLX":  635.40,   # Netflix Inc.
    "NVDA":  875.90,   # NVIDIA Corp.
    "BABA":   85.00,   # Alibaba Group
    "UBER":   78.25,   # Uber Technologies
}

DIVIDER = "─" * 60


def show_available_stocks() -> None:
    print(f"\n{'TICKER':<8} {'COMPANY / PRICE (USD)':>30}")
    print(DIVIDER)
    company_names = {
        "AAPL": "Apple Inc.",      "TSLA": "Tesla Inc.",
        "GOOGL": "Alphabet Inc.",  "MSFT": "Microsoft Corp.",
        "AMZN": "Amazon.com Inc.", "META": "Meta Platforms",
        "NFLX": "Netflix Inc.",    "NVDA": "NVIDIA Corp.",
        "BABA": "Alibaba Group",   "UBER": "Uber Technologies",
    }
    for ticker, price in STOCK_PRICES.items():
        print(f"  {ticker:<8} {company_names[ticker]:<25} ${price:>8.2f}")
    print(DIVIDER)


def get_portfolio() -> list[dict]:
    """Interactively collect the user's stock holdings."""
    portfolio = []
    print("\n  Enter your stock holdings (type 'done' when finished).\n")

    while True:
        ticker = input("  Stock ticker (e.g. AAPL): ").strip().upper()
        if ticker == "DONE":
            break
        if ticker not in STOCK_PRICES:
            print(f"  ⚠  '{ticker}' not found. Available: {', '.join(STOCK_PRICES)}\n")
            continue

        # Quantity input with validation
        while True:
            qty_str = input(f"  Quantity of {ticker} shares: ").strip()
            try:
                qty = float(qty_str)
                if qty <= 0:
                    raise ValueError
                break
            except ValueError:
                print("  ⚠  Please enter a positive number.\n")

        price  = STOCK_PRICES[ticker]
        value  = price * qty

        # Avoid duplicates — add to existing holding
        for entry in portfolio:
            if entry["ticker"] == ticker:
                entry["quantity"] += qty
                entry["value"]    += value
                print(f"  ✅ Added {qty} more shares of {ticker}. "
                      f"Total holding: {entry['quantity']} shares.\n")
                break
        else:
            portfolio.append({"ticker": ticker, "quantity": qty,
                               "price": price, "value": value})
            print(f"  ✅ {ticker} added — {qty} shares @ ${price:.2f}\n")

    return portfolio


def display_portfolio(portfolio: list[dict]) -> None:
    if not portfolio:
        print("\n  Portfolio is empty.\n")
        return

    total = sum(p["value"] for p in portfolio)

    print(f"\n{'':=<60}")
    print(f"  📊  PORTFOLIO SUMMARY  —  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'':=<60}")
    print(f"  {'TICKER':<8} {'SHARES':>10} {'PRICE (USD)':>13} {'VALUE (USD)':>13} {'%':>6}")
    print(DIVIDER)

    for p in sorted(portfolio, key=lambda x: x["value"], reverse=True):
        pct = (p["value"] / total) * 100 if total else 0
        bar = "█" * int(pct / 5)       # simple visual bar (max 20 blocks)
        print(f"  {p['ticker']:<8} {p['quantity']:>10.2f} "
              f"${p['price']:>11.2f} ${p['value']:>11.2f} "
              f"{pct:>5.1f}%  {bar}")

    print(DIVIDER)
    print(f"  {'TOTAL INVESTMENT':.<40} ${total:>11.2f}")
    print(f"{'':=<60}\n")


def save_results(portfolio: list[dict], filename: str = "portfolio_report") -> None:
    """Save portfolio to both .txt and .csv files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    total = sum(p["value"] for p in portfolio)

    # ── Plain-text report ──────────────────────────────────
    txt_path = f"{filename}_{timestamp}.txt"
    with open(txt_path, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("       STOCK PORTFOLIO REPORT — CodeAlpha\n")
        f.write(f"       Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"  {'Ticker':<8} {'Shares':>10} {'Price':>12} {'Value':>12}\n")
        f.write("-" * 50 + "\n")
        for p in portfolio:
            f.write(f"  {p['ticker']:<8} {p['quantity']:>10.2f} "
                    f"${p['price']:>10.2f} ${p['value']:>10.2f}\n")
        f.write("-" * 50 + "\n")
        f.write(f"  {'TOTAL':<8} {'':>10} {'':>12} ${total:>10.2f}\n")
        f.write("=" * 60 + "\n")

    # ── CSV report ─────────────────────────────────────────
    csv_path = f"{filename}_{timestamp}.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ticker", "quantity", "price", "value"])
        writer.writeheader()
        writer.writerows(portfolio)
        writer.writerow({"ticker": "TOTAL", "quantity": "", "price": "", "value": round(total, 2)})

    print(f"  💾 Report saved → {txt_path}")
    print(f"  💾 Report saved → {csv_path}\n")


def main() -> None:
    print("\n" + "=" * 60)
    print("      📈  STOCK PORTFOLIO TRACKER  📈")
    print("=" * 60)

    show_available_stocks()
    portfolio = get_portfolio()
    display_portfolio(portfolio)

    if portfolio:
        save = input("  Save report to file? (y/n): ").strip().lower()
        if save == "y":
            save_results(portfolio)

    print("  Thank you for using Stock Portfolio Tracker! 👋\n")


if __name__ == "__main__":
    main()
