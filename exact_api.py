from datetime import datetime

import requests

import config

HEADERS_BASE = {
    "Accept": "application/json",
}


def _headers(token):
    return {**HEADERS_BASE, "Authorization": f"Bearer {token}"}


def _get_json(token, url, params=None):
    resp = requests.get(url, headers=_headers(token), params=params)
    resp.raise_for_status()
    data = resp.json()
    # Exact Online wraps results in {"d": {"results": [...]}} or {"d": [...]}
    d = data.get("d", data)
    if isinstance(d, dict) and "results" in d:
        return d["results"]
    return d


def _get_all_json(token, url, params=None):
    """GET with automatic pagination — follows __next links."""
    all_results = []
    resp = requests.get(url, headers=_headers(token), params=params)
    resp.raise_for_status()
    data = resp.json()

    while True:
        d = data.get("d", data)
        if isinstance(d, dict) and "results" in d:
            all_results.extend(d["results"])
            next_url = d.get("__next")
        elif isinstance(d, list):
            all_results.extend(d)
            next_url = None
        else:
            all_results.append(d)
            next_url = None

        if not next_url:
            break
        resp = requests.get(next_url, headers=_headers(token))
        resp.raise_for_status()
        data = resp.json()

    return all_results


def _get_current_division(token):
    """Get the current division from /current/Me to bootstrap API calls."""
    url = f"{config.API_URL}/current/Me"
    results = _get_json(token, url, params={"$select": "CurrentDivision"})
    if isinstance(results, list):
        return results[0]["CurrentDivision"]
    return results["CurrentDivision"]


def get_divisions(token):
    """Get all divisions (entities) accessible to this account."""
    current_div = _get_current_division(token)
    url = f"{config.API_URL}/{current_div}/system/Divisions"
    results = _get_json(token, url, params={"$select": "Code,Description"})
    return results


def get_bank_gl_accounts(token, division):
    """Get bank and cash GL accounts for a division (Type 10=Cash, 12=Bank)."""
    url = f"{config.API_URL}/{division}/financial/GLAccounts"
    params = {
        "$filter": "Type eq 10 or Type eq 12",
        "$select": "ID,Code,Description,Type,TypeDescription",
    }
    return _get_json(token, url, params=params)


def get_reporting_balance(token, division, gl_account_id):
    """Get the current balance for a GL account by summing all reporting periods."""
    url = f"{config.API_URL}/{division}/financial/ReportingBalance"
    params = {
        "$filter": f"GLAccount eq guid'{gl_account_id}'",
        "$select": "Amount,ReportingYear,ReportingPeriod",
    }
    results = _get_all_json(token, url, params=params)
    if not results:
        return 0.0
    return sum(entry.get("Amount", 0) for entry in results)


def _parse_exact_date(date_str):
    """Parse Exact Online date format '/Date(ms)/' to a datetime."""
    if not date_str:
        return None
    import re
    match = re.search(r"/Date\((\d+)\)/", date_str)
    if not match:
        return None
    return datetime.fromtimestamp(int(match.group(1)) / 1000)


def get_last_transaction_date(token, division, gl_account_id):
    """Get the date of the most recent transaction for a GL account."""
    url = f"{config.API_URL}/{division}/financialtransaction/TransactionLines"
    params = {
        "$filter": f"GLAccount eq guid'{gl_account_id}'",
        "$select": "Date",
        "$orderby": "Date desc",
        "$top": "1",
    }
    results = _get_json(token, url, params=params)
    if not results:
        return None
    entry = results[0] if isinstance(results, list) else results
    return _parse_exact_date(entry.get("Date"))


def get_all_gl_accounts(token, division):
    """Get all GL accounts for a division."""
    url = f"{config.API_URL}/{division}/financial/GLAccounts"
    params = {
        "$select": "ID,Code,Description,Type,TypeDescription,BalanceType",
    }
    return _get_all_json(token, url, params=params)


def get_year_balances(token, division, year):
    """Get all reporting balances for a given fiscal year."""
    url = f"{config.API_URL}/{division}/financial/ReportingBalance"
    params = {
        "$filter": f"ReportingYear eq {year}",
        "$select": "GLAccount,GLAccountCode,GLAccountDescription,Amount,"
                   "AmountCredit,AmountDebit,BalanceType,ReportingPeriod",
    }
    return _get_all_json(token, url, params=params)


def get_annual_report_data(token, division, year):
    """Fetch and aggregate annual report data (balance sheet + P&L) for a fiscal year."""
    balances = get_year_balances(token, division, year)

    # Aggregate amounts per GL account
    accounts = {}
    for entry in balances:
        code = entry.get("GLAccountCode", "")
        key = code
        if key not in accounts:
            accounts[key] = {
                "code": code,
                "description": entry.get("GLAccountDescription", ""),
                "balance_type": entry.get("BalanceType", ""),
                "amount": 0.0,
                "amount_credit": 0.0,
                "amount_debit": 0.0,
            }
        accounts[key]["amount"] += entry.get("Amount", 0) or 0
        accounts[key]["amount_credit"] += entry.get("AmountCredit", 0) or 0
        accounts[key]["amount_debit"] += entry.get("AmountDebit", 0) or 0

    balance_sheet = []
    profit_loss = []
    for acct in sorted(accounts.values(), key=lambda a: a["code"]):
        if acct["balance_type"] == "B":
            balance_sheet.append(acct)
        elif acct["balance_type"] == "W":
            profit_loss.append(acct)

    # Assets: debit balances on balance sheet; Liabilities: credit balances
    total_assets = sum(a["amount"] for a in balance_sheet if a["amount"] > 0)
    total_liabilities = abs(sum(a["amount"] for a in balance_sheet if a["amount"] < 0))

    # Revenue: credit balances on P&L; Expenses: debit balances
    total_revenue = abs(sum(a["amount"] for a in profit_loss if a["amount"] < 0))
    total_expenses = sum(a["amount"] for a in profit_loss if a["amount"] > 0)
    net_result = total_revenue - total_expenses

    return {
        "balance_sheet": balance_sheet,
        "profit_loss": profit_loss,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_result": net_result,
    }


def get_bank_balances(token, division):
    """Get balances for all bank/cash accounts in a division."""
    accounts = get_bank_gl_accounts(token, division)
    balances = []
    for acct in accounts:
        gl_id = acct["ID"]
        balance = get_reporting_balance(token, division, gl_id)
        last_tx = get_last_transaction_date(token, division, gl_id)
        balances.append({
            "name": acct.get("Description") or "Unknown",
            "code": acct.get("Code", ""),
            "balance": balance,
            "last_transaction": last_tx,
        })
    return balances
