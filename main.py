from finsage.parser import load_excel_file, parse_profit_and_loss, parse_cash_flow
from finsage.analyzer import analyze_profit_and_loss, analyze_cash_flow
from finsage.reporter import generate_report

# Load Excel files
pl_df = load_excel_file("samples/sample_profit_and_loss.xlsx")
cf_df = load_excel_file("samples/monthly_cash_flow_statement.xlsx")

# Parse
pl_data = parse_profit_and_loss(pl_df)
cf_data = parse_cash_flow(cf_df)

# Analyze
pl_summary = analyze_profit_and_loss(pl_data)
cf_summary = analyze_cash_flow(cf_data)

# To output summary (Used for debugging)
# print("Profit & Loss Summary:")
# print(pl_summary)
# print("\nCash Flow Summary:")
# print(cf_summary)


# Generate PDF
generate_report("output_report.pdf", pl_summary, cf_summary)
print("✅ Report generated as output_report.pdf")
