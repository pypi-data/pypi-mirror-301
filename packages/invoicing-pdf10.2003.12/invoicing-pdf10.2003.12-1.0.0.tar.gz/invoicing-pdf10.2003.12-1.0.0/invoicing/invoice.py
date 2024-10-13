import pandas as pd
import glob
from fpdf import FPDF
import pathlib
import os


def generate(invoices_path, pdfs_path, image_path, 
             product_id, product_name, amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice excel files into PDF invoices
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")
    for filepath in filepaths:
        filepath = pathlib.Path(filepath)

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = filepath.stem
        invoice_nr, date = filename.split("-")

        pdf.set_font(family="Times", style="B", size=18)
        pdf.cell(w=0, h=8, txt=f"Invoice.nr.{invoice_nr}", align="L", ln=1)
        pdf.cell(w=0, h=8, txt=f"Date: {date}", align="L", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # Add table headers
        columns = df.columns
        columns = [item.replace('_', ' ').title() for item in columns]
        pdf.set_font(family="Times", style="B", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=65, h=8, txt=columns[1], border=1)
        pdf.cell(w=35, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        # Add rows to the table
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=f"{row[product_id]}", border=1)
            pdf.cell(w=65, h=8, txt=f"{row[product_name]}", border=1)
            pdf.cell(w=35, h=8, txt=f"{row[amount_purchased]}", border=1)
            pdf.cell(w=30, h=8, txt=f"{row[price_per_unit]}", border=1)
            pdf.cell(w=30, h=8, txt=f"{row[total_price]}", border=1, ln=1)

        # Add total amount row
        total_amt = df[total_price].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=65, h=8, txt="", border=1)
        pdf.cell(w=35, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="Total Amount:", border=1)
        pdf.cell(w=30, h=8, txt=str(total_amt), border=1, ln=1)

        # Add total amount sentence
        pdf.set_font(family="Times", size=16)
        pdf.cell(w=30, h=15, txt=f"The total amount is: {total_amt}", ln=1)

        # Add company name and logo
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=55, h=15, txt="MSK ENTERPRISES")
        pdf.image(image_path, w=20)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)

        pdf.output(f"{pdfs_path}/{filename}.pdf")


