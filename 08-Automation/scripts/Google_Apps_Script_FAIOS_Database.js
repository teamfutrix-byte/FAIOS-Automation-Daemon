/**
 * FAIOS Enterprise Google Apps Script Database Engine v32.0 (Multi-Tab Topic Verification Standard)
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

    // Setup 9-Column Headers on Sheets
    setupSheetHeaders(ss);

    let scheduledSheet = ss.getSheetByName("Scheduled_Posts") || ss.getSheets()[0];

    // GET_PAST_TOPICS: Scans ALL tabs (Scheduled_Posts, Published_Posts, System_Approvals) for 100% Anti-Duplicate Protection!
    if (action === "GET_PAST_TOPICS") {
      let topics = [];
      let allSheets = ss.getSheets();
      for (let s = 0; s < allSheets.length; s++) {
        let sheet = allSheets[s];
        if (sheet.getLastRow() > 1) {
          let values = sheet.getRange(2, 5, sheet.getLastRow() - 1, 1).getValues();
          for (let i = 0; i < values.length; i++) {
            if (values[i][0]) topics.push(values[i][0]);
          }
        }
      }
      return ContentService.createTextOutput(JSON.stringify({ status: "SUCCESS", topics: topics }))
        .setMimeType(ContentService.MimeType.JSON);
    }

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

      // EXACT 9 ELEMENTS IN APPEND ROW!
      scheduledSheet.appendRow([
        data.post_id,                                                      // 1. Post ID
        createdTimeStr,                                                   // 2. Created Date & Time
        data.platform,                                                    // 3. Platform
        data.post_time,                                                   // 4. Scheduled Post Time
        data.caption,                                                     // 5. Viral Reach Caption
        data.hashtags || "#NEET2026 #JEE2026 #FutrixAI #EdTech #StudySmart", // 6. 5 Viral Hashtags
        clickableFormula,                                                 // 7. Google Drive Media Link
        data.approval_status || "APPROVED",                               // 8. Approval Status
        false                                                             // 9. Published
      ]);

      return ContentService.createTextOutput(JSON.stringify({ status: "SUCCESS", post_id: data.post_id, drive_url: driveUrl }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    if (action === "MARK_AS_PUBLISHED") {
      let publishedSheet = ss.getSheetByName("Published_Posts") || ss.insertSheet("Published_Posts");
      let postIdToPublish = data.post_id;
      
      let rows = scheduledSheet.getDataRange().getValues();
      let publishedTimestamp = new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });

      for (let i = 1; i < rows.length; i++) {
        if (rows[i][0] === postIdToPublish) {
          let rowData = rows[i];
          
          publishedSheet.appendRow([
            rowData[0], // Post ID
            rowData[1], // Created Date & Time
            rowData[2], // Platform
            publishedTimestamp, // Actual Published Date & Time
            rowData[4], // Viral Reach Caption
            rowData[5], // 5 Viral Hashtags
            rowData[6], // Google Drive Media Link
            "PUBLISHED", // Status
            data.live_post_url || "https://instagram.com/futrix" // Live Post Link
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
  let scheduledSheet = ss.getSheetByName("Scheduled_Posts") || ss.getSheets()[0];
  let publishedSheet = ss.getSheetByName("Published_Posts") || ss.insertSheet("Published_Posts");

  var scheduledHeaders = [
    "Post ID", "Created Date & Time", "Platform", "Scheduled Post Time", 
    "Viral Reach Caption", "5 Viral Hashtags", "Google Drive Media Link", "Approval Status", "Published"
  ];
  scheduledSheet.getRange(1, 1, 1, 9).setValues([scheduledHeaders]);
  scheduledSheet.getRange(1, 1, 1, 9).setFontWeight("bold").setBackground("#1E293B").setFontColor("#38BDF8");

  var publishedHeaders = [
    "Post ID", "Created Date & Time", "Platform", "Published Date & Time", 
    "Viral Reach Caption", "5 Viral Hashtags", "Google Drive Media Link", "Status", "Live Post Link"
  ];
  publishedSheet.getRange(1, 1, 1, 9).setValues([publishedHeaders]);
  publishedSheet.getRange(1, 1, 1, 9).setFontWeight("bold").setBackground("#065F46").setFontColor("#34D399");
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({ status: "OK", message: "FAIOS 9-Element Array Engine v32.0 Live!" }))
    .setMimeType(ContentService.MimeType.JSON);
}
