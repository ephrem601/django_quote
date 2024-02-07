from django.shortcuts import render, redirect, get_object_or_404
from quotes.forms import QuoteForm
from django.db.models.functions import Random
from .models import Quote
from django.views.generic import View
import random
from django.http import JsonResponse, HttpResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import telegram 
from telegram import Update
# Define a function to handle incoming messages
from django.conf import settings
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.core import serializers

# bot_token = '6281201453:AAHy5KAq4BBbjXFMzjYYAINgDUpA6Nok1TY'
# bot = telegram.Bot(token=bot_token)
# webhook_url = 'https://f02f-102-218-51-116.ngrok-free.app/quotes/webhook/'
# bot.setWebhook(webhook_url)


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
         
        t = handle_message(request)
        context = {
            "txt": "t"
        }
         
        print(context)
        
        return JsonResponse(context)
         
    elif request.method == 'GET':
        return HttpResponse("Get method...")

def handle_message(request):
    raw_data = request.body.decode('utf-8')
    data = json.loads(raw_data)
    update = Update.de_json(data, bot)
    s=start_up(update)
    if s:
        bot.send_message(update.message.chat_id, s)
    if update:
        text = update.message.text
        userName = update.message.from_user.first_name
        quote = Quote.objects.filter(quote_category__icontains=text).annotate(random=Random()).order_by('random').first()
        
        if quote:
            heading = f"{'-' * 15}\n {quote.quote_category} \n{'-' * 15}\n"
            body = f"{'-' * 60}\n {quote.quote} \n{'-' * 60}\n"
            text_send_to_bot = f"{heading}\n{body}\n"
        
            bot.send_message(update.message.chat_id, text_send_to_bot)
            return text
#Development Server
def start_up(update):
    text = update.message.text
    if text=='/start': 
        txt = '''
         type hope to fine hope
        '''
        return txt
     

def create_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()  # create a new Quote object and save it to the database
            messages.success(request, 'Succeeded!')
            form = QuoteForm()
    else:
        form = QuoteForm()

    return render(request, 'quotes/create_quote.html', {'form': form})


def quote_view(request):
    #quote = Quote.objects.filter(quote_category=quote_category).annotate(random=Random()).order_by('random').first()
    quote=Quote.objects.all()
    context = {
        'quote_list':quote,
    }
    
    return render(request, 'quotes/list_quote.html', context)


class QuoteUpdateView(UpdateView):
    model = Quote
    form_class = QuoteForm
    template_name = "quotes/edit_quote.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
 
    def get_success_url(self):
        return reverse('quotes:list-quote')
    
    
class QuoteDeleteView(DeleteView):
    model = Quote
    template_name = 'quotes/delete_quote.html'
    success_url = reverse_lazy('quotes:list-quote')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Succeeded!')
        return super().delete(request, *args, **kwargs)