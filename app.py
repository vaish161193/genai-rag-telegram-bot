import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from retrieval import load_chunks_from_database
from rag import answer_question


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

MODEL_NAME = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.30


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello Vaishnavi! 👋\n"
        "I am your GenAI RAG Assistant.\n\n"
        "You can:\n"
        "/help - See available commands\n"
        "/ask <question> - Ask using the knowledge base\n\n"
        "Or simply type your question directly."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show available commands\n"
        "/ask <question> - Ask a question\n\n"
        "You can also simply type a question without /ask."
    )


async def process_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    question: str,
):
    model = context.bot_data["model"]
    chunks = context.bot_data["chunks"]

    try:
        answer, results = answer_question(
            question,
            model,
            chunks,
        )

        best_result = results[0]

        if best_result["score"] < SIMILARITY_THRESHOLD:
            response = f"🤖 {answer}"
        else:
            response = (
                f"🤖 {answer}\n\n"
                f"📄 Source: {best_result['source']}"
            )

        await update.message.reply_text(response)

    except Exception as error:
        print(f"Error while answering question: {error}")

        await update.message.reply_text(
            "Sorry, I couldn't process your question right now."
        )


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)

    if not question:
        await update.message.reply_text(
            "Please provide a question.\n\n"
            "Example:\n"
            "/ask How many annual leave days do employees get?"
        )
        return

    await process_question(
        update,
        context,
        question,
    )


async def direct_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    question = update.message.text.strip()

    if not question:
        return

    await process_question(
        update,
        context,
        question,
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    print(f"Telegram error: {context.error}")


def main():
    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Loading knowledge base...")

    chunks = load_chunks_from_database()

    print(f"Loaded {len(chunks)} chunks.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.bot_data["model"] = model
    app.bot_data["chunks"] = chunks

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ask", ask))

    app.add_handler(
        MessageHandler(
            filters.TEXT & (~filters.COMMAND),
            direct_message,
        )
    )

    app.add_error_handler(error_handler)

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()