from app.data.fundamentals_data import fundamentals

def rank_metrics():
    metrics = ["PE", "EPS", "ROE", "Debt"]
    stocks = list(fundamentals.keys())
    ranked = {s: {} for s in stocks}

    for metric in metrics:
        reverse = metric != "Debt"
        sorted_stocks = sorted(
            stocks,
            key=lambda s: fundamentals[s][metric],
            reverse=reverse
        )
        for rank, stock in enumerate(sorted_stocks, start=1):
            ranked[stock][metric] = rank

    return ranked


def layman_insights(stock):
    f = fundamentals[stock]
    return {
        "PE": "Expensive" if f["PE"] > 0.7 else "Cheap",
        "EPS": "Strong earnings" if f["EPS"] > 0.7 else "Weak earnings",
        "ROE": "High returns" if f["ROE"] > 0.7 else "Low returns",
        "Debt": "Low debt" if f["Debt"] < 0.3 else "High debt"
    }


def top5_positives_risks(stock):
    f = fundamentals[stock]
    positives, risks = [], []

    if f["PE"] < 0.3: positives.append("Stock is undervalued")
    if f["EPS"] > 0.7: positives.append("Strong earnings growth")
    if f["ROE"] > 0.7: positives.append("Excellent profitability")
    if f["Debt"] < 0.3: positives.append("Low debt burden")

    if f["PE"] > 0.7: risks.append("Stock may be overpriced")
    if f["EPS"] < 0.3: risks.append("Weak earnings")
    if f["ROE"] < 0.3: risks.append("Poor profitability")
    if f["Debt"] > 0.7: risks.append("High debt risk")

    return {
        "positives": positives[:5],
        "risks": risks[:5]
    }
