/**
 * FAIOS Native Telegram Approval Gate (Zero-n8n Required)
 * Runs natively on Node.js / Antigravity
 */

const HTTPS = require('https');

// Read Environment Variables
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '8850369070:AAHe3J6Nz4Ci9OJy1qyMFcryMvCYeUzXYCs';
const FOUNDER_CHAT_ID = process.env.FOUNDER_TELEGRAM_CHAT_ID || '8519187268';

/**
 * Dispatch Proposal to Founder Telegram with Inline Buttons (HTML Format)
 */
async function sendProposalToTelegram(proposal) {
    if (!TELEGRAM_BOT_TOKEN || !FOUNDER_CHAT_ID) {
        console.error("❌ TELEGRAM_BOT_TOKEN or FOUNDER_TELEGRAM_CHAT_ID not set!");
        return;
    }

    const messageText = `<b>FAIOS EXECUTIVE PROPOSAL APPROVAL REQUEST</b>\n\n` +
        `<b>Proposal ID:</b> ${proposal.proposal_id}\n` +
        `<b>Executive:</b> ${proposal.executive}\n` +
        `<b>Category:</b> ${proposal.category}\n` +
        `<b>Title:</b> ${proposal.title}\n\n` +
        `<b>Impact Summary:</b> ${proposal.impact_summary}\n` +
        `<b>Risk:</b> ${proposal.risk_assessment}\n` +
        `<b>Confidence:</b> ${proposal.confidence || '0.98/1.00'}\n\n` +
        `Tap below to approve or reject:`;

    const inlineKeyboard = {
        inline_keyboard: [
            [
                { text: '✅ APPROVE', callback_data: `APPROVE:${proposal.proposal_id}` },
                { text: '❌ REJECT', callback_data: `REJECT:${proposal.proposal_id}` }
            ]
        ]
    };

    const postData = JSON.stringify({
        chat_id: FOUNDER_CHAT_ID,
        text: messageText,
        parse_mode: 'HTML',
        reply_markup: inlineKeyboard
    });

    const options = {
        hostname: 'api.telegram.org',
        path: `/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
        }
    };

    const req = HTTPS.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => console.log('Telegram Dispatch Success:', body));
    });

    req.write(postData);
    req.end();
}

module.exports = { sendProposalToTelegram };
