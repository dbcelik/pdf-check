from pypdf import PdfReader
from deepdiff import DeepDiff

def extract_annotations(pdf_file):
    reader = PdfReader(pdf_file)
    annotations = []

    for page_num, page in enumerate(reader.pages):
        if "/Annots" in page:
            for annot in page["/Annots"]:
                obj = annot.get_object()
                annotations.append({
                    "page": page_num + 1,
                    "content": obj.get("/Contents"),
                    "author": obj.get("/T"),
                    "type": obj.get("/Subtype")
                })
    return annotations


def compare_pdfs(pdf_old, pdf_new):
    annots_old = extract_annotations(pdf_old)
    annots_new = extract_annotations(pdf_new)

    diff = DeepDiff(annots_old, annots_new, ignore_order=True)

    if not diff:
        return "SAME"

    output = []
    output.append("DIFFERENCES FOUND:\n")

    for change_type, changes in diff.items():

        # Değiştirilen yorumlar
        if change_type == "values_changed":
            for path, change in changes.items():
                if "content" in path:
                    idx = int(path.split("[")[1].split("]")[0])
                    page = annots_old[idx]["page"]
                    output.append(
                        f"PAGE {page} - COMMENT CHANGED\n"
                        f"  OLD: {change['old_value']}\n"
                        f"  NEW: {change['new_value']}\n"
                    )

        # Eklenen yorumlar
        elif change_type == "iterable_item_added":
            for item in changes.values():
                output.append(
                    f"PAGE {item['page']} - COMMENT ADDED\n"
                    f"  {item['content']}\n"
                )

        # Silinen yorumlar
        elif change_type == "iterable_item_removed":
            for item in changes.values():
                output.append(
                    f"PAGE {item['page']} - COMMENT REMOVED\n"
                    f"  {item['content']}\n"
                )

    return "\n".join(output)
