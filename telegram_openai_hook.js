const TelegramBot = require('node-telegram-bot-api');
const { OpenAI } = require('openai');

// Reemplaza con tus claves reales
const TELEGRAM_TOKEN = 'TU_TELEGRAM_BOT_TOKEN';
const OPENAI_API_KEY = 'TU_OPENAI_API_KEY';

const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });
const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const userText = msg.text;

  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: userText }],
    });

    const aiReply = completion.choices[0].message.content;
    bot.sendMessage(chatId, aiReply);
  } catch (error) {
    bot.sendMessage(chatId, 'Error al conectar con OpenAI.');
  }
});