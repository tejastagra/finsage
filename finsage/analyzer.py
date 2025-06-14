# finsage/analyzer.py

def sanitize_values(values):
    cleaned = []
    for v in values:
        if isinstance(v, str):
            v = v.replace('$', '').replace(',', '').strip()
        try:
            cleaned.append(float(v))
        except ValueError:
            continue
    return cleaned


def analyze_profit_and_loss(pl_data):
    revenue = pl_data.get("Revenue", {})
    costs = pl_data.get("Cost of Goods Sold", {})
    expenses = pl_data.get("Operating Expenses", {})
    net_profit = pl_data.get("Net Profit", 0)

    # Convert values
    revenue_items = [(k, float(str(v).replace('$', '').replace(',', '').strip())) for k, v in revenue.items()]
    cost_items = [(k, float(str(v).replace('$', '').replace(',', '').strip())) for k, v in costs.items()]
    expense_items = [(k, float(str(v).replace('$', '').replace(',', '').strip())) for k, v in expenses.items()]

    total_revenue = sum([v for _, v in revenue_items])
    total_expenses = sum([v for _, v in cost_items + expense_items])
    break_even = total_expenses - total_revenue if total_revenue < total_expenses else 0

    return {
        "top_revenue_drivers": sorted(revenue_items, key=lambda x: x[1], reverse=True)[:5],
        "top_cost_drivers": sorted(cost_items + expense_items, key=lambda x: x[1], reverse=True)[:5],
        "net_profit": float(str(net_profit).replace('$', '').replace(',', '').strip()),
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
        "break_even_capital": round(break_even, 2)
    }


def analyze_cash_flow(cf_data):
    inflows = cf_data.get("Operating Activities", {}).copy()
    inflows.update(cf_data.get("Investing Activities", {}))
    inflows.update(cf_data.get("Financing Activities", {}))

    inflow_values = sanitize_values([v for v in inflows.values() if v > 0])
    outflow_values = sanitize_values([v for v in inflows.values() if v < 0])

    sorted_inflows = sorted([(k, v) for k, v in inflows.items() if v > 0], key=lambda x: x[1], reverse=True)
    sorted_outflows = sorted([(k, abs(v)) for k, v in inflows.items() if v < 0], key=lambda x: x[1], reverse=True)

    return {
        "top_inflows": sorted_inflows[:5],
        "top_outflows": sorted_outflows[:5],
        "total_inflows": round(sum(inflow_values), 2),
        "total_outflows": round(abs(sum(outflow_values)), 2),
        "net_cash_flow": round(sum(inflow_values) + sum(outflow_values), 2)
    }

