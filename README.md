# Fresh vs Rotten Fruit Classification

## 1. Project Title & Description
**Project Name:** FRESH: Fresh vs Rotten Fruit Classification System

**Description:**
This project is a fruit freshness classification system built with TensorFlow. It analyzes uploaded fruit images and predicts whether they are **Fresh** or **Rotten**. The project also includes a training notebook for model development, a saved trained model for reuse, and a desktop GUI for easy image selection, prediction, and result viewing. The GUI supports multiple image uploads and includes Grad-CAM explainability so users can see which parts of the image influenced the model's prediction.

---

## 2. Group / Team Members
**Repository Link:** https://github.com/JethroIsHere/Fresh.git

## Team Contributions

### 1 Kurt Allen Alorro (`@kurykatsu24`)
- Role: Project coordinator, documentation lead, and ideation
- Assigned: setup, run instructions, and project scope
- Contributions:
	- [ ] Updated README team details and run steps
	- [ ] Led ideation and scope notes


### 2 Christine Joy Maravilla (`@ChristineM24`)
- Role: Data preparation and dataset management
- Assigned: `fruit_images/` and dataset notes
- Completed work:
	- [ ] Organized `fruit_images/` and verified naming conventions
	- [ ] Added data preparation notes
    - [ ] Ran rigorous testing on `fruit_classification.ipynb`

### 3 Jazylle Mae Senibalo (`@yllezy`)
- Role: Model training and evaluation; prepare presentation slides (PPT)
- Assigned: model evaluation notes and PPT deliverable
- Completed work:
	- [ ] Updated notebook workflow and recorded metrics
	- [ ] Prepared PPT outline 

### 4 Duke Salfred Bocala (`@enryu`)
- Role: GUI integration and prediction flow
- Assigned: `fruit_gui.py` improvements and explainability
- Completed work:
	- [ ] Updated GUI controls and tested explainability popup

### 5 Jethro Roland Dañocup (`@JethroIsHere`)
- Role: Testing, QA, dependency checks, final submission, and model exports
- Assigned: `fruit_classification.ipynb` (final runs) and `requirements.txt`
- Completed work:
	- [ ] Verified model export and requirements
	- [ ] Ran final training/evaluation and export `fruit_classification_model.h5`
---

## 3. Prerequisites / Requirements

### Folder Setup
Create a project folder named by your group (for example):
- `groupname/` or
- `groupnumber/`

Example:
```powershell
mkdir group5
cd group5
```

### Programming Language
- Python 3.10+ (recommended: Python 3.10 or Python 3.11)

### Required Libraries
Install dependencies from `requirements.txt`:
- tensorflow
- numpy
- pillow
- customtkinter
- matplotlib
- scipy

Optional for notebook workflows:
- jupyter

---

## 4. How to Run the Program

### A. Clone and open project
```powershell
git clone https://github.com/JethroIsHere/Fresh.git
cd Fresh
```

### B. Create and activate virtual environment (Windows PowerShell)
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### C. Install dependencies
```powershell
pip install -r requirements.txt
```

### D. Ensure model file exists
Before running GUI, confirm this file exists in the project root:
- `fruit_classification_model.h5`

If missing, run the notebook first (`fruit_classification.ipynb`) to train/export the model.

### E. Run the GUI app
```powershell
python fruit_gui.py
```

---

## Configuration Notes
- Keep `fruit_classification_model.h5` in the same folder as `fruit_gui.py`.
- The GUI expects image inputs (`.jpg`, `.jpeg`, `.png`, `.webp`).
- Default model path in code: `MODEL_PATH = 'fruit_classification_model.h5'`.

---


