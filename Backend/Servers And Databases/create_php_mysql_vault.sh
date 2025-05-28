#!/bin/bash

# PHP & MySQL 3-Day Learning Vault Setup Script
# Creates organized folder structure for intensive learning

echo "🚀 Setting up PHP & MySQL 3-Day Learning Vault..."

# Create main directory
MAIN_DIR="PHP_MySQL_3Day_Bootcamp"
mkdir -p "$MAIN_DIR"

# Day 1: PHP Fundamentals & Environment Setup
DAY1_DIR="$MAIN_DIR/Day_1_PHP_Fundamentals"
mkdir -p "$DAY1_DIR"

# Day 1 Files
touch "$DAY1_DIR/1.1_Environment_Setup.md"
touch "$DAY1_DIR/1.2_PHP_Syntax_Essentials.md"
touch "$DAY1_DIR/1.3_Variables_Data_Types.md"
touch "$DAY1_DIR/1.4_Control_Structures.md"
touch "$DAY1_DIR/1.5_Functions_Basics.md"
touch "$DAY1_DIR/1.6_Arrays_Manipulation.md"
touch "$DAY1_DIR/1.7_Form_Handling.md"
touch "$DAY1_DIR/1.8_Day1_Review_Checklist.md"

# Day 2: Advanced PHP & MySQL Integration
DAY2_DIR="$MAIN_DIR/Day_2_Advanced_PHP_MySQL"
mkdir -p "$DAY2_DIR"

# Day 2 Files
touch "$DAY2_DIR/2.1_MySQL_Setup_Basics.md"
touch "$DAY2_DIR/2.2_SQL_CRUD_Operations.md"
touch "$DAY2_DIR/2.3_PHP_MySQL_Connection.md"
touch "$DAY2_DIR/2.4_Prepared_Statements.md"
touch "$DAY2_DIR/2.5_Sessions_Cookies.md"
touch "$DAY2_DIR/2.6_Error_Handling_Security.md"
touch "$DAY2_DIR/2.7_File_Upload_Management.md"
touch "$DAY2_DIR/2.8_Day2_Review_Checklist.md"

# Day 3: Real-World Application & Deployment
DAY3_DIR="$MAIN_DIR/Day_3_Application_Deployment"
mkdir -p "$DAY3_DIR"

# Day 3 Files
touch "$DAY3_DIR/3.1_OOP_PHP_Essentials.md"
touch "$DAY3_DIR/3.2_MVC_Architecture_Basics.md"
touch "$DAY3_DIR/3.3_Database_Design_Best_Practices.md"
touch "$DAY3_DIR/3.4_Building_Complete_CRUD_App.md"
touch "$DAY3_DIR/3.5_Authentication_Authorization.md"
touch "$DAY3_DIR/3.6_Performance_Optimization.md"
touch "$DAY3_DIR/3.7_Deployment_Production.md"
touch "$DAY3_DIR/3.8_Day3_Final_Review.md"

# Create project workspace
PROJECT_DIR="$MAIN_DIR/Practical_Projects"
mkdir -p "$PROJECT_DIR"
touch "$PROJECT_DIR/Project_1_Contact_Form.md"
touch "$PROJECT_DIR/Project_2_User_Management_System.md"
touch "$PROJECT_DIR/Project_3_Blog_Application.md"

# Create reference materials
REF_DIR="$MAIN_DIR/Reference_Materials"
mkdir -p "$REF_DIR"
touch "$REF_DIR/PHP_Quick_Reference.md"
touch "$REF_DIR/MySQL_Commands_Cheatsheet.md"
touch "$REF_DIR/Common_Interview_Questions.md"
touch "$REF_DIR/Resources_Links.md"

# Create main index file
cat > "$MAIN_DIR/README.md" << 'EOF'
# PHP & MySQL 3-Day Intensive Bootcamp

## 🎯 Goal
Transform from basic understanding to resume-worthy proficiency in PHP & MySQL within 3 days.

