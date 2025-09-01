/*
 Telegram ↔ OpenAI (y opcional Hugging Face)
 - Requisitos: Node 18+, TELEGRAM_BOT_TOKEN, OPENAI_API_KEY
 - Opcional: HUGGINGFACE_TOKEN para /hf

 Modo: polling (más simple que webhooks para desarrollo)
*/

import TelegramBot from 'node-telegram-bot-api';
import OpenAI from 'openai';
import { HfInference } from '@huggingface/inference';

const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
if (!BOT_TOKEN) {
  console.error('Missing TELEGRAM_BOT_TOKEN in environment');
  process.exit(1);
}

const OPENAI_API_KEY = process.env.OPENAI_API_KEY || '';
const DEFAULT_MODEL = process.env.DEFAULT_MODEL || 'gpt-4o-mini';
const HF_TOKEN = process.env.HUGGINGFACE_TOKEN || '';

const bot = new TelegramBot(BOT_TOKEN, { polling: true });
const openai = OPENAI_API_KEY ? new OpenAI({ apiKey: OPENAI_API_KEY }) : null;
const hf = HF_TOKEN ? new HfInference(HF_TOKEN) : null;

// Memoria corta por chat (en RAM) para contexto breve
const chatHistory = new Map(); // chatId -> [{role, content}]
const MAX_HISTORY_MESSAGES = 8; // user+assistant pares

function pushHistory(chatId, role, content) {
  const hist = chatHistory.get(chatId) || [];
  hist.push({ role, content });
  // mantén sólo las últimas N interacciones
  const excess = Math.max(0, hist.length - MAX_HISTORY_MESSAGES);
  if (excess > 0) hist.splice(0, excess);
  chatHistory.set(chatId, hist);
}

function buildMessages(chatId, userText) {
  const base = [
    { role: 'system', content: 'Eres un asistente útil y conciso. Si el tema es médico, responde con rigor y claridad.' }
  ];
  const hist = chatHistory.get(chatId) || [];
  return [...base, ...hist, { role: 'user', content: userText }];
}

function splitForTelegram(text, chunkSize = 3800) {
  const chunks = [];
  let remaining = text || '';
  while (remaining.length > chunkSize) {
    let idx = remaining.lastIndexOf('\n', chunkSize);
    if (idx === -1) idx = chunkSize;
    chunks.push(remaining.slice(0, idx));
    remaining = remaining.slice(idx);
  }
  if (remaining) chunks.push(remaining);
  return chunks;
}

async function replyLong(chatId, text, opts = {}) {
  const parts = splitForTelegram(text);
  for (const p of parts) {
    // eslint-disable-next-line no-await-in-loop
    await bot.sendMessage(chatId, p, { disable_web_page_preview: true, ...opts });
  }
}

async function handleOpenAI(chatId, text) {
  if (!openai) return 'OpenAI no está configurado (falta OPENAI_API_KEY).';
  const messages = buildMessages(chatId, text);
  const resp = await openai.chat.completions.create({
    model: DEFAULT_MODEL,
    messages,
    temperature: 0.7,
    max_tokens: 512
  });
  const out = resp.choices?.[0]?.message?.content?.trim() || 'Sin respuesta';
  pushHistory(chatId, 'user', text);
  pushHistory(chatId, 'assistant', out);
  return out;
}

async function handleHF(model, prompt) {
  if (!hf) return 'Hugging Face no está configurado (falta HUGGINGFACE_TOKEN).';
  const res = await hf.textGeneration({
    model,
    inputs: prompt,
    parameters: { max_new_tokens: 200, temperature: 0.7 }
  });
  // La librería devuelve string o objeto según modelo; normalizamos a texto
  if (typeof res === 'string') return res;
  if (res && typeof res.generated_text === 'string') return res.generated_text;
  return JSON.stringify(res);
}

bot.onText(/^\/start(?:@\w+)?$/, async (msg) => {
  const chatId = msg.chat.id;
  await bot.sendMessage(
    chatId,
    '¡Hola! Envíame un mensaje y responderé con OpenAI.\n' +
      'Comandos:\n' +
      '• /hf <modelo> <prompt> → usa Hugging Face\n' +
      '• /clear → limpia el contexto del chat'
  );
});

bot.onText(/^\/clear(?:@\w+)?$/, async (msg) => {
  const chatId = msg.chat.id;
  chatHistory.delete(chatId);
  await bot.sendMessage(chatId, 'Contexto limpiado.');
});

bot.onText(/^\/hf\s+([^\s]+)\s+([\s\S]+)/, async (msg, match) => {
  const chatId = msg.chat.id;
  const model = match?.[1];
  const prompt = match?.[2];
  try {
    await bot.sendChatAction(chatId, 'typing');
    const out = await handleHF(model, prompt);
    await replyLong(chatId, out);
  } catch (err) {
    console.error('HF error:', err);
    await bot.sendMessage(chatId, '❌ Error usando Hugging Face.');
  }
});

bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const text = (msg.text || '').trim();
  if (!text || text.startsWith('/')) return; // comandos ya manejados arriba
  try {
    await bot.sendChatAction(chatId, 'typing');
    const out = await handleOpenAI(chatId, text);
    await replyLong(chatId, out);
  } catch (err) {
    console.error('OpenAI error:', err);
    await bot.sendMessage(chatId, '❌ Error generando respuesta.');
  }
});

console.log('🤖 Telegram bot iniciado (polling).');

