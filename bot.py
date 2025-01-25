from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import logging

# Configurazione del logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Token del bot e ID canale
TOKEN_BOT = "7671310351:AAHyqTs5_i7qwMmmeXXsiPnJispekGYfXss"
CHANNEL_ID = "@topDealsAmaz0n"

# Stati della conversazione
LINK, IMAGE, DESCRIPTION = range(3)

# Funzione /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Benvenuto! Questo bot ti permette di creare post pubblicitari per il tuo canale affiliato Amazon. Usa il comando /help per vedere i comandi disponibili."
    )

# Funzione /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Inizia il bot\n"
        "/manda - Inizia la creazione di un post pubblicitario\n"
        "/annulla - Annulla l'operazione corrente\n"
        "/help - Mostra questo messaggio di aiuto"
    )

# Funzione per il comando /manda
async def manda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Invia il link del prodotto Amazon.")
    return LINK

# Gestione del link
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["link"] = update.message.text
    await update.message.reply_text("Ora invia il link dell'immagine del prodotto.")
    return IMAGE

# Gestione dell'immagine
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["image"] = update.message.text
    await update.message.reply_text("Perfetto! Ora invia la descrizione del prodotto.")
    return DESCRIPTION

# Gestione della descrizione e invio al canale
async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["description"] = update.message.text

    link = context.user_data["link"]
    image = context.user_data["image"]
    description = context.user_data["description"]

    # Invio del messaggio al canale
    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=image,
        caption=f"📦 <b>Offerta Amazon</b>\n\n{description}\n\n🔗 <a href='{link}'>Acquista ora</a>",
        parse_mode="HTML",
    )
    await update.message.reply_text("Il messaggio è stato inviato al canale!")
    return ConversationHandler.END

# Funzione /annulla
async def annulla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operazione annullata.")
    return ConversationHandler.END

# Gestione di input non validi
async def invalid_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Input non valido. Usa /help per vedere i comandi disponibili.")

# Funzione principale
def main():
    application = Application.builder().token(TOKEN_BOT).build()

    # Configurazione della conversazione
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("manda", manda)],
        states={
            LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link)],
            IMAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_image)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description)],
        },
        fallbacks=[CommandHandler("annulla", annulla)],
    )

    # Aggiunta dei comandi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("annulla", annulla))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input))

    # Avvio del bot
    application.run_polling()

if __name__ == "__main__":
    main()
