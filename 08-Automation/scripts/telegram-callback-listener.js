/**
 * FAIOS Telegram Callback Query Listener & Google Sheets Sync (Secured & Verified)
 */

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '8850369070:AAHe3J6Nz4Ci9OJy1qyMFcryMvCYeUzXYCs';
const GOOGLE_APPS_SCRIPT_WEBAPP_URL = process.env.GOOGLE_APPS_SCRIPT_WEBAPP_URL || 'https://script.google.com/macros/s/AKfycbxXOpIAijWjS-4a3Ft292jntUwTuKPkHgzzufBaC5AJGQO8xILS14mIONklMq54ox1a/exec';
const SECRET_API_KEY = 'futrix_sec_2026_x79q90m3';

let lastUpdateId = 0;

/**
 * Answer Telegram Callback Query
 */
async function answerCallbackQuery(callbackQueryId, text) {
    try {
        await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/answerCallbackQuery`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                callback_query_id: callbackQueryId,
                text: text,
                show_alert: true
            })
        });
    } catch (err) {
        console.error("Error answering callback query:", err);
    }
}

/**
 * Update Proposal Status in Google Sheets (Follows 302 redirects)
 */
async function updateGoogleSheets(proposalId, status) {
    console.log(`[Google Sheets] Syncing Proposal ${proposalId} -> ${status}...`);
    const payload = {
        secret_key: SECRET_API_KEY,
        action: 'ADD_PROPOSAL',
        proposal_id: proposalId,
        executive: 'AI-CEO',
        category: 'CONTENT_RELEASE',
        title: 'Release NEET UG Physics High-Yield Mock Series 01',
        impact_summary: 'Publishes 180 verified Qs for 12,000 NEET aspirants.',
        risk_assessment: 'LOW',
        status: status
    };

    try {
        const response = await fetch(GOOGLE_APPS_SCRIPT_WEBAPP_URL, {
            method: 'POST',
            redirect: 'follow',
            headers: { 'Content-Type': 'text/plain;charset=utf-8' },
            body: JSON.stringify(payload)
        });

        const resultText = await response.text();
        console.log(`[Google Sheets Live Response]:`, resultText);
    } catch (err) {
        console.error(`[Google Sheets Sync Failed]:`, err);
    }
}

/**
 * Poll Telegram Updates for Button Clicks
 */
async function pollTelegramUpdates() {
    try {
        const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates?offset=${lastUpdateId + 1}&timeout=30`;
        const res = await fetch(url);
        const response = await res.json();

        if (response.ok && response.result.length > 0) {
            for (const update of response.result) {
                lastUpdateId = update.update_id;

                if (update.callback_query) {
                    const callback = update.callback_query;
                    const actionData = callback.data;
                    const [action, proposalId] = actionData.split(':');

                    console.log(`[FOUNDER ACTION DETECTED] Button: ${action} for Proposal: ${proposalId}`);

                    if (action === 'APPROVE') {
                        await answerCallbackQuery(callback.id, '✅ PROPOSAL APPROVED! Syncing to Google Sheets...');
                        await updateGoogleSheets(proposalId, 'APPROVED');
                    } else if (action === 'REJECT') {
                        await answerCallbackQuery(callback.id, '❌ PROPOSAL REJECTED! Syncing to Google Sheets...');
                        await updateGoogleSheets(proposalId, 'REJECTED');
                    }
                }
            }
        }
    } catch (err) {
        console.error("Poll error:", err.message);
    }

    setTimeout(pollTelegramUpdates, 1000);
}

console.log("🚀 FAIOS Telegram Callback Button Listener Engine Started (Secured Sync)...");
pollTelegramUpdates();
