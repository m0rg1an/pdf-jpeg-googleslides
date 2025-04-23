PDF to Slides Tool – How to Use

This tool lets you convert a PDF into a Google Slides presentation.
Each PDF page is turned into a PNG image and inserted into a separate slide.

-----------------------------------
Files included:
- pdf-to-slides.gs → Google Apps Script file
  (Rename to .js if needed, but .gs is recommended)

-----------------------------------
Setup Instructions:

1. Go to https://script.google.com/ and click "+ New project"

2. Paste the content from `pdf-to-slides.gs` into the editor

3. Save the project (e.g. name it "PDF to Slides")

4. Enable Drive API:
   - In the left menu, click "+" next to "Services"
   - Find "Drive API" and click "Add"

5. In Google Drive:
   - Upload a PDF file
   - Copy its File ID from the URL (example: .../d/<ID>/view)
   - Create a folder for converted PNG images
   - Copy its Folder ID from the URL

6. In the code:
   - Replace `fileId = '...'` with your PDF File ID
   - Replace `folderId = '...'` with your Folder ID

7. Click ▶️ Run → select `main()` and allow permissions

8. Wait 10–60 seconds ⏳

9. Open the Logs tab to get a link to your generated Google Slides presentation

-----------------------------------
Notes:
- You may rename the script file extension from `.js` to `.gs` for better compatibility.
- If you see any errors like “no function found” — make sure you selected `main` in the Run dropdown.
- You can run the script again for different PDFs by changing the File ID and Folder ID.

✔️ That's it!
