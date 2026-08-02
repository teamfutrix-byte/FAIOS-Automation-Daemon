/**
 * FAIOS World-Class Playwright HTML-to-Image Carousel Renderer v11.0
 * Uses Chromium Headless Browser to capture 1080x1080 HTML/CSS slides (Figma/Canva/Varun Mayya Design Quality).
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const LOGO_PATH = path.join('c:', 'Users', 'L470', 'Desktop', 'Futrix', 'Logo', 'Futrix Logo.png');

async function renderPlaywrightSlide(slideNum, totalSlides, badgeText, title, subTitle, points, footerText, outputPath) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1080, height: 1080 } });

    const logoUri = `file:///${LOGO_PATH.replace(/\\/g, '/')}`;

    const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap');
  
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    background: #090D16;
    width: 1080px;
    height: 1080px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #F8FAFC;
  }
  .card {
    width: 1080px;
    height: 1080px;
    background: radial-gradient(circle at 10% 10%, #1E293B 0%, #090D16 85%);
    border: 4px solid #38BDF8;
    padding: 60px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    box-shadow: inset 0 0 120px rgba(56, 189, 248, 0.2);
  }
  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .brand-logo-group {
    display: flex;
    align-items: center;
    gap: 20px;
  }
  .logo-img {
    height: 70px;
    width: auto;
    filter: drop-shadow(0 0 14px rgba(56, 189, 248, 0.5));
  }
  .badge {
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
    border: 1.5px solid #818CF8;
    color: #A5B4FC;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 10px 24px;
    border-radius: 30px;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
  }
  .slide-counter {
    background: rgba(56, 189, 248, 0.12);
    border: 1.5px solid #38BDF8;
    color: #38BDF8;
    font-weight: 800;
    font-size: 20px;
    padding: 10px 22px;
    border-radius: 20px;
  }
  .header-block {
    margin-top: 15px;
  }
  .title {
    font-size: 46px;
    font-weight: 900;
    color: #38BDF8;
    line-height: 1.2;
    letter-spacing: -0.5px;
  }
  .subtitle {
    font-size: 28px;
    font-weight: 600;
    color: #94A3B8;
    margin-top: 10px;
  }
  .content-container {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(56, 189, 248, 0.35);
    border-radius: 24px;
    padding: 36px;
    flex-grow: 1;
    margin: 25px 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
  }
  .point-row {
    display: flex;
    align-items: center;
    gap: 20px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 18px 24px;
    border-radius: 16px;
  }
  .point-icon {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0284C7 0%, #6366F1 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 22px;
    color: #FFF;
    flex-shrink: 0;
  }
  .point-text {
    font-size: 24px;
    font-weight: 700;
    color: #F8FAFC;
    line-height: 1.4;
  }
  .footer-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 2px solid rgba(255,255,255,0.1);
    padding-top: 20px;
  }
  .tagline {
    font-size: 22px;
    font-weight: 800;
    color: #38BDF8;
    letter-spacing: 2px;
  }
  .swipe-btn {
    background: #0284C7;
    color: #FFF;
    font-weight: 800;
    font-size: 18px;
    padding: 10px 24px;
    border-radius: 12px;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
  }
</style>
</head>
<body>
<div class="card">
  <div class="top-bar">
    <div class="brand-logo-group">
      <img src="${logoUri}" class="logo-img" />
      <div class="badge">${badgeText}</div>
    </div>
    <div class="slide-counter">SLIDE ${slideNum}/${totalSlides}</div>
  </div>

  <div class="header-block">
    <div class="title">${title}</div>
    <div class="subtitle">${subTitle}</div>
  </div>

  <div class="content-container">
    ${points.map((p, idx) => `
      <div class="point-row">
        <div class="point-icon">${idx + 1}</div>
        <div class="point-text">${p}</div>
      </div>
    `).join('')}
  </div>

  <div class="footer-bar">
    <div class="tagline">FUTRIX AI • LEARN • DECIDE • GROW</div>
    <div class="swipe-btn">SWIPE NEXT ➡️</div>
  </div>
</div>
</body>
</html>`;

    await page.setContent(htmlContent);
    await page.screenshot({ path: outputPath, type: 'png' });
    await browser.close();
    console.log(`Rendered Playwright PNG: ${outputPath}`);
    return outputPath;
}

async function generateFull5PlaywrightDeck() {
    const slidesData = [
        {
            slideNum: 1,
            title: "🚀 DAY 1 STARTUP LAUNCH",
            subTitle: "Why 85% of NEET & JEE Aspirants Fail",
            points: [
                "The 12-Hour Study Trap & Rote Memorization",
                "Why traditional coaching fails ambitious students",
                "Delayed 48-hour doubt clearing kills momentum",
                "Introducing FUTRIX: Learn. Decide. Grow."
            ]
        },
        {
            slideNum: 2,
            title: "❌ THE OLD WAY VS FUTRIX WAY",
            subTitle: "No More 48-Hour Delayed Doubts",
            points: [
                "❌ Old Way: Wait 2 days for doubt resolution",
                "❌ Old Way: Memorize formulas without clarity",
                "✨ FUTRIX Way: Sub-60s Instant Doubt Clearing",
                "✨ FUTRIX Way: Step-by-Step Socratic Guidance"
            ]
        },
        {
            slideNum: 3,
            title: "🧠 MEMORY LAB FLASHCARDS",
            subTitle: "Multiply Retention 3X with SuperMemo-2",
            points: [
                "Active Recall + Spaced Repetition Algorithm",
                "Automatically pinpoints your weak concepts",
                "Daily 10-minute micro-revision sprints",
                "Retain 95% of NEET & JEE formulas for exam day"
            ]
        },
        {
            slideNum: 4,
            title: "🎯 GAMIFIED PRACTICE LEADERBOARDS",
            subTitle: "Build Daily Streaks & Rank Higher",
            points: [
                "Earn XP for every solved PYQ & cleared doubt",
                "Compete with top rankers across India",
                "Track your real-time accuracy SLA",
                "Gamified habits that guarantee exam success"
            ]
        },
        {
            slideNum: 5,
            title: "🚀 JOIN FUTRIX WEB APP TODAY",
            subTitle: "Start Your Free Trial Now!",
            points: [
                "✨ Access Socratic AI Tutor 24/7",
                "✨ Unlock Memory Lab Flashcards",
                "✨ Solve 10,000+ Verified PYQs",
                "🎯 Visit FUTRIX App Now: https://futrix.app"
            ]
        }
    ];

    const paths = [];
    for (const d of slidesData) {
        const out = path.join(__dirname, `futrix_playwright_slide_${d.slideNum}.png`);
        await renderPlaywrightSlide(d.slideNum, 5, "FUTRIX STARTUP LAUNCH", d.title, d.subTitle, d.points, "FUTRIX AI", out);
        paths.push(out);
    }
    return paths;
}

module.exports = { renderPlaywrightSlide, generateFull5PlaywrightDeck };
