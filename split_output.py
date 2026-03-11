import fitz  # PyMuPDF
import os


def split_pdf(input_pdf, max_pages=200, output_prefix="split"):
    doc = fitz.open(input_pdf)
    total_pages = doc.page_count

    part = 1
    for start in range(0, total_pages, max_pages):
        end = min(start + max_pages, total_pages)

        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start, to_page=end - 1)

        output_file = f"{output_prefix}_part{part}.pdf"
        new_doc.save(output_file)
        new_doc.close()

        print(f"Created {output_file} (pages {start+1}-{end})")
        part += 1

    doc.close()


if __name__ == "__main__":
    split_pdf("output_pdf/merged_dex.pdf", max_pages=200, output_prefix="output")