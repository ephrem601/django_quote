def handle_message(update):
     
    text = update.message.text
    print(text)
     
    # Find a statement that matches the user's text
    # quote = Quote.objects.filter(
    #     text__icontains=text,
    #     emotion_type__icontains=text
    # ).order_by('?').first()

    # If a statement is found, send it to the user
    # if text:
    #     bot.send_message(update.message.chat_id, "text")


def create_quote(request):
    if request.method == 'POST':
        emotion = request.POST.get('emotion_type')
        print(emotion)
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()  # create a new Quote object and save it to the database
            return redirect('quotes:show-quotes', emotion_type=emotion)  # redirect to the quote detail page
    else:
        form = QuoteForm()

    return render(request, 'quotes/create_quote.html', {'form': form})


def quote_view(request, emotion_type):
    quote = Quote.objects.filter(emotion_type=emotion_type).annotate(random=Random()).order_by('random').first()
    text=Quote.objects.all()
    context = {
        'quote':quote,
    }
     
    return render(request, 'quotes/list_quote.html', context)


from telegram.ext import (
        Updater, 
        CommandHandler, 
        MessageHandler, 
        Filters
    )
# from googlemaps import Client as GoogleMaps
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
import logging
import requests
import nltk
import io
import numpy as np
import random
import string
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 

# # Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [
                    ['/start', '/info', '/quiz', '/joke'],
                    ['/physics', '/channel', '/clear', '/first']
                ]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

# update.message.reply_text('Bye! Hope to see you again next time.',
#                               reply_markup=ReplyKeyboardRemove())

# def start(update, context):
#     print("starting...")
#     update.message.reply_text("To continue press\n /{}".format(info(update, context)), reply_markup=markup)

def start(update, context):
    msg_get = update.message
    context.user_data['username']= msg_get.from_user.first_name
    data = context.user_data['username']
    data = "{}".format(data)
    data = str(data)
    text = '''
    Hi {} Welcome to /Bethlehem /Secondary /School /Chat /Bot. I am an /Intelligent /Robot. You can press the /links or the /buttons below to access the /resource that I have. You can also type any link on your /message /box to access me. for example when you type /quiz in your message dialog, I will directly takes you to the /quiz and so on. I may not be available unless the /background /software runs on me that helps me to chat with you. Have a good time with me.

    * /start \n  
    * /info  \n  
    * /quiz \n 
    *  visite @bethlehemschool\n 
    * physics  \n
        
    Thanks in advance !!
    contact @: 
    ephremnigussie7@gmail.com
    https://github.com/ephrem601/
    https://twitter.com/@EphremOfficials
    https://m.facebook.com/ephrem.nigussie.125

    '''.format(data)
    update.message.reply_text(text=text, reply_markup=markup)
   
# @bot.message_handler(content_types=['location'])
# def handle_location(message):
#     print("{0}, {1}".format(message.location.latitude, message.location.longitude))

def info(update, context):
    msg = update.message
    context.user_data['text']=msg.text
    context.user_data['firstname']=msg.from_user.first_name
    firstname=context.user_data['firstname']
    chatId= msg.chat_id
    data = 'Welcome /'+firstname+' \nYour Chat ID is /'+str(chatId) 
    
    data = str(data)
    update.message.reply_text(data)
     
    #update.message.reply_text(data) 


