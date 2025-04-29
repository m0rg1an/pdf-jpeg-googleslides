import fitz  # PyMuPDF
import sys

def scale_up_and_center_content(input_path, output_path, scale_factor=1.6):
    # US Letter size in points
    letter_width, letter_height = 612, 792

    src_doc = fitz.open(input_path)
    dst_doc = fitz.open()

    for page in src_doc:
        rect = page.rect

        # Apply the scale factor directly to the content
        scale_x = scale_factor
        scale_y = scale_factor

        # Calculate the new content size after scaling
        new_width = rect.width * scale_x
        new_height = rect.height * scale_y

        # Create new US Letter page
        dst_page = dst_doc.new_page(width=letter_width, height=letter_height)

        # Center the scaled content on the new page
        tx = (letter_width - new_width) / 2
        ty = (letter_height - new_height) / 2

        # Show original page on new canvas with scaling and translation
        dst_page.show_pdf_page(
            fitz.Rect(tx, ty, tx + new_width, ty + new_height),
            src_doc,
            page.number
        )

    dst_doc.save(output_path)
    print(f"Saved scaled-up vector PDF to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 scale_up_and_center_content.py input.pdf output.pdf")
    else:
        scale_up_and_center_content(sys.argv[1], sys.argv[2])
