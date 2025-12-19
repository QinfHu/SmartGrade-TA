import pandas as pd
import numpy as np
import re
import xlsxwriter
import os

class CourseGrader:
    def __init__(self, file_path, weights, cutoffs=None):
        """
        Initialize the grader.
        :param file_path: Path to the CSV file exported from LMS (Brightspace/Canvas).
        :param weights: Dictionary of weights, e.g., {'Homework': 0.3, 'Final': 0.4}.
        :param cutoffs: List of tuples for grading scale.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        self.file_path = file_path
        self.weights = weights
        self.df = pd.read_csv(file_path)
        self.result_df = None
        
        # Default Grading Scale (Standard)
        self.cutoffs = cutoffs if cutoffs else [
            (93, 'A'), (90, 'A-'), (87, 'B+'), (83, 'B'), (80, 'B-'),
            (77, 'C+'), (73, 'C'), (70, 'C-'), (67, 'D+'), (60, 'D'), (0, 'F')
        ]

    def _get_letter_grade(self, score):
        for cutoff, letter in self.cutoffs:
            if score >= cutoff:
                return letter
        return 'F'

    def _smart_extract_score(self, keyword):
        """
        Fuzzy match columns based on keywords (Brightspace/Canvas format compatible).
        """
        target_col = None
        max_points = 100.0
        
        # Strategy 1: Look for Category columns (common in Brightspace)
        for col in self.df.columns:
            if keyword.lower() in col.lower() and 'Subtotal Numerator' in col:
                target_col = col
                denom_col = target_col.replace('Numerator', 'Denominator')
                if denom_col in self.df.columns:
                    return ((self.df[target_col] / self.df[denom_col].replace(0, np.nan)) * 100).fillna(0)
        
        # Strategy 2: Look for Item columns
        if not target_col:
            for col in self.df.columns:
                if keyword.lower() in col.lower() and 'Points Grade' in col and 'Weighted' not in col:
                    target_col = col
                    match = re.search(r'MaxPoints:([\d\.]+)', col)
                    if match: max_points = float(match.group(1))
                    return ((self.df[target_col] / max_points) * 100).fillna(0)
        
        print(f"⚠️  Warning: Could not find column for '{keyword}'. Defaulting to 0.")
        return pd.Series([0] * len(self.df))

    def process_grades(self, bonus_points=0):
        """
        Calculate weighted totals and apply bonus.
        """
        print("Processing grades...")
        
        # Prepare basic info
        cols_to_keep = ['Last Name', 'First Name', 'OrgDefinedId']
        # Check if OrgDefinedId exists, otherwise try to find ID
        if 'OrgDefinedId' not in self.df.columns:
            possible_ids = [c for c in self.df.columns if 'ID' in c]
            if possible_ids:
                cols_to_keep = ['Last Name', 'First Name', possible_ids[0]]
        
        self.result_df = self.df[cols_to_keep].copy()
        # Rename ID column to standard 'ID'
        self.result_df.columns = ['Last Name', 'First Name', 'ID']
        self.result_df['ID'] = self.result_df['ID'].astype(str).str.replace('#', '')

        # Calculate Scores
        self.result_df['Weighted Total (Raw)'] = 0
        
        for category, weight in self.weights.items():
            col_name = f"{category} ({int(weight*100)}%)"
            scores = self._smart_extract_score(category)
            self.result_df[col_name] = scores.round(2)
            self.result_df['Weighted Total (Raw)'] += self.result_df[col_name] * weight

        # Apply Bonus
        self.result_df['Final Score'] = self.result_df['Weighted Total (Raw)'] + bonus_points
        self.result_df['Proposed Grade'] = self.result_df['Final Score'].apply(self._get_letter_grade)
        
        # Generate Remarks
        self.result_df['Remarks'] = self.result_df.apply(lambda row: self._generate_remarks(row), axis=1)
        
        # Rounding for display
        cols_to_round = [c for c in self.result_df.columns if '%' in c] + ['Weighted Total (Raw)', 'Final Score']
        self.result_df[cols_to_round] = self.result_df[cols_to_round].round(2)
        
        self.result_df.sort_values(by=['Last Name', 'First Name'], inplace=True)
        return self.result_df

    def _generate_remarks(self, row):
        notes = []
        # Check for missing items (0 score)
        for cat in self.weights.keys():
            col = f"{cat} ({int(self.weights[cat]*100)}%)"
            if row[col] == 0:
                notes.append(f"Missing {cat}")
        
        # Check for borderline cases (within 0.5 points)
        score = row['Final Score']
        for cut, letter in self.cutoffs:
            if cut > score and (cut - score) <= 0.5:
                notes.append(f"Borderline {letter} (-{cut-score:.2f})")
                break
        return "; ".join(notes)

    def export_to_excel(self, output_filename):
        """
        Export to a scientific-style Excel report.
        """
        if self.result_df is None:
            raise ValueError("Data not processed. Call process_grades() first.")
            
        writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
        workbook = writer.book

        # Styles (Scientific / Minimalist)
        fmt_header = workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10, 'border': 1, 'bottom': 2, 'bg_color': '#F2F2F2', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        fmt_body = workbook.add_format({'font_name': 'Arial', 'font_size': 10, 'align': 'center', 'valign': 'vcenter'})
        fmt_name = workbook.add_format({'font_name': 'Arial', 'font_size': 10, 'align': 'left', 'valign': 'vcenter'})
        
        # Highlight Styles
        fmt_raw = workbook.add_format({'font_name': 'Arial', 'font_size': 10, 'font_color': '#7F7F7F', 'align': 'center', 'valign': 'vcenter', 'right': 1, 'right_color': '#D9D9D9'})
        fmt_bonus = workbook.add_format({'font_name': 'Arial', 'font_size': 10, 'bold': True, 'bg_color': '#EBF1DE', 'align': 'center', 'valign': 'vcenter'})
        fmt_alert = workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'font_color': '#9C0006', 'align': 'left', 'valign': 'vcenter'})

        # --- Sheet 1: Gradebook ---
        self.result_df.to_excel(writer, sheet_name='Gradebook', index=False)
        ws = writer.sheets['Gradebook']
        
        # Column Widths
        ws.set_column('A:B', 15, fmt_name)  # Name
        ws.set_column('C:C', 12, fmt_body)  # ID
        
        # Dynamic Columns Formatting
        raw_idx = self.result_df.columns.get_loc('Weighted Total (Raw)')
        bonus_idx = self.result_df.columns.get_loc('Final Score')
        grade_idx = self.result_df.columns.get_loc('Proposed Grade')
        remark_idx = self.result_df.columns.get_loc('Remarks')

        # Set widths for score columns
        ws.set_column(3, raw_idx-1, 10, fmt_body) 
        ws.set_column(raw_idx, raw_idx, 12, fmt_raw)        # Raw Score (Grey)
        ws.set_column(bonus_idx, bonus_idx, 12, fmt_bonus)  # Final Score (Green)
        ws.set_column(grade_idx, grade_idx, 8, fmt_bonus)   # Grade (Green)
        ws.set_column(remark_idx, remark_idx, 25, fmt_alert) # Remarks

        for col, val in enumerate(self.result_df.columns):
            ws.write(0, col, val, fmt_header)
        ws.freeze_panes(1, 3)

        # --- Sheet 2: Grading Scale ---
        scale_data = pd.DataFrame(self.cutoffs, columns=['Letter Grade', 'Min Score'])
        scale_data.to_excel(writer, sheet_name='Rubric', index=False)
        
        # --- Sheet 3: Summary ---
        summary = self.result_df['Proposed Grade'].value_counts().reindex([c[1] for c in self.cutoffs], fill_value=0).reset_index()
        summary.columns = ['Grade', 'Count']
        summary.to_excel(writer, sheet_name='Summary', index=False)
        
        # Chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': 'Count',
            'categories': ['Summary', 1, 0, len(self.cutoffs), 0],
            'values':     ['Summary', 1, 1, len(self.cutoffs), 1],
            'data_labels': {'value': True},
            'fill':       {'color': '#4F81BD'},
            'border':     {'none': True}
        })
        chart.set_title({'name': 'Grade Distribution', 'name_font': {'size': 12, 'bold': False}})
        chart.set_legend({'none': True})
        writer.sheets['Summary'].insert_chart('D2', chart)

        writer.close()
        print(f"✅ Done! Report generated: {output_filename}")