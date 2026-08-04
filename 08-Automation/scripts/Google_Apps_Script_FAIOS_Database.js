/**
 * FAIOS Enterprise Google Apps Script Database Engine v33.0
 * CLOUD-PERSISTENT ANTI-DUPLICATE ENGINE
 * - Dedicated "Used_Topic_IDs" tab for 100% duplicate prevention across Render restarts
 * - LOG_USED_TOPIC action: writes sub_topic_id to cloud sheet
 * - GET_PAST_TOPICS now returns actual sub_topic_ids (not captions)
 * MUST REPLACE ALL CODE IN APPS SCRIPT EDITOR!
 */

const SECRET_API_KEY = "futrix_sec_2026_x79q90m3";

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    
    if (data.secret_key !== SECRET_API_KEY) {
      return ContentService.createTextOutput(JSON.stringify({ status: "UNAUTHORIZED", message: "Invalid API Secret Key" }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    const action = data.action;
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    setupSheetHeaders(ss);

    let scheduledSheet = ss.getSheetByName("Scheduled_Posts") || ss.getSheets()[0];

    // ─────────────────────────────────────────────────────────────────────────
    // GET_PAST_TOPICS: Returns ACTUAL sub_topic_ids from Used_Topic_IDs sheet
    // (cloud-persistent, survives Render restarts)
    // ─────────────────────────────────────────────────────────────────────────
    if (action === "GET_PAST_TOPICS") {
      let usedIds = [];

      // Primary: Read from dedicated Used_Topic_IDs tab (sub_topic_id column)
      let usedSheet = ss.getSheetByName("Used_Topic_IDs");
      if (usedSheet && usedSheet.getLastRow() > 1) {
        let vals = usedSheet.getRange(2, 1, usedSheet.getLastRow() - 1, 1).getValues();
        for (let i = 0; i < vals.length; i++) {
          if (vals[i][0]) usedIds.push(String(vals[i][0]).trim().toLowerCase());
        }
      }

      // Fallback: Also read captions from Scheduled_Posts & Published_Posts
      // (for backward compatibility with old records)
      let allSheets = ss.getSheets();
      for (let s = 0; s < allSheets.length; s++) {
        let sheet = allSheets[s];
        let name = sheet.getName();
        if ((name === "Scheduled_Posts" || name === "Published_Posts") && sheet.getLastRow() > 1) {
          let vals = sheet.getRange(2, 5, sheet.getLastRow() - 1, 1).getValues();
          for (let i = 0; i < vals.length; i++) {
            if (vals[i][0]) usedIds.push(String(vals[i][0]).toLowerCase());
          }
        }
      }

      return ContentService.createTextOutput(JSON.stringify({ status: "SUCCESS", topics: usedIds }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // LOG_USED_TOPIC: Write sub_topic_id to Used_Topic_IDs tab after generation
    // Called every time content is generated - ensures 100% cloud persistence
    // ─────────────────────────────────────────────────────────────────────────
    if (action === "LOG_USED_TOPIC") {
      let sub_topic_id = data.sub_topic_id;
      let format_type = data.format_type || "unknown";
      if (!sub_topic_id) {
        return ContentService.createTextOutput(JSON.stringify({ status: "ERROR", message: "sub_topic_id required" }))
          .setMimeType(ContentService.MimeType.JSON);
      }

      let usedSheet = ss.getSheetByName("Used_Topic_IDs");
      if (!usedSheet) {
        usedSheet = ss.insertSheet("Used_Topic_IDs");
        usedSheet.getRange(1, 1, 1, 3).setValues([["Sub Topic ID", "Format Type", "Generated At"]]);
        usedSheet.getRange(1, 1, 1, 3).setFontWeight("bold").setBackground("#7C3AED").setFontColor("#FFFFFF");
      }

      // Check if already exists (avoid even logging duplicates)
      let alreadyLogged = false;
      if (usedSheet.getLastRow() > 1) {
        let existing = usedSheet.getRange(2, 1, usedSheet.getLastRow() - 1, 1).getValues();
        for (let i = 0; i < existing.length; i++) {
          if (String(existing[i][0]).trim().toLowerCase() === sub_topic_id.trim().toLowerCase()) {
            alreadyLogged = true;
            break;
          }
        }
      }

      if (!alreadyLogged) {
        let timestamp = new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });
        usedSheet.appendRow([sub_topic_id, format_type, timestamp]);
      }

      return ContentService.createTextOutput(JSON.stringify({ status: "SUCCESS", logged: !alreadyLogged, sub_topic_id: sub_topic_id }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // ADD_SCHEDULED_POST
    // ─────────────────────────────────────────────────────────────────────────
    if (action === "ADD_SCHEDULED_POST") {
      let driveUrl = "";

      if (data.media_base64) {
        try {
          var bytes = Utilities.base64Decode(data.media_base64);
          var blob = Utilities.newBlob(bytes, data.mime_type || "application/pdf", data.file_name || "futrix_carousel_deck.pdf");
          
          var folderName = "FUTRIX_Media_Assets";
          var folders = DriveApp.getFoldersByName(folderName);
          var folder = folders.hasNext() ? folders.next() : DriveApp.createFolder(folderName);
          
          var file = folder.createFile(blob);
          file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
          driveUrl = file.getUrl();
        } catch (driveErr) {
          Logger.log("Drive Upload Error: " + driveErr);
        }
      }

      if (!driveUrl && data.media_url) {
        driveUrl = data.media_url;
      }

      const clickableFormula = driveUrl.startsWith("http") ? `=HYPERLINK("${driveUrl}", "View File in Google Drive 📁")` : driveUrl;
      const createdTimeStr = new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });

      scheduledSheet.appendRow([
        data.post_id,
        createdTimeStr,
        data.platform,
        data.post_time,
        data.caption,
        data.hashtags || "#NEET2027 #JEE2027 #FutrixAI #EdTech #StudySmart",
        clickableFormula,
        data.approval_status || "APPROVED",
        false
      ]);

      return ContentService.createTextOutput(JSON.stringify({ status: "SUCCESS", post_id: data.post_id, drive_url: driveUrl }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // MARK_AS_PUBLISHED
    // ─────────────────────────────────────────────────────────────────────────
    if (action === "MARK_AS_PUBLISHED") {
      let publishedSheet = ss.getSheetByName("Published_Posts") || ss.insertSheet("Published_Posts");
      let postIdToPublish = data.post_id;
      
      let rows = scheduledSheet.getDataRange().getValues();
      let publishedTimestamp = new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });

      for (let i = 1; i < rows.length; i++) {
        if (rows[i][0] === postIdToPublish) {
          let rowData = rows[i];
          publishedSheet.appendRow([
            rowData[0], rowData[1], rowData[2], publishedTimestamp,
            rowData[4], rowData[5], rowData[6], "PUBLISHED",
            data.live_post_url || "https://instagram.com/futrix_official"
          ]);
          scheduledSheet.deleteRow(i + 1);
          return ContentService.createTextOutput(JSON.stringify({ status: "SUCCESS", message: "Post Moved to Published_Posts!" }))
            .setMimeType(ContentService.MimeType.JSON);
        }
      }
      return ContentService.createTextOutput(JSON.stringify({ status: "ERROR", message: "Post ID not found" }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    return ContentService.createTextOutput(JSON.stringify({ status: "ERROR", message: "Unknown action" }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: "ERROR", error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function setupSheetHeaders(ss) {
  // Scheduled_Posts
  let scheduledSheet = ss.getSheetByName("Scheduled_Posts") || ss.getSheets()[0];
  scheduledSheet.getRange(1, 1, 1, 9).setValues([["Post ID", "Created Date & Time", "Platform", "Scheduled Post Time", "Viral Reach Caption", "5 Viral Hashtags", "Google Drive Media Link", "Approval Status", "Published"]]);
  scheduledSheet.getRange(1, 1, 1, 9).setFontWeight("bold").setBackground("#1E293B").setFontColor("#38BDF8");

  // Published_Posts
  let publishedSheet = ss.getSheetByName("Published_Posts") || ss.insertSheet("Published_Posts");
  publishedSheet.getRange(1, 1, 1, 9).setValues([["Post ID", "Created Date & Time", "Platform", "Published Date & Time", "Viral Reach Caption", "5 Viral Hashtags", "Google Drive Media Link", "Status", "Live Post Link"]]);
  publishedSheet.getRange(1, 1, 1, 9).setFontWeight("bold").setBackground("#065F46").setFontColor("#34D399");

  // Used_Topic_IDs (NEW - Cloud Anti-Duplicate Engine)
  let usedSheet = ss.getSheetByName("Used_Topic_IDs");
  if (!usedSheet) {
    usedSheet = ss.insertSheet("Used_Topic_IDs");
    usedSheet.getRange(1, 1, 1, 3).setValues([["Sub Topic ID", "Format Type", "Generated At"]]);
    usedSheet.getRange(1, 1, 1, 3).setFontWeight("bold").setBackground("#7C3AED").setFontColor("#FFFFFF");
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({ status: "OK", message: "FAIOS Anti-Duplicate Engine v33.0 Live!" }))
    .setMimeType(ContentService.MimeType.JSON);
}
