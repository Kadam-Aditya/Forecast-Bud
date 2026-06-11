from django.shortcuts import render

def ai_chatbot(request):
    response = None
    user_message = None

    if request.method == "POST":
        user_message = request.POST.get("message")

        # 🔥 Simple demo AI logic
        if user_message:
            msg = user_message.lower()

            if "save" in msg:
                response = "💡 Tip: Try the 50/30/20 rule — 50% needs, 30% wants, 20% savings."
            
            elif "invest" in msg:
                response = "📈 Consider mutual funds, SIPs, or index funds for long-term growth."
            
            elif "budget" in msg:
                response = "📊 Track expenses and set monthly limits for each category."
            
            elif "stock" in msg:
                response = "📉 Stocks can be volatile. Diversify your portfolio to reduce risk."
            
            else:
                response = "🤖 I'm here to help with finance! Ask about saving, investing, or budgeting."

    return render(request, "AIChatbot/ai_chatbot.html", {
        "response": response,
        "user_message": user_message
    })