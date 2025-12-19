from grader_lib import CourseGrader

# ================= CONFIGURATION =================

# 1. Input File Name (CSV exported from Brightspace/Canvas)
# IMPORTANT: Put your csv file in this folder.
INPUT_FILE = 'You file name.csv' 

# 2. Output File Name
OUTPUT_FILE = 'Final_Grades_Report.xlsx'

# 3. Weights (Rubric)
# Keys must match keywords in your CSV column headers.
# Values should sum to 1.0 (or close to it).
WEIGHTS = {
    'Homework': 0.20,
    'Lab': 0.06,
    'Quiz': 0.13,
    'Midterm': 0.30,
    'Final': 0.30,
    'Portfolio': 0.01
}

# 4. Global Bonus Points (Added to final score)
BONUS_POINTS = 0.5

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
