/**
 * Entry point function
 */
function main() {
  mainAsync();
}

/**
 * Main async logic to convert PDF → PNG → Google Slides
 */
function mainAsync() {
  const fileId = 'Your_pdf_file_id';     // ← Insert your PDF file ID
  const folderId = 'Your_folder_id';     // ← Insert your output folder ID

  const blob = DriveApp.getFileById(fileId).getBlob();
  convertPDFToPNG_(blob, folderId);
}

/**
 * Converts PDF into PNG thumbnails and creates a Google Slides presentation
 */
function convertPDFToPNG_(blob, folderId) {
  const cdnjs = "https://cdn.jsdelivr.net/npm/pdf-lib/dist/pdf-lib.min.js";
  eval(UrlFetchApp.fetch(cdnjs).getContentText());

  const setTimeout = (f, t) => { Utilities.sleep(t); return f(); };

  const data = new Uint8Array(blob.getBytes());
  PDFLib.PDFDocument.load(data).then(async (doc) => {
    const pageCount = doc.getPageCount();
    const imageBlobs = [];
    const tempFileIds = [];

    for (let i = 0; i < pageCount; i++) {
      const tempDoc = await PDFLib.PDFDocument.create();
      const [page] = await tempDoc.copyPages(doc, [i]);
      tempDoc.addPage(page);

      const bytes = await tempDoc.save();
      const partBlob = Utilities.newBlob([...new Int8Array(bytes)], MimeType.PDF, `page_${i + 1}.pdf`);
      const file = DriveApp.createFile(partBlob);
      tempFileIds.push(file.getId());

      Utilities.sleep(3000); // Needed for thumbnail to generate

      const thumbnail = Drive.Files.get(file.getId(), { fields: 'thumbnailLink' }).thumbnailLink;
      if (!thumbnail) throw new Error("Failed to get thumbnail. Try increasing sleep time.");

      const image = UrlFetchApp.fetch(thumbnail.replace(/=s\d+/, "=s1600")).getBlob().setName(`page_${i + 1}.png`);
      imageBlobs.push(image);
    }

    const folder = DriveApp.getFolderById(folderId || 'root');
    const imageIds = [];

    imageBlobs.forEach((img) => {
      const file = folder.createFile(img);
      imageIds.push(file.getId());
    });

    // Create Google Slides presentation
    const presentation = SlidesApp.create("PDF to Slides");
    const slideWidth = presentation.getPageWidth();
    const slideHeight = presentation.getPageHeight();

    imageIds.forEach(id => {
      const blob = DriveApp.getFileById(id).getBlob();
      const slide = presentation.appendSlide(SlidesApp.PredefinedLayout.BLANK);
      const image = slide.insertImage(blob);

      const imgWidth = image.getWidth();
      const imgHeight = image.getHeight();
      const scale = Math.min(slideWidth / imgWidth, slideHeight / imgHeight);

      image.setWidth(imgWidth * scale);
      image.setHeight(imgHeight * scale);
      image.setLeft((slideWidth - image.getWidth()) / 2);
      image.setTop((slideHeight - image.getHeight()) / 2);
    });

    // Remove default empty slide
    presentation.getSlides()[0].remove();

    Logger.log("Done! Your presentation: " + presentation.getUrl());

    // Delete temporary PDF thumbnails
    tempFileIds.forEach(id => DriveApp.getFileById(id).setTrashed(true));
  });
}
