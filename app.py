import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from retrieval import load_chunks_from_database, retrieve
from sentence_transformers import SentenceTransformer


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

MODEL_NAME = "all-MiniLM-L6-v2"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello Vaishnavi! 👋\n"
        "I am your GenAI RAG Assistant.\n\n"
        "Use /help to see what I can do."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show available commands\n"
        "/ask <question> - Ask a question using the knowledge base"
    )


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)

    if not question:
        await update.message.reply_text(
            "Please provide a question.\n\n"
            "Example:\n"
            "/ask How many vacation days do employees get?"
        )
        return

    model = context.bot_data["model"]
    chunks = context.bot_data["chunks"]

    results = retrieve(
        question,
        chunks,
        model,
        top_k=3,
    )

    best_result = results[0]

    response = (
        f"🔎 Most relevant information:\n\n"
        f"{best_result['text']}\n\n"
        f"📄 Source: {best_result['source']}\n"
        f"📊 Similarity: {best_result['score']:.4f}"
    )

    await update.message.reply_text(response)


def main():
    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Loading knowledge base from SQLite...")

    chunks = load_chunks_from_database()

    print(f"Loaded {len(chunks)} chunks.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.bot_data["model"] = model
    app.bot_data["chunks"] = chunks

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ask", ask))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()