import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import math
token = ''
bot = telebot.TeleBot(token)

current_expression = ""
a = {}
def calculator_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keys = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+',
        'C', '(', ')', '⌫',
        '√', 'x²', '%', '1/x'
    ]
    markup.add(*keys)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global current_expression
    current_expression = ""
    bot.send_message(message.chat.id, "Привет! Это телеграмм бот", reply_markup=calculator_keyboard())


@bot.message_handler(func=lambda message: True)
def process_calculation(message):
    global current_expression
    input_text = message.text.strip()
    if  message.chat.id in a:
      try:bot.delete_message(message.chat.id,a[message.chat.id])
      except:pass
    if input_text == '=':
        try:

            result = eval(current_expression)
            if current_expression == '':
              bot.send_message(message.chat.id, 'Введите число')
            bot.send_message(message.chat.id, f"📈 Результат: {result}", reply_markup=calculator_keyboard())
            current_expression = ""
        except Exception as e:
            bot.send_message(message.chat.id, f"❗ Произошла ошибка: {e}. Проверьте ваше выражение.", reply_markup=calculator_keyboard())
    elif input_text == 'C':
        current_expression = ""
        bot.sen_message(message.chat.idsage, "🖊️ Текущее выражение очищено.", reply_markup=calculator_keyboard())
    elif input_text == '⌫':
        current_expression = current_expression[:-1]
        s = bot.send_message(message.chat.id, f"🔙 Текущее выражение: {current_expression}", reply_markup=calculator_keyboard())
        a[message.chat.id]=s.message_id

    elif input_text == "1/x":
        if  int(current_expression) == 0:
            bot.send_message(message.chat.id,'На ноль делить нельзя')
        else:
            current_expression = 1/int(current_expression)
            current_expression = str(current_expression)
    elif input_text=='%':
        current_expression = int(current_expression)/100
        current_expression = str(current_expression)
    elif input_text=='x²':
        current_expression= int(current_expression)**2
        current_expression = str(current_expression)
    elif  input_text=='√':
        current_expression= math.sqrt(int(current_expression))
        current_expression = str(current_expression)
    elif input_text=='/':

            current_expression = current_expression + '/'
    else:

        current_expression += input_text
        bot.send_message(message.chat.id, f"✅ Текущее выражение: {current_expression}", reply_markup=calculator_keyboard())

bot.polling()