def quiz_test(update, context):
    return update.message.reply_text("Please Select a subject\n for physics t.me/QuizBot?start=RWN3JIKR")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Similarity search NLTK Learn
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey")
GREETING_RESPONSES = ["hi", "hey", "*node*", "hello", "I am glad", "you are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            # return random.choice(GREETING_RESPONSES) returns chices randomly
            return GREETING_RESPONSES


def learn_physics(update, context):
    print("starting physics lesson...")
    msg = update.message
    context.user_data['text']=msg.text
     
    context.user_data['username']=msg.from_user.first_name
    # username=context.user_data['username']
    warnings.filterwarnings('ignore')
    f=open('physics.txt','r', errors='ignore')
    raw=f.read()
    raw=raw.lower()#convert to lowercase
    sent_tokens=nltk.sent_tokenize(raw) #convert to list of sentences
    # word_tokens=nltk.word_tokenize(raw)#convert to list of words
    lammer=nltk.stem.WordNetLemmatizer()

    def lemmatizeToken(tokens):
        return [lammer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct), None)for punct in string.punctuation)

    def lematizeNormalize(text):
        return lemmatizeToken(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    def response(user_response):
    
        chatbot_response =''
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=lematizeNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals  = np.array(cosine_similarity(tfidf[-1], tfidf))
        
        idx = np.argsort(vals)
        idx = idx[0][-2] 
        flat = vals.flatten()
        flat = np.array(flat)
        flat = np.sort(flat)
        
        req_tfidf = flat[-1]
        if req_tfidf==0:
            chatbot_response = chatbot_response+"I am sorry! I don't unserstand you"

        else:
            chatbot_response = chatbot_response+sent_tokens[idx]
            
            return chatbot_response

    flag = True
    
    if flag==True:
        
        user_response = context.user_data['text']
        user_response = user_response.lower()
        
        if user_response !='bye':
        
            if user_response=='thanks' or user_response=='thank you':
                flag = False
                print("Chatbot: you are welcome")
            
            else:
                if greeting(user_response)!=None:
                    update.message.reply_text("Chatbot: \n"+greeting(user_response))
                else: 
                    response_to_telegram_console =response(user_response)
                    response_to_telegram_console = str(response_to_telegram_console)  
                    update.message.reply_text(response_to_telegram_console)
                    print("Definition: \n",response(user_response))
                    sent_tokens.remove(user_response)
            
        else:
            flag = False
            print("Chatbot : Bye! take care..")

 
def main():
    print("Running...")
    bot_token = "<token>"
     
    updater = Updater(bot_token, use_context=True)
    # a dispatcher disconnects from the server
    
    dp = updater.dispatcher

    # Get the dispatcher to register to handler
    dp.add_handler(CommandHandler('start', start, pass_user_data=True))
    dp.add_handler(CommandHandler('info', info))
    dp.add_handler(CommandHandler('quiz',quiz_test))
     
    dp.add_handler(MessageHandler(Filters.text, learn_physics))
    
    updater.start_polling()

      

     
    updater.idle()


if __name__ == '__main__':
    
    main()

#///////////////////////////////
class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = StudentForm
    template_name = "attendance/staff_edit.html"
     
    def get_success_url(self):
        return reverse('attendance:student')
    

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = 'attendance/confirm_student_delete.html'
    success_url = reverse_lazy('attendance:student')
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Model instance deleted successfully.')
        return super().delete(request, *args, **kwargs)







def handle_message(request):
    update = request.POST.get('update')
    if update:
        text = update.message.text
        userName = update.message.from_user.first_name
        print(update.message.from_user.first_name)
        quote = Quote.objects.filter(quote_category__icontains=text).annotate(random=Random()).order_by('random').first()
        #for quote in quote_queryset:
        heading = f"{'-' * 15}\n {quote.quote_category} \n{'-' * 15}\n"
        body = f"{'-' * 60}\n {quote.quote} \n{'-' * 60}\n"
        text_send_to_bot =f"{heading}\n{body}\n"
        if quote:
            context = {
                'quote':'quote'
            }
            # print(f"{heading}\n{body}\n")
            bot.send_message(update.message.chat_id, text_send_to_bot)

        if request.is_ajax():
            # if the request was made via AJAX, return the context data in JSON format
            return JsonResponse(context)
        else:
        #     # otherwise, render the QR reader template with the context data
            return render(request, 'quotes/chat_list.html', context)
        #     #return render(request, "quotes/chat_list.html", context)
    else:
        # If the 'update' value is not provided, handle the error condition
        response = "No update value provided"
    return response






try:
            # Parse the incoming webhook data
            raw_data = request.body.decode('utf-8')
            data = json.loads(raw_data)
            
            update = Update.de_json(data, bot)  # Assuming `bot` is an instance of `telegram.Bot`
            #update = Update.de_json(json.loads(request.body), bot)  # Assuming `bot` is an instance of `telegram.Bot`
            context ={
                'response': None,
            }
            # Process the update
            if update is not None and hasattr(update, 'message') and update.message is not None:
                # handle_message(update)
                begin = start_up(update)
                if begin == '/start':
                    first_name = update.message.from_user.first_name
                    last_name = update.message.from_user.last_name
                    full_name = f"{first_name} {last_name}" if last_name else first_name
                    txt1 = "This bot provides you with inspiring quotes based on the keywords you type. Enjoy the uplifting experience! Tips for using the bot:\n"
                    txt2 = "-Enter a keyword related to the type of quote you're looking for, such as:\n"
                    txt3 = "-  Happiness\n-  Hope\n-  Love\n-  Success\n-  Empathy\n-  Beauty\n -  Fear\n -  Fact\n"
                    txt4 = "-You can also type about few letters of it such as Happ, Hop, Succ, Emp and so on"
                    info = f"Hello! {full_name},\n{txt1}\n{txt2}\n{txt3}\n{txt4}"

                    bot.send_message(update.message.chat_id, info)
                else:
                    response = handle_message(update)  # Assuming this function generates the response
                    context['response'] = response
                    print(response)
                    response_json = json.dumps(context)
                        # if the request was made via AJAX, return the context data in JSON format
                    return JsonResponse(response_json)
                       
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            error_message = "Invalid JSON data"
            return JsonResponse({"error": error_message}, status=400)
        except Exception as e:
            print("Exception:", e)
            error_message = "An error occurred"
            return JsonResponse({"error": error_message}, status=500)
    elif request.method == 'GET':
        # Handle the GET request and return an appropriate response
        return HttpResponse("This is the webhook endpoint...")
    else:
        return HttpResponse(status=405)  # Method not allowed
###

<p>Welcome, {{ userName }}!</p>
<p>Original text: {{ text }}</p>
<p>Text sent to the bot: {{ text_send_to_template }}</p>
{% block chat_list %}
<style>
    /* Custom styles for the chat page */
    .chat-container {
      max-width: 500px;
      margin: 0 auto;
      padding: 20px;
    }
    .message {
      margin-bottom: 20px;
    }
    .message .sender {
      font-weight: bold;
    }

    .message .timestamp {
      color: #777;
      font-size: 12px;
    }

    .message .content {
      margin-top: 5px;
    }
  </style>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  
  <div class="container">
    <div class="chat-container">
      <button id="my-button" class="btn btn-success">Send AJAX Request</button>
      <div class="message">
        <div class="sender">Welcome, {{ text }}!</div>
        <div class="timestamp">August 19, 2023 10:30 AM</div>
        <div class="content">
            Original text: {{ text }}
        </div>
      </div>
      <div class="message">
        <div class="sender">The Bot</div>
        <div class="timestamp">August 19, 2023 10:35 AM</div>
        <div class="content">
         <div id="quote-list">
            finibus metus nunc a ante.
          </div>
        </div>
      </div>
      <!-- Add more messages here -->
    </div>
  </div>
