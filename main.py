from grader_lib import CourseGrader

# ================= CONFIGURATION =================

# 1. Input File Name (CSV exported from Brightspace/Canvas)
# IMPORTANT: Put your csv file in this folder.
INPUT_FILE = 'YOUR_FILE_NAME_HERE.csv' 

# 2. Output File Name
OUTPUT_FILE = 'Final_Grades_Report.xlsx'

# 3. Weights (Rubric)
# Keys must match keywords in your CSV column headers.
# Values should sum to 1.0 (or close to it).
WEIGHTS = {
    'Homework': 0.28,
    'Lab': 0.06,
    'Quiz': 0.10,
    'Midterm': 0.32,
    'Final': 0.20,
    'Portfolio': 0.04
}

# 4. Global Bonus Points (Added to final score)
BONUS_POINTS = 1.0

# ===============================================

if __name__ == "__main__":
    try:
        # Initialize
        grader = CourseGrader(INPUT_FILE, WEIGHTS)
        
        # Process
        grader.process_grades(bonus_points=BONUS_POINTS)
        
        # Export
        grader.export_to_excel(OUTPUT_FILE)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Tip: Check if your input filename is correct in main.py")