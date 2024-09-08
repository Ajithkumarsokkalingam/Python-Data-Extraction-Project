import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os


csv_file = r'C:\python projects\Data Extraction and Invoice PDF Generation\All Bills.csv'
logo_path = r'C:\python projects\Data Extraction and Invoice PDF Generation\weboin.png'


if not os.path.isfile(csv_file):
    print(f"File not found: {csv_file}")
    exit(1)


try:
    data = pd.read_csv(csv_file)
    print("CSV file loaded successfully!")
except PermissionError:
    print(f"Permission denied: {csv_file}")
    exit(1)

data.columns = data.columns.str.strip()
print("Column names in the CSV file:", data.columns.tolist())

if 'INVOICE No.' not in data.columns:
    print("The 'INVOICE No.' column is missing from the CSV file.")
    exit(1)

invoices = data.groupby('INVOICE No.')

def generate_invoice(invoice_data, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Invoice")

    c.setFont("Helvetica", 12)
    y = height - 150
    for key, value in invoice_data.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 20

    if os.path.isfile(logo_path):
        c.drawImage(logo_path, 400, height - 150, width=100, height=50)

    c.save()

output_dir = r'C:\python projects\Data Extraction and Invoice PDF Generation\invoices'
os.makedirs(output_dir, exist_ok=True)

for invoice_number, invoice_data in invoices:
    invoice_dict = invoice_data.to_dict(orient='records')[0] 
    output_path = os.path.join(output_dir, f'Invoice_{invoice_number}.pdf')
    generate_invoice(invoice_dict, output_path)

print("Invoices generated successfully!")
