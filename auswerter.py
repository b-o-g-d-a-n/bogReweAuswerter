import pypdf
import re
import csv
import pathlib

from categories import categories
from categories import top_categories


##################################################
#                  VARIABLES                     #
##################################################

output_file_name = "output.csv"
bon_path = "Bons"

##################################################
##################################################




bons_dir = pathlib.Path(bon_path)
output = []
for pdf_file in bons_dir.glob("*.pdf"):
    reader = pypdf.PdfReader(pdf_file)

    text = ""
    for page in reader.pages:
        text += page.extract_text()


    # Find everything between UID Nr.: XXX and SUMME
    pattern = r"UID Nr\.:.*?(?=SUMME)"
    matches = re.findall(pattern, text, re.DOTALL)

    pattern_date = r"(\d\d)\.(\d\d)\.(\d\d\d\d)"
    match_date = re.search(pattern_date, text)

    # Clean and split into lines
    rows = []
    for match in matches:
        lines = match.strip().split("\n")
        for line in lines:
            if line.strip():
                rows.append(line.strip())

    for row in rows[2:-1]:
        # Remove Stk and price / kg
        if 'x' in row:
            continue

        # Capture name and price
        match = re.match(r"^(.*?)\s+([\d,]+)\s*[A-Za-z]$", row)
        if match:
            # Add the data to the set
            date = f"{match_date.group(3)}-{match_date.group(2)}-{match_date.group(1)}"
            name = match.group(1).strip()
            price = match.group(2).replace(',','.')
            category = categories.get(name, "unknown")
            top_category = top_categories.get(category, "unknown")
            output.append([date, name, price, category, top_category])


# Write to CSV
with open(output_file_name, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "name", "price", "category", "top_category"])
    writer.writerows(output)

