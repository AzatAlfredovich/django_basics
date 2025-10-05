from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def contacts(request):
    return render(request, "contacts.html")

def contact_message(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")\

        return HttpResponse(f"Спасибо, {name}! Ваше сообщение отправлено!")
    return render(request, 'contacts.html')