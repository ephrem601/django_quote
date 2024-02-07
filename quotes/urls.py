from django.urls import path
from quotes.views import(
    webhook, 
    create_quote,
    quote_view,
    QuoteUpdateView,
    QuoteDeleteView,
    handle_message,
     
)

app_name = 'quotes'

urlpatterns = [
    path('', create_quote, name='quotes'),
    path('list/', quote_view, name='list-quote'),
    path('edit/<slug:slug>/', QuoteUpdateView.as_view(), name='edit-quote'),
    path('delete/<slug:slug>/', QuoteDeleteView.as_view(), name='delete-quote'),
    path('webhook/',webhook, name='webhook'),
    path('telegram/',handle_message, name='telegram'),
]