# FinSage: Automated Financial Report Visualiser

**FinSage** is a smart and simple Python tool that takes your messy Profit & Loss and Cash Flow Excel sheets and turns them into a polished, professional PDF report — complete with graphs and summaries.

Created by **Tejas Tagra**.

---

## What Does It Do?

FinSage:

* Extracts and analyses data from raw Excel sheets (even if not perfectly formatted)
* Supports both Profit & Loss and Cash Flow statements
* Automatically generates charts for:

  * Top Revenue Drivers
  * Top Cost Drivers
  * Major Cash Inflows
  * Major Cash Outflows
* Computes:

  * Total revenue and expenses
  * Net profit
  * Capital required to break even
  * Total inflows/outflows
  * Net cash flow
* Generates a clean, styled PDF report with graphs and bullet-point summaries
* Works with just a few lines of Python (see below)

---

## Folder Structure

```
finsage/
|
├── analyzer.py        # Calculates summaries, inflows, outflows, etc.
├── parser.py          # Reads and cleans Excel files
├── reporter.py        # Generates PDF reports
|
├── templates/
|   └── report_template.html  # Jinja2 template for the report
|
├── temp_charts/       # Temporary folder for generated chart images
├── output_report.pdf  # Final generated report
├── requirements.txt   # All required dependencies
```

---

## Installation

1. Clone this repo:

```bash
git clone https://github.com/yourusername/finsage.git
cd finsage
```

2. Install dependencies:

```bash
pip3 install -r requirements.txt
```

Note: `weasyprint` may require additional system packages for fonts and rendering.

* On macOS:

```bash
brew install cairo pango gdk-pixbuf libffi
```

* On Ubuntu:

```bash
sudo apt install libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
```

---

## How to Use

1. Place your Excel files in the root folder. For example:

   * `sample_profit_and_loss.xlsx`
   * `monthly_cash_flow_statement.xlsx`

2. Add a main Python script like this:

```python
from finsage.parser import load_excel_file, parse_profit_and_loss, parse_cash_flow
from finsage.analyzer import analyze_profit_and_loss, analyze_cash_flow
from finsage.reporter import generate_report

# Load and parse your files
pl_df = load_excel_file("sample_profit_and_loss.xlsx")
cf_df = load_excel_file("monthly_cash_flow_statement.xlsx")

pl_data = parse_profit_and_loss(pl_df)
cf_data = parse_cash_flow(cf_df)

pl_summary = analyze_profit_and_loss(pl_data)
cf_summary = analyze_cash_flow(cf_data)

# Generate PDF report
generate_report("output_report.pdf", pl_summary, cf_summary)
```

3. Run it:

```bash
pythone your_script.py
```

4. Done! Open `output_report.pdf` to view your financial report.

---

## Example Output

Your final PDF report includes:

* Bar charts for top financial metrics
* Clear, bulleted summaries
* Automatic data parsing from common Excel formats
* A formal disclaimer for use

---

## Tech Stack

* Python 3.10+
* pandas, openpyxl – Excel file handling
* matplotlib – Chart generation
* jinja2 – HTML templating
* xhtml2pdf – PDF rendering
* weasyprint (optional) – For better PDF output

---

## License & Credits

This tool was created independently by **Tejas Tagra**.

For feedback, contributions, or queries, contact: [hello@tejastagra.com](mailto:hello@tejastagra.com)
