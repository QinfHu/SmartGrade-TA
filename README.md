# 🎓 SmartGrade-TA

**SmartGrade-TA** is a Python-based automation tool designed for Teaching Assistants (TAs) and Instructors. It instantly converts raw CSV grade exports (from LMS like Brightspace or Canvas) into professional, scientific-style Excel reports.

It handles weighted calculations, applies bonus points, detects "borderline" students, and formats the output for easy review by Professors or Department Chairs.

---

## 🇬🇧 English Documentation

### ✨ Key Features

* **Auto-Calculation:** Automatically calculates weighted totals based on your custom rubric (e.g., Homework 30%, Final 40%).
* **Scientific Reporting:** Generates a minimalist, research-style Excel report with "freeze panes" for easy navigation.
* **Visual Comparison:** Side-by-side comparison of **Raw Scores** (Grey) vs. **Final Scores with Bonus** (Green Highlight), making the impact of curves/bonuses transparent.
* **Red Flags & Borderlines:** Automatically detects:
    * Missing assignments (0 scores).
    * "Borderline" students (e.g., within 0.5 points of the next letter grade).
* **Privacy First:** Built-in `.gitignore` ensures student data is never uploaded to GitHub.

### 🚀 Quick Start

#### 1. Installation
Ensure you have Python installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt

2. Prepare Your Data
Export the grade book from your LMS (Brightspace, Canvas, Blackboard) as a CSV file.

Place the CSV file in the project folder.

Note: The script uses fuzzy matching. As long as your column headers contain keywords like "Homework", "Midterm", or "Final", it will recognize them.

3. Configure the Script
Open main.py and update the configuration section:

Python

# main.py

# 1. Your CSV Filename
INPUT_FILE = 'Your_Course_Export.csv' 

# 2. Grading Weights (Must sum to approx 1.0)
WEIGHTS = {
    'Homework': 0.28,
    'Lab': 0.06,
    'Midterm': 0.32,
    'Final': 0.20,
    'Portfolio': 0.04
}

# 3. Bonus Points (Added to the final score)
BONUS_POINTS = 1.0 
4. Run the Script
Execute the script in your terminal:

Bash

python main.py
📊 Output
The tool will generate a new Excel file (e.g., Final_Grades_Report.xlsx) containing:

Gradebook: The master list with calculated grades and remarks.

Summary: A grade distribution histogram and statistics.

Rubric: A reference sheet showing the grading scale used.

🛡️ Privacy & Security
Student privacy (FERPA) is the top priority.

Local Processing: This script runs entirely on your local machine. No data is sent to the cloud.

Git Protection: The repository includes a .gitignore file pre-configured to exclude *.csv and *.xlsx files. This prevents you from accidentally uploading real student data to GitHub.

🇨🇳 中文说明 (Chinese Documentation)
📖 项目简介
SmartGrade-TA 是一款专为助教 (TA) 设计的成绩处理自动化工具。它可以将学校系统（如 Brightspace/Canvas）导出的原始 CSV 成绩单，一键转换为排版精美、符合科研习惯的 Excel 报表。

✨ 核心功能
- 自动加权计算： 根据你设定的权重（如：作业 30%，期末 40%）自动计算总分。

- 直观的分数对比： 报表中会并列展示 “原始分” (灰色) 和 “含加分后的最终分” (绿色高亮)，让导师一眼看出加分（Bonus）对成绩的影响。

- 异常与边缘检测： 自动在备注栏标记以下情况：

- 缺交 (Missing): 某项作业或考试为 0 分。

- 边缘人 (Borderline): 距离下一档等级仅差 0.5 分以内的学生（方便决定是否“捞人”）。

科研风格排版： 生成的表格极其干净、专业，关键列高亮，并自动冻结首行首列。

🚀 使用步骤
1. 安装依赖
下载代码后，在终端运行以下命令安装所需的 Python 库：

Bash

pip install -r requirements.txt
2. 准备数据
从学校系统下载成绩单（CSV 格式），并将其放入项目文件夹中。

注意： 代码支持模糊匹配。只要 CSV 表头里包含 "Homework", "Midterm" 等关键词，程序就能自动识别，无需手动改名。

3. 修改配置
打开 main.py 文件，修改顶部的配置区域：

Python

# main.py

# 1. 输入文件名 (你下载的 CSV)
INPUT_FILE = 'Your_Course_Export.csv' 

# 2. 权重配置 (名称需与表头关键词对应)
WEIGHTS = {
    'Homework': 0.28,
    'Lab': 0.06,
    'Midterm': 0.32, # 期中
    'Final': 0.20,   # 期末
    'Portfolio': 0.04
}

# 3. 全员加分 (例如全班加 1 分)
BONUS_POINTS = 1.0 
4. 运行程序
在终端输入：

Bash

python main.py
📊 输出结果
程序会生成一个新的 Excel 文件，包含：

Gradebook: 包含原始分、最终分、等级建议及备注的完整名单。

Summary: 自动生成的成绩分布直方图。

Rubric: 本次评分使用的分数线标准说明。

🛡️ 隐私保护说明
保护学生隐私 (FERPA) 是本工具设计的红线。

本地运行： 所有数据处理均在你的电脑本地完成，不会上传至任何云端。

防止误传： 项目内置了 .gitignore 文件，配置为自动忽略所有的 .csv 和 .xlsx 文件。这意味着即使你执行了 git 上传命令，真实的成绩单也不会被上传到 GitHub，确保绝对安全。

📝 License
MIT License. Free for all TAs to use.