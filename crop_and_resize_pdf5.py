import fitz  # PyMuPDF
import sys

def crop_and_resize_pdf(input_pdf_path, output_pdf_path):
    # Standard US Letter size in points
    LETTER_WIDTH = 612  # 8.5 inches * 72
    LETTER_HEIGHT = 792  # 11 inches * 72

    doc = fitz.open(input_pdf_path)
    new_doc = fitz.open()

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        rect = page.rect

        # Define the area to crop: maintain the aspect ratio
        aspect_ratio_letter = LETTER_WIDTH / LETTER_HEIGHT
        target_width = rect.height * aspect_ratio_letter

        if rect.width > target_width:
            # Crop equally from left and right
            extra_width = rect.width - target_width
            left = rect.x0 + extra_width / 2
            right = rect.x1 - extra_width / 2
            clip = fitz.Rect(left, rect.y0, right, rect.y1)
        else:
            clip = rect  # No cropping needed

        # Render the cropped area to a pixmap (image)
        zoom_x = 2  # 2x = ~144 DPI (good quality)
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y)

        pix = page.get_pixmap(matrix=mat, clip=clip)

        # Create a new blank Letter page
        new_page = new_doc.new_page(width=LETTER_WIDTH, height=LETTER_HEIGHT)

        # Calculate the scaling factor to fit the image into the Letter page
        image_rect = fitz.Rect(0, 0, pix.width, pix.height)

        scale_x = LETTER_WIDTH / image_rect.width
        scale_y = LETTER_HEIGHT / image_rect.height
        scale = min(scale_x, scale_y)

        # Center the image on the page
        img_width = pix.width * scale
        img_height = pix.height * scale
        img_x0 = (LETTER_WIDTH - img_width) / 2
        img_y0 = (LETTER_HEIGHT - img_height) / 2
        img_x1 = img_x0 + img_width
        img_y1 = img_y0 + img_height

        img_rect = fitz.Rect(img_x0, img_y0, img_x1, img_y1)

        # Insert the image
        new_page.insert_image(img_rect, pixmap=pix)

        print(f"Processed page {page_number + 1}")

    # Save the new document
    new_doc.save(output_pdf_path)
    print(f"Saved resized PDF to {output_pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python crop_and_resize_pdf.py input.pdf output.pdf")
    else:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]
        crop_and_resize_pdf(input_pdf, output_pdf)

