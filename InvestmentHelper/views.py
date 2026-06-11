from django.shortcuts import render

def investment_helper(request):
    recommendation = None

    if request.method == "POST":
        income = float(request.POST.get('income', 0))
        savings = float(request.POST.get('savings', 0))
        risk = request.POST.get('risk')

        # Simple logic for demo
        if risk == "low":
            recommendation = [
                "Fixed Deposits (FD)",
                "Public Provident Fund (PPF)",
                "Government Bonds"
            ]
        elif risk == "medium":
            recommendation = [
                "Mutual Funds",
                "Index Funds",
                "ETFs"
            ]
        elif risk == "high":
            recommendation = [
                "Stocks",
                "Cryptocurrency",
                "Startup Investments"
            ]

    return render(request, "InvestmentHelper/investment_helper.html", {
        "recommendation": recommendation
    })