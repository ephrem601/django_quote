from quotes.models import Quote
from django import forms
 
 
class QuoteForm(forms.ModelForm):
    quote_category = forms.ChoiceField(choices=Quote.USER_TYPE_CHOICES)
    owned_by =forms.CharField(max_length=200, required=False)
    quote = forms.CharField(widget=forms.Textarea)
     
    class Meta:
        model=Quote
        fields = ['quote_category','owned_by', 'quote']

  

