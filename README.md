# 📄 PDF Editor

A versatile and user-friendly web application built with **Streamlit** that allows you to perform various operations on your PDF files.

## ✨ Features

This application provides the following PDF manipulation tools:

*   **✂️ Extract:** extract a range of pages from a PDF file.
*   **➕ Insert:** insert pages from one or more PDF files into a main PDF file.
*   **🔗 Merge:** concatenate several PDF files into a single, merged PDF file.
*   **🔄 Rearrange:** rearrange the pages of a PDF file.
*   **🗑️ Remove:** remove a range of pages from a PDF file.

## 🚀 How to Use

1.  **Choose an action:** select one of the available actions from the sidebar menu.
2.  **Upload your file(s):** use the file uploader to select the PDF file(s) you want to process.
3.  **Set parameters:** depending on the selected action, you may need to specify page ranges or other options.
4.  **Process and download:** dlick the action button (e.g., "Extract pages") to process the file(s). Once processed, a download button will appear for you to save your new PDF.

### Action-Specific Instructions

*   **Extract, Remove, and Rearrange:**
    1.  Upload a single PDF file.
    2.  Specify the 'Start page' and 'End page' for the range of pages you want to affect.
    3.  For rearranging, you'll also need to specify the new position for the selected pages.
*   **Insert:**
    1.  Upload the main PDF file you want to insert pages into.
    2.  Upload one or more additional PDF files containing the pages to be inserted.
    3.  For each additional file, specify the insertion position in the main file and, optionally, a specific range of pages to insert from the additional file.
*   **Merge:**
    1.  Upload two or more PDF files that you want to combine.
    2.  The files will be merged in the order they are listed.

## 💻 Deployment

You can run this application on your local machine or deploy it to a cloud platform that supports Python applications.

### 🏠 Local Deployment

**Prerequisites:**
*   Python 3.7+
*   pip (Python package installer)

**Linux / macOS:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/chusk2/pdf-editor.git
    cd pdf-editor
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

**Windows:**

For the simplest setup on Windows, you can use the provided batch script which automates the entire process.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/chusk2/pdf-editor.git
    cd pdf-editor
    ```
2.  **Run the launcher script:**
    Simply double-click on the `run_app.bat` file.

    The script will automatically:
    *   Check for a valid Python installation.
    *   Create a local virtual environment (`venv`).
    *   Install all required dependencies.
    *   Launch the PDF Editor application in your web browser.

    ***

    <details>
    <summary><b>Manual Installation (for advanced users)</b></summary>

    1.  **Clone the repository:**
        ```bash
        git clone https://github.com/chusk2/pdf-editor.git
        cd pdf-editor
        ```
    2.  **Create a virtual environment (recommended):**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    3.  **Install the dependencies:**
        ```bash
        pip install -r requirements.txt
        ```
    4.  **Run the application:**
        ```bash
        streamlit run app.py
        ```
    </details>

### ☁️ Cloud Deployment (e.g., Streamlit Cloud)

1.  **Fork this repository** to your GitHub account.
2.  **Sign up for Streamlit Cloud:** Go to [share.streamlit.io](https://share.streamlit.io) and sign up.
3.  **Deploy the app:** Click "New app" and choose the forked repository. Streamlit Cloud will automatically detect the `requirements.txt` file and deploy the application.

> This project was created by a self-taught junior developer with a passion for data and web development. With a background in SQL, R, and Python, and experience with data science tools like NumPy, Pandas, and Matplotlib, this project is an exploration into building practical web applications with Streamlit.