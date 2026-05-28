import openpyxl

wb = openpyxl.load_workbook("/Users/uchun1ee/.gemini/antigravity/scratch/teaworld2026/booth_layout.xlsx")
sheet = wb.active

print("Merged cell ranges:")
for merged_range in sheet.merged_cells.ranges:
    print(f"Range: {merged_range} | Width: {merged_range.bounds[2] - merged_range.bounds[0] + 1} | Height: {merged_range.bounds[3] - merged_range.bounds[1] + 1}")
