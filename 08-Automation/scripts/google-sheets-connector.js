/**
 * FAIOS Native Google Sheets Connector (Node.js fetch with 302 redirect support)
 */

const GOOGLE_APPS_SCRIPT_WEBAPP_URL = process.env.GOOGLE_APPS_SCRIPT_WEBAPP_URL || 'https://script.google.com/macros/s/AKfycbxGn2rYhuxaMy2k9DH1hHQ26TLvZusL5aZiaLztD_3-eKtiDjEijvngm2Uvgm1oer1Qhw/exec';

/**
 * Save Data Record to Google Sheets via Apps Script Web App (follows 302 redirects)
 */
async function saveToGoogleSheets(payload) {
    try {
        const response = await fetch(GOOGLE_APPS_SCRIPT_WEBAPP_URL, {
            method: 'POST',
            redirect: 'follow',
            headers: {
                'Content-Type': 'text/plain;charset=utf-8' // Google Apps Script requirement for simple CORS POST
            },
            body: JSON.stringify(payload)
        });

        const text = await response.text();
        console.log('[Google Sheets Response]:', text);
        try {
            return JSON.parse(text);
        } catch (e) {
            return { status: "SUCCESS", raw: text };
        }
    } catch (err) {
        console.error('[Google Sheets Error]:', err);
        return { status: "ERROR", error: err.message };
    }
}

module.exports = { saveToGoogleSheets };