## 📅 Schedule Overview

### Day 1: PHP Fundamentals & Environment
- Environment setup and configuration
- Core PHP syntax and fundamentals
- Data handling and form processing
- **Goal**: Solid foundation in PHP basics

### Day 2: Advanced PHP & MySQL Integration
- MySQL setup and CRUD operations
- PHP-MySQL integration with security
- Session management and file handling
- **Goal**: Database-driven applications

### Day 3: Real-World Application & Deployment
- Object-oriented PHP and MVC patterns
- Complete application development
- Authentication, optimization, and deployment
- **Goal**: Production-ready skills

## 📂 Structure
```
Day_1_PHP_Fundamentals/     # Core PHP concepts
Day_2_Advanced_PHP_MySQL/   # Database integration
Day_3_Application_Deployment/ # Real-world application
Practical_Projects/         # Hands-on projects
Reference_Materials/        # Quick references and resources
```

## ✅ Success Metrics
- [ ] Can build a complete CRUD application
- [ ] Understand security best practices
- [ ] Comfortable with PHP OOP concepts
- [ ] Can deploy applications to production
- [ ] Ready to add PHP + MySQL to resume

---
*Start with Day 1 and progress sequentially for best results.*
EOF

# Create directory tree display
echo ""
echo "📁 Vault Structure Created:"
echo "└── $MAIN_DIR/"
echo "    ├── Day_1_PHP_Fundamentals/"
echo "    │   ├── 1.1_Environment_Setup.md"
echo "    │   ├── 1.2_PHP_Syntax_Essentials.md"
echo "    │   ├── 1.3_Variables_Data_Types.md"
echo "    │   ├── 1.4_Control_Structures.md"
echo "    │   ├── 1.5_Functions_Basics.md"
echo "    │   ├── 1.6_Arrays_Manipulation.md"
echo "    │   ├── 1.7_Form_Handling.md"
echo "    │   └── 1.8_Day1_Review_Checklist.md"
echo "    ├── Day_2_Advanced_PHP_MySQL/"
echo "    │   ├── 2.1_MySQL_Setup_Basics.md"
echo "    │   ├── 2.2_SQL_CRUD_Operations.md"
echo "    │   ├── 2.3_PHP_MySQL_Connection.md"
echo "    │   ├── 2.4_Prepared_Statements.md"
echo "    │   ├── 2.5_Sessions_Cookies.md"
echo "    │   ├── 2.6_Error_Handling_Security.md"
echo "    │   ├── 2.7_File_Upload_Management.md"
echo "    │   └── 2.8_Day2_Review_Checklist.md"
echo "    ├── Day_3_Application_Deployment/"
echo "    │   ├── 3.1_OOP_PHP_Essentials.md"
echo "    │   ├── 3.2_MVC_Architecture_Basics.md"
echo "    │   ├── 3.3_Database_Design_Best_Practices.md"
echo "    │   ├── 3.4_Building_Complete_CRUD_App.md"
echo "    │   ├── 3.5_Authentication_Authorization.md"
echo "    │   ├── 3.6_Performance_Optimization.md"
echo "    │   ├── 3.7_Deployment_Production.md"
echo "    │   └── 3.8_Day3_Final_Review.md"
echo "    ├── Practical_Projects/"
echo "    │   ├── Project_1_Contact_Form.md"
echo "    │   ├── Project_2_User_Management_System.md"
echo "    │   └── Project_3_Blog_Application.md"
echo "    ├── Reference_Materials/"
echo "    │   ├── PHP_Quick_Reference.md"
echo "    │   ├── MySQL_Commands_Cheatsheet.md"
echo "    │   ├── Common_Interview_Questions.md"
echo "    │   └── Resources_Links.md"
echo "    └── README.md"

echo ""
echo "✅ Setup complete! Navigate to $MAIN_DIR to begin your 3-day journey."
echo "💡 Run this script in your desired parent directory."
echo "🚀 Ready to transform your PHP & MySQL skills!"
