# Fresh vs Rotten Fruit Classification

## 1. Project Title & Description
**Project Name:** FRESH: Fresh vs Rotten Fruit Classification System

**Description:**
This project is a TensorFlow-based fruit freshness classifier. It takes an uploaded fruit image and predicts whether the fruit is **Fresh** or **Rotten**. The repository includes a training notebook for model development, a saved model for reuse, and a desktop GUI for easy prediction. The GUI supports multiple image uploads and includes Grad-CAM explainability so users can see which image areas influenced the prediction.

---

## 2. Group / Team Members
**Repository Link:** https://github.com/JethroIsHere/Fresh.git

### Team Contributions

1. **Kurt Allen Alorro** (`@kurykatsu24`)
- Email: kurtallen.alorro@wvsu.edu.ph
- Role: Project coordinator, documentation lead, and ideation
- Assigned files: `README.md`
- Contribution summary: planned the project scope, organized documentation, and led ideation for the system design.

2. **Christine Joy Maravilla** (`@ChristineM24`)
- Email: christinejoy.maravilla@wvsu.edu.ph
- Role: Data preparation and dataset management
- Assigned files: `fruit_images/`
- Contribution summary: organized the fruit image dataset, checked naming consistency, and prepared image assets for training and testing.

3. **Jazylle Mae Senibalo** (`@yllezy`)
- Email: jazyllemae.senibalo@wvsu.edu.ph
- Role: Model training, evaluation, and presentation slides (PPT)
- Assigned files: `fruit_classification.ipynb`, `FRESH_PPT.pdf`
- Contribution summary: handled notebook training, evaluated model performance, and prepared the presentation slides for defense.

4. **Duke Salfred Bocala** (`@enryu`)
- Email: dukesalfredbocala4@gmail.com
- Role: GUI integration and prediction flow
- Assigned files: `fruit_gui.py`
- Contribution summary: developed the desktop interface, integrated prediction logic, and added the explainability popup.

5. **Jethro Roland Dañocup** (`@JethroIsHere`)
- Email: danocupjethro913@gmail.com
- Role: Testing, QA, dependency checks, final submission, and model exports
- Assigned files: `requirements.txt`, `fruit_classification_model.h5`
- Contribution summary: finalized the trained model, managed dependencies, checked the full workflow, and prepared the project for submission.

---

## 3. Prerequisites / Requirements

### Programming Language
- Python 3.10 or Python 3.11

### Required Libraries / Dependencies
Install the dependencies listed in `requirements.txt`:
- tensorflow
- numpy
- pillow
- customtkinter
- matplotlib
- scipy
- jupyter

If the model file is stored through Git LFS, make sure Git LFS is installed on your machine before cloning or pulling the repository.

---

## 4. How to Run the Program

### A. Clone the repository
```powershell
git clone https://github.com/JethroIsHere/Fresh.git
cd Fresh
```

### B. Create and activate a virtual environment
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### C. Install the required libraries
```powershell
pip install -r requirements.txt
```

### D. Prepare the model file
Make sure `fruit_classification_model.h5` is present in the project root. If it is missing, open and run `fruit_classification.ipynb` first to train or export the model.

### E. Run the GUI
```powershell
python fruit_gui.py
```

---

## Configuration Notes
- Keep `fruit_classification_model.h5` in the same folder as `fruit_gui.py`.
- The GUI accepts `.jpg`, `.jpeg`, `.png`, and `.webp` files.
- The model path used by the app is `fruit_classification_model.h5`.
- If Git LFS is enabled on the repository, install Git LFS before cloning so the model file downloads correctly.

---


