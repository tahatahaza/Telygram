import requests
import time
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

# تعريف الحالات
START, ANALYZE_DEALS, ENABLE_NOTIFICATIONS, DISABLE_NOTIFICATIONS, ACTIVE_ANALYSIS = range(5)

# قائمة بأسماء الأصول المحللة مع بعض المعلومات الإضافية
assets = {
    "Bitcoin": {
        "market_name": "Bitcoin",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل بيتكوين",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Europe Composite Index": {
        "market_name": "Europe Composite Index",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل الأسواق الأوروبية",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Asia Composite Index": {
        "market_name": "Asia Composite Index",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل الأسواق الآسيوية",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "EUR/USD": {
        "market_name": "EUR/USD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج اليورو مقابل الدولار الأمريكي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "GBP/USD": {
        "market_name": "GBP/USD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الجنيه الإسترليني مقابل الدولار الأمريكي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "AUD/JPY": {
        "market_name": "AUD/JPY",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأسترالي مقابل الين الياباني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "AUD/USD": {
        "market_name": "AUD/USD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأسترالي مقابل الدولار الأمريكي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "BRENT": {
        "ma

rket_name": "BRENT",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل النفط الخام برنت",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "CAD/JPY": {
        "market_name": "CAD/JPY",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الكندي مقابل الين الياباني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Commodity Composite Index": {
        "market_name": "Commodity Composite Index",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل السلع المختلفة",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "DAX": {
        "market_name": "DAX",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر داكس الألماني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Dow Jones": {
        "market_name": "Dow Jones",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر داو جونز الصناعي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "EUR/AUD": {
        "market_name": "EUR/AUD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج اليورو مقابل الدولار الأسترالي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "EUR/CAD": {
        "market_name": "EUR/CAD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج اليورو مقابل الدولار الكندي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "EUR/GBP": {
        "market_name": "EUR/GBP",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج اليورو مقابل الجنيه الإسترليني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "EUR/JPY": {
        "market_name": "EUR/JPY",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج اليورو مقابل الين الياباني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Ethereum": {
        "market_name": "Ethereum",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل الإثيريوم",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "FTSE 100": {
        "market_name": "FTSE 100",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر فوتسي 100 البريطاني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "GBP/AUD": {
        "market_name": "GBP/AUD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الجنيه الإسترليني مقابل الدولار الأسترالي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "GBP/CAD": {
        "market_name": "GBP/CAD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الجنيه الإسترليني مقابل الدولار الكندي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "GBP/JPY": {
        "market_name": "GBP/JPY",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الجنيه الإسترليني مقابل الين الياباني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Gold": {
        "market_name": "Gold",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل الذهب",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Hang Seng Index": {
        "market_name": "Hang Seng Index",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر هانج سنغ الصيني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Litecoin": {
        "market_name": "Litecoin",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل الليتكوين",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "NASDAQ": {
        "market_name": "NASDAQ",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر ناسداك الأمريكي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Silver": {
        "market_name": "Silver",
        "trading_platform": "منصة التداول المثالية",


        "analysis": "تحليل الفضة",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "USD/CAD": {
        "market_name": "USD/CAD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأمريكي مقابل الدولار الكندي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "USD/JPY": {
        "market_name": "USD/JPY",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأمريكي مقابل الين الياباني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Basic Altcoin Index": {
        "market_name": "Basic Altcoin Index",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر العملات الرقمية الأساسي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "AUD/CAD": {
        "market_name": "AUD/CAD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأسترالي مقابل الدولار الكندي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Oasis Index": {
        "market_name": "Oasis Index",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر أواسيس",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "AUD/CHF": {
        "market_name": "AUD/CHF",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأسترالي مقابل الفرنك السويسري",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "AUD/NZD": {
        "market_name": "AUD/NZD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأسترالي مقابل الدولار النيوزيلندي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "CAC40": {
        "market_name": "CAC40",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر كاك 40 الفرنسي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "CAD/CHF": {
        "market_name": "CAD/CHF",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الكندي مقابل الفرنك السويسري",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "CHF/JPY": {
        "market_name": "CHF/JPY",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الفرنك السويسري مقابل الين الياباني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Copper": {
        "market_name": "Copper",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل النحاس",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "EUR/CHF": {
        "market_name": "EUR/CHF",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج اليورو مقابل الفرنك السويسري",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "EUR/NZD": {
        "market_name": "EUR/NZD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج اليورو مقابل الدولار النيوزيلندي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "EURO STOXX 50": {
        "market_name": "EURO STOXX 50",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر يورو ستوكس 50 الأوروبي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "GBP/CHF": {
        "market_name": "GBP/CHF",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الجنيه الإسترليني مقابل الفرنك السويسري",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "GBP/NZD": {
        "market_name": "GBP/NZD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الجنيه الإسترليني مقابل الدولار النيوزيلندي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "NZD/CAD": {
        "market_name": "NZD/CAD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار النيوزيلندي مقابل الدولار الكندي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "NZD/CHF": {
        "market_name": "NZ

D/CHF",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار النيوزيلندي مقابل الفرنك السويسري",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "NZD/JPY": {
        "market_name": "NZD/JPY",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار النيوزيلندي مقابل الين الياباني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "NZD/USD": {
        "market_name": "NZD/USD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار النيوزيلندي مقابل الدولار الأمريكي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Natural Gas": {
        "market_name": "Natural Gas",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل الغاز الطبيعي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Nikkei 225": {
        "market_name": "Nikkei 225",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر نيكي 225 الياباني",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Platinum": {
        "market_name": "Platinum",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل البلاتين",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "RUSSELL 2000": {
        "market_name": "RUSSELL 2000",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر راسل 2000 الأمريكي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "S&P 500": {
        "market_name": "S&P 500",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر S&P 500 الأمريكي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "USD/CHF": {
        "market_name": "USD/CHF",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأمريكي مقابل الفرنك السويسري",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "USD/MXN": {
        "market_name": "USD/MXN",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأمريكي مقابل البيزو المكسيكي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "USD/NOK": {
        "market_name": "USD/NOK",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأمريكي مقابل الكرونة النرويجية",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "USD/SGD": {
        "market_name": "USD/SGD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأمريكي مقابل الدولار السنغافوري",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "AUD/CAD": {
        "market_name": "AUD/CAD",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأسترالي مقابل الدولار الكندي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Arabian General Index": {
        "market_name": "Arabian General Index",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل المؤشر العام العربي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "BMW": {
        "market_name": "BMW",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل أسهم BMW",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Basic Dollar Index": {
        "market_name": "Basic Dollar Index",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل مؤشر الدولار الأساسي",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "AUD/USD OTC": {
        "market_name": "AUD/USD OTC",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل زوج الدولار الأسترالي مقابل الدولار الأمريكي (OTC)",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    },
    "Amazon": {
        "market_name": "Amazon",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل أسهم أمازون",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)


    },
    "Apple": {
        "market_name": "Apple",
        "trading_platform": "منصة التداول المثالية",
        "analysis": "تحليل أسهم أبل",
        "success_rate": 0.9,  # نسبة نجاح الصفقة (90٪)
    }
}

# قائمة لتخزين الأصول التي تم اختيارها للتحليل
selected_assets = []

# تعيين توكن البوت هنا
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# دالة بدء التنفيذ
def start(update, context):
    user = update.message.from_user
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"مرحبًا {user.first_name}، أهلاً بك في بوت تحليل الأسواق المالية!",
    )

    return ANALYZE_DEALS

# دالة للتحليل الآلي للصفقات
def analyze_deals(update, context):
    query = update.message.text.lower()

    # إذا تم اختيار الأمر "بدء التحليل"
    if query == "بدء التحليل":
        # إظهار لوحة المفاتيح للاختيار من بين الأصول المحتملة للتحليل
        reply_keyboard = [list(assets.keys())]
        update.message.reply_text(
            "من فضلك، اختر الأصول التي ترغب في تحليلها:",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="اختر الأصول"
            ),
        )
        return ENABLE_NOTIFICATIONS

    # إذا تم اختيار الأمر "تحليل"
    elif query == "تحليل":
        # إظهار الأصول التي تم اختيارها للتحليل ونتائج التحليل
        if len(selected_assets) > 0:
            message = "نتائج التحليل:\n\n"
            for asset in selected_assets:
                success_rate = assets[asset]["success_rate"] * 100
                message += (
                    f"أصل: {asset}\n"
                    f"نسبة نجاح الصفقة: {success_rate:.2f}%\n"
                    f"منصة التداول: {assets[asset][ trading_platform ]}\n"
                    f"تحليل: {assets[asset][ analysis ]}\n\n"
                )
            update.message.reply_text(message)
            selected_assets.clear()
        else:
            update.message.reply_text("لم يتم اختيار أي أصول للتحليل.")
        return ANALYZE_DEALS

    # إذا لم يتم اختيار أمر صالح
    else:
        update.message.reply_text("الرجاء استخدام الأوامر المتاحة فقط.")
        return ANALYZE_DEALS

# دالة لتفعيل إشعارات التحليل
def enable_notifications(update, context):
    # التأكد من أن الأمر المدخل هو اسم صالح للأصل
    selected_asset = update.message.text
    if selected_asset in assets:
        selected_assets.append(selected_asset)
        update.message.reply_text(f"تم اختيار {selected_asset} للتحليل.")
    else:
        update.message.reply_text("الرجاء اختيار أصول من القائمة فقط.")
    return ENABLE_NOTIFICATIONS

# دالة لإيقاف إشعارات التحليل
def disable_notifications(update, context):
    # التحقق من أن الأمر المدخل هو اسم صالح للأصل
    selected_asset = update.message.text
    if selected_asset in assets:
        if selected_asset in selected_assets:
            selected_assets.remove(selected_asset)
            update.message.reply_text(f"تم إزالة {selected_asset} من قائمة التحليل.")
        else:
            update.message.reply_text(f"{selected_asset} لم يتم اختياره للتحليل بعد.")
    else:
        update.message.reply_text("الرجاء اختيار أصول من القائمة فقط.")
    return ENABLE_NOTIFICATIONS

# دالة لإلغاء الأمر الحالي
def cancel(update, context):
    user = update.message.from_user
    update.message.reply_text(
        f"تم إلغاء الأمر الحالي، أهلاً بك مرة أخرى {user.first_name}!",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END

# دالة رئيسية لبدء التشغيل
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
 # إنشاء المحادثة وتعيين الدوال لكل حالة من حالات المحادثة
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ANALYZE_DEALS: [
                MessageHandler(Filters.regex("^(بدء التحليل)$"), analyze_deals),
                MessageHandler(Filters.regex("^(تحليل)$"), analyze_deals),
            ],
            ENABLE_NOTIFICATIONS: [
                MessageHandler(Filters.regex("^(تحليل)$"), analyze_deals),
                MessageHandle(
Filters.text & ~Filters.regex("^(تحليل)$"), enable_notifications
                ),
            ],
            DISABLE_NOTIFICATIONS: [
                MessageHandler(Filters.regex("^(تحليل)$"), analyze_deals),
                MessageHandler(
                    Filters.text & ~Filters.regex("^(تحليل)$"), disable_notifications
                ),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv_handler)

    # بدء التحديث
    updater.start_polling()

    # للتأكد من عدم إيقاف التشغيل حتى يتم إيقافه يدويًا
    updater.idle()

if __name__ == "__main__":
    main()