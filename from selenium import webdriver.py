import requests
from bs4 import BeautifulSoup
import telebot
import yfinance as yf

token = "6468026632:AAEt-QUn6QcGy4LYDmb37R9ZjFgIgYXEFxs"
bot = telebot.TeleBot(token)

# Функция для получения процентного роста акций за последний месяц
def get_monthly_price_change(symbol):
    try:
        # Получаем данные о цене акции за последний месяц
        stock = yf.Ticker(symbol)
        price_change = stock.history(period='1mo')['Close'].pct_change().iloc[-1] * 100
        return f"{price_change:.2f}%"
    except Exception as e:
        print("Ошибка при получении процентного роста цены акции:", e)
        return None

# Функция для получения цены акции
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        current_price = stock.history(period='1d')['Close'].iloc[-1]
        return current_price
    except Exception as e:
        print("Ошибка при получении цены акции:", e)
        return None

# Функция для получения информации о популярных акциях
def get_popular_stocks():
    return ["AAPL", "GOOG", "AMZN"]

# Функция для получения информации о самых активно торгуемых акциях
def get_most_traded_stocks():
    try:
        url = "https://finance.yahoo.com/most-active"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')[1:]  # Пропускаем заголовок таблицы
        most_traded_stocks = []
        for row in rows:
            cells = row.find_all('td')
            symbol = cells[0].text
            most_traded_stocks.append(symbol)
        return most_traded_stocks[:5]  # Возвращаем только первые 5 акций (можно изменить количество)
    except Exception as e:
        print("Ошибка при получении информации о самых активно торгуемых акциях:", e)
        return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я бот, который показывает текущие цены на самые популярные акции и информацию о самых активно торгуемых акциях. Напиши /stocks, чтобы получить информацию.")

# Обработчик команды /popular_stocks
@bot.message_handler(commands=['popular_stocks'])
def send_popular_stocks_prices(message):
    popular_stocks = get_popular_stocks()
    response = "Текущие цены на популярные акции:\n"
    for stock_symbol in popular_stocks:
        price = get_stock_price(stock_symbol)
        if price is not None:
            response += f"{stock_symbol}: ${price:.2f}\n"
        else:
            response += f"{stock_symbol}: Не удалось получить цену\n"
    bot.reply_to(message, response)

# Обработчик команды /most_traded_stocks
@bot.message_handler(commands=['most_traded_stocks'])
def send_most_traded_stocks(message):
    most_traded_stocks = get_most_traded_stocks()
    response = "Самые активно торгуемые акции:\n"
    for stock_symbol in most_traded_stocks:
        response += f"{stock_symbol}\n"
    bot.reply_to(message, response)

# Обработчик команды /monthly_price_change
@bot.message_handler(commands=['monthly_price_change'])
def send_monthly_price_change(message):
    popular_stocks = get_popular_stocks()
    response = "Процентный рост акций за последний месяц:\n"
    for stock_symbol in popular_stocks:
        price_change = get_monthly_price_change(stock_symbol)
        if price_change is not None:
            response += f"{stock_symbol}: {price_change}\n"
        else:
            response += f"{stock_symbol}: Не удалось получить информацию\n"
    bot.reply_to(message, response)

# Запуск телеграм-бота
bot.polling()