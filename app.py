import streamlit as st
import tempfile
import os

from scripts.extract_pages      import extract_pages
from scripts.insert_pages       import insert_pages
from scripts.merge_files        import merge_files
from scripts.rearrange_pages    import rearrange_pages
from scripts.remove_pages       import remove_pages

st.title('PDF Editor')

st.header('PDF Editor')

st.subheader('Choose a function:')

pdf_function = st.radio("Action to be performed:",
        options = ['Extract pages',
                    'Insert pages',
                    'Merge pdf files',
                    'Rearrange pages',
                    'Remove pages'],
        captions = ['extract pages from a pdf file',
                    'insert pages from a pdmf file into another one',
                    'concatenate several pdf files into a final merged pdf file',
                    'rearrange the pages of a pdf file',
                    'remove pages from a pdf file']
)

if pdf_function == 'Extract pages':
    st.header('Extract pages from pdf file')
    if st.toggle('Show function description'):
        st.write("""
                Extracts a range of pages from a PDF and saves them as a new file.

                Select a starting and an ending page from your PDF to create a new, smaller PDF containing only the pages within that range (inclusive).
                
                For example, if you choose start=3 and end=5, the new PDF will contain pages 3, 4, and 5 from the original file.extract_pages.
                """)
    # Initialize the key for upload_file in session state
    if 'file_uploader_key' not in st.session_state:
        st.session_state['file_uploader_key'] = 0
    
    file = st.file_uploader("Select a pdf file...",
                            key = st.session_state['file_uploader_key'],
                            type=['pdf']
                            )

    if file:

        # create a temp folder
        temp_dir_path = tempfile.mkdtemp()
        
        # get full path of uploaded file
        filename_path = os.path.join(temp_dir_path, file.name)

        # create the actual file
        with open(filename_path, 'wb') as f:
            f.write(file.read())
                    
        # st.write(f"Uploaded file full path: {filename_path}")
    
    start = st.number_input('Start page', min_value = 1, value = 1, step = 1 )
    end = st.number_input('End page', min_value = 1, value = 1, step = 1)

    if st.button('Extract pages'):
        extract_pages(filename_path, start, end)
    
    if file:
        if st.button('Reset Extract pages'):
            st.session_state['file_uploader_key'] += 1
            st.rerun()