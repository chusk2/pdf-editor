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

def reset_uploader_key():
    if 'file_uploader_key' in st.session_state:
        st.session_state['file_uploader_key'] += 1

# SIDEBAR MENU
pdf_action = st.sidebar.radio("Actions available:",
        options = [f"{action['label']} {action['icon']}" for action in PDF_ACTIONS.values()],
        captions = [action['caption'] for action in PDF_ACTIONS.values()],
        key = 'action_active',
        on_change = reset_uploader_key
)

def upload_files(action):
    # Initialize the key for upload_file in session state
    if 'file_uploader_key' not in st.session_state:
        st.session_state['file_uploader_key'] = 0

    ## INSERT ACTION
    if action == 'insert':
        st.session_state['file_uploader_key_2'] = st.session_state.get('file_uploader_key_2', 100)
        source_file = st.file_uploader("Select the source PDF file...",
                                       key=st.session_state['file_uploader_key'],
                                       type=['pdf'])
        inserted_files = st.file_uploader("Select the PDF file to insert...",
                                         key=st.session_state['file_uploader_key_2'],
                                         type=['pdf'],
                                         accept_multiple_files=True)
        return {'source': source_file, 'inserted_files': inserted_files}
    
    ## MERGE ACTION
    elif action == 'merge':
        uploaded_files = st.file_uploader("Select PDF files...",
                                         key=st.session_state['file_uploader_key'],
                                         type=['pdf'],
                                         accept_multiple_files=True)
        return {'files': uploaded_files}
    
    ## EXTRACT, REARRANGE OR REMOVE
    else:
        uploaded_file = st.file_uploader("Select a PDF file...",
                                         key=st.session_state['file_uploader_key'],
                                         type=['pdf'])
        return {'files': [uploaded_file] if uploaded_file else []}

# extract action name from option
if pdf_action:
    action = pdf_action[:-2].split(' ')[0].lower()
    action_description = PDF_ACTIONS[action]['caption'].capitalize()
    st.header(action_description)

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
    
    # show the upload file widget, adapted for each action
    uploaded_files = upload_files(action)

    # if there are uploaded files
    if any(uploaded_files.values()):

        # design upload and page limits
        # for extract, remove and rearrange actions
        if action in ['extract', 'remove', 'rearrange']:
            uploaded_file = uploaded_files['files'][0]

            pdf_file_length = len(PdfReader(uploaded_file).pages)
            
            col1, col2 = st.columns(2)
            with col1:
                start = st.number_input(label = 'Start page', min_value = 1, max_value= pdf_file_length,
                                        value = 1, step = 1, key = 'start_value')
            with col2:
                end = st.number_input(label = 'End page', min_value = st.session_state['start_value'],
                                      max_value = pdf_file_length, step = 1, key = st.session_state['start_value'])
            
            if action == 'rearrange':
                col1, col2 = st.columns(2)
                with col1:
                    relative_pos = st.radio("Relative position", ('before', 'after'))
                with col2:
                    new_pos = st.number_input(label = 'New position', min_value=1, max_value=pdf_file_length,
                                              step = 1, value = 1)

        # design upload and page limits for insert action
        elif action == 'insert':
            source_file = uploaded_files['source']
            inserted_files = uploaded_files['insert']
            if source_file and inserted_files:
                source_length = len(PdfReader(source_file).pages)
                for ins_file in inserted_files:
                    inserted_length = len(PdfReader(ins_file).pages)
                    col1, col2 = st.columns(2)
                    # relative position
                    with col1:
                        relative_pos = st.radio("Relative position", ('before', 'after'))
                    # insert page
                    with col2:
                        insert_pos = st.number_input(label = 'Insert position', min_value = 1,
                                                     max_value=source_length, step = 1, value = 1)
                    # interval from insertion file
                    st.write("Optional: Select a range of pages to insert from the insertion file.")
                    col1, col2 = st.columns(2)
                    with col1:
                        start_insertion = st.number_input(label = 'Start page (insertion)', min_value=1,
                                                          max_value= inserted_length, step = 1, value = 1, key = 'start_insertion')
                    with col2:
                        end_insertion = st.number_input(label = 'End page (insertion)', min_value=st.session_state['start_insertion'],
                                                        max_value = inserted_length, step = 1, value = st.session_state['start_insertion'])


        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if st.button('Reset operation'):
                st.session_state['file_uploader_key'] += 1
                if 'file_uploader_key_2' in st.session_state:
                    st.session_state['file_uploader_key_2'] += 1
                st.rerun()

        with col2:
            button_label = f"{action.capitalize()} files" if action == 'merge' else f"{action.capitalize()} pages"
            if st.button(button_label):
                try:
                    if action in ['extract', 'remove']:
                        output_buffer, output_filename = function(uploaded_files['files'][0], start, end)
                    elif action == 'merge':
                        output_buffer, output_filename = function(uploaded_files['files'])
                    elif action == 'rearrange':
                        output_buffer, output_filename = function(uploaded_files['files'][0], start, end, relative_pos, new_pos)
                    elif action == 'insert':
                        output_buffer, output_filename = function(source_file, inserted_files, insert_pos, relative_pos, start_insertion, end_insertion)

                    with col3:
                        st.download_button(f"Download {action}d file", output_buffer.getvalue(), output_filename, "application/pdf")
                    st.success('Processed file ready to be downloaded!')
                except Exception as e:
                    st.warning(f'Error: {e}')
