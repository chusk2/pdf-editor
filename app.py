import streamlit as st
import tempfile
import os

from PyPDF2 import PdfReader

from scripts.extract_pages      import extract_pages
from scripts.insert_pages       import insert_pages
from scripts.merge_files        import merge_files
from scripts.rearrange_pages    import rearrange_pages
from scripts.remove_pages       import remove_pages

st.title('PDF Editor')

st.sidebar.markdown('# Choose an action')
st.sidebar.subheader('Select an action from the list below to perform on a pdf file')

PDF_ACTIONS = {
    "extract": {
        "label": "Extract",
        "caption": "extract pages from a pdf file",
        "icon": "✂️"  # Scissors
    },
    "insert": {
        "label": "Insert",
        "caption": "insert pages from a pdmf file into another one",
        "icon": "➕"  # Plus sign
    },
    "merge": {
        "label": "Merge",
        "caption": "concatenate several pdf files into a final merged pdf file",
        "icon": "🔗"  # Chain link
    },
    "rearrange": {
        "label": "Rearrange",
        "caption": "rearrange the pages of a pdf file",
        "icon": "🔄"  # Arrows/Revolving
    },
    "remove": {
        "label": "Remove",
        "caption": "remove pages from a pdf file",
        "icon": "🗑️"  # Trash can
    }
}

functions = {
    'extract' : extract_pages,
    'insert' : insert_pages,
    'merge' : merge_files,
    'rearrange' : rearrange_pages,
    'remove' : remove_pages
}

# SIDEBAR MENU
pdf_action = st.sidebar.radio("Actions available:",
        options = [f"{action['label']} {action['icon']}" for action in PDF_ACTIONS.values()],
        captions = [action['caption'] for action in PDF_ACTIONS.values()]
)

# extract action name from option
if pdf_action:

    action = pdf_action[:-2].split(' ')[0].lower()
    action_description = PDF_ACTIONS[action]['caption'].capitalize()
    # toggle action description and help
    st.header(action_description)

    # access the docstring from the function
    function = functions[action]
    function_docstring_lines = function.__doc__.split('\n')
    function_docstring = ''
    for line in function_docstring_lines:
        line = line.strip()
        if not line.startswith('Args:'):
            function_docstring += f'{line}\n'
        else:
            function_docstring = function_docstring.strip()
            break

    if st.toggle('Show function description'):
        st.write(function_docstring)
        
    # Initialize the key for upload_file in session state
    if 'file_uploader_key' not in st.session_state:
        st.session_state['file_uploader_key'] = 0
    
    # upload the file
    uploaded_file = st.file_uploader("Select a pdf file...",
                            key = st.session_state['file_uploader_key'],
                            type=['pdf']
                            )

    # if a file has been already uploaded
    if uploaded_file:

        pdf_file_length = len(PdfReader(uploaded_file).pages)

        # show start and end number inputs after a file has been uploaded
        # the end value is set to be at least equal to current start value
        col1, col2 = st.columns([1,1])
        with col1:
            start = st.number_input('Start page', min_value = 1, max_value= pdf_file_length,
                                    value = 1, step = 1, key = 'start_value' )
        with col2:
            end = st.number_input('End page', min_value = st.session_state['start_value'],
                                  max_value= pdf_file_length,
                                  value = st.session_state['start_value'], step = 1)

        col1, col2, col3 = st.columns([1,1,2])

        with col1:
            if st.button('Reset operation'):
                st.session_state['file_uploader_key'] += 1
                st.rerun()

        with col2:
            if st.button('Extract pages'):
                
                output_buffer, output_filename = function(uploaded_file, start, end)

                # try:
                #     output_buffer, output_filename = extract_pages(uploaded_file, start, end)
                    
                # except:
                #     st.warning('Error: extraction failed!')
        
                with col3:
                    # extraction process ok
                    st.download_button(
                        label="Download extracted pages",
                        data=output_buffer.getvalue(), # Get the bytes from the buffer
                        file_name=output_filename,
                        mime="application/pdf"
                    )
