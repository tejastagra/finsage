# finsage/parser.py

import pandas as pd
import re

def load_excel_file(filepath):
    """Load Excel file and return dataframe, automatically handles common header junk."""
    df = pd.read_excel(filepath, engine="openpyxl", header=None)
    return df

def parse_profit_and_loss(df):
    """Parses a Profit & Loss statement and returns structured data."""
    # Drop header rows dynamically by finding the first row with numeric values
    for i, row in df.iterrows():
        if any(isinstance(x, (int, float)) or (isinstance(x, str) and x.strip().startswith('$')) for x in row):
            df = df.iloc[i:].reset_index(drop=True)
            break

    # Adjust headers based on number of columns
    if len(df.columns) >= 4:
        df.columns = ['Item', 'Blank', '2024', '2023']
    elif len(df.columns) == 3:
        df.columns = ['Item', '2024', '2023']
    else:
        raise ValueError("Unexpected column format in Profit & Loss statement.")

    if 'Blank' in df.columns:
        df = df[['Item', '2024']]
    else:
        df = df[['Item', '2024']]

    df.dropna(subset=['Item'], inplace=True)

    structured_data = {
        "Revenue": {},
        "Cost of Goods Sold": {},
        "Operating Expenses": {},
        "Other Income": {},
        "Net Profit": 0
    }

    current_section = None
    for _, row in df.iterrows():
        label = str(row['Item']).strip()
        val_raw = str(row['2024']).strip()

        try:
            val = float(val_raw.replace('$', '').replace(',', ''))
        except:
            val = None

        # Identify section headers
        if re.fullmatch(r'Revenue', label, re.IGNORECASE):
            current_section = "Revenue"
            continue
        elif re.fullmatch(r'Cost of Goods Sold', label, re.IGNORECASE):
            current_section = "Cost of Goods Sold"
            continue
        elif re.fullmatch(r'Operating Expenses', label, re.IGNORECASE):
            current_section = "Operating Expenses"
            continue
        elif re.fullmatch(r'Other Income', label, re.IGNORECASE):
            current_section = "Other Income"
            continue
        elif re.search(r'Net profit', label, re.IGNORECASE):
            structured_data["Net Profit"] = val if val is not None else 0
            current_section = None
            continue

        # Add value under the current section
        if current_section and val is not None:
            structured_data[current_section][label] = val

    return structured_data

def parse_cash_flow(df):
    """Parses a monthly cash flow file into structured data."""
    structured_data = {
        "Operating Activities": {},
        "Investing Activities": {},
        "Financing Activities": {},
        "Summary": {}
    }

    current_section = None
    for _, row in df.iterrows():
        label = str(row.iloc[0]).strip()

        # Detect section changes
        if "operating activities" in label.lower():
            current_section = "Operating Activities"
            continue
        elif "investing activities" in label.lower():
            current_section = "Investing Activities"
            continue
        elif "financing activities" in label.lower():
            current_section = "Financing Activities"
            continue
        elif "net increase in cash" in label.lower():
            current_section = "Summary"

        if current_section:
            values = row.iloc[1:].dropna()
            cleaned = []
            for val in values:
                try:
                    val = float(str(val).replace('$', '').replace(',', '').strip())
                    cleaned.append(val)
                except ValueError:
                    continue
            monthly_total = sum(cleaned)
            structured_data[current_section][label] = monthly_total

    return structured_data
