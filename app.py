import streamlit as st
import tempfile
import os
import io
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter

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
        "caption": "insert pages from a pdf file into another one",
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

# initialize keys
for key in ['start_widget_counter',
            'end_widget_counter',
            'uploader_key_counter',
            'multi_uploader_key_counter',
            'insert_widget_counters']:
    if key not in st.session_state.keys():
        st.session_state[key] = 0

# function to reset widgets
def reset(rerun:bool = False ):
    st.session_state['uploader_key_counter'] += 1
    st.session_state['multi_uploader_key_counter'] += 1
    st.session_state['start_widget_counter'] += 1
    st.session_state['end_widget_counter'] += 1
    if rerun:
        st.rerun()
    
def reset_start_end():
    st.session_state['start_widget_counter'] += 1
    st.session_state['end_widget_counter'] += 1
    st.rerun()

def reset_start_end_insert_pages():
    st.session_state['insert_start_widget_counter'] += 1
    st.session_state['insert_end_widget_counter'] += 1

## function to insert start and end number_input widgets
def interval_pages_widgets(pdf_file_length):
    col1, col2 = st.columns(2)
    with col1:
        start = st.number_input(label = 'Start page', min_value = 1, max_value= pdf_file_length,
                                value = 1, step = 1,
                                key = f"start_key_{st.session_state['start_widget_counter']}")
    with col2:
        end = st.number_input(label = 'End page', min_value = 1,
                                max_value = pdf_file_length, step = 1, value = 1,
                                key = f"end_key_{st.session_state['end_widget_counter']}")
    
    return start, end


# SIDEBAR MENU
pdf_action = st.sidebar.radio("Actions available:",
        options = [f"{action['label']} {action['icon']}" for action in PDF_ACTIONS.values()],
        captions = [action['caption'] for action in PDF_ACTIONS.values()],
        key = 'action_active',
        on_change = reset
)

# function to upload a SINGLE file
def upload_single_file():
    return st.file_uploader("Select PDF file...", type=['pdf'],
                            key = f"file_uploader_{st.session_state['uploader_key_counter']}")


## ACTION DESCRIPTION
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
    
    # show the action description
    if st.toggle('Show function description'):
        st.write(function_docstring)

    action_button_clicked = False
## SHOW UPLOAD, START AND END PAGES WIDGETS
if pdf_action:

    # --- UI Rendering Block ---
    if action in ['extract', 'remove', 'rearrange']:

        # only one file was uploaded
        uploaded_file = upload_single_file()

        # work out the number of pages of pdf file
        if uploaded_file:
            pdf_file_length = len(PdfReader(uploaded_file).pages)
        
            # write start and end widgets' header
            if action != 'extract':
                st.write(f'Select interval of pages to be {action}d.')
            else:
                st.write(f'Select interval of pages to be {action}ed.')

            start, end = interval_pages_widgets(pdf_file_length)

            if start > end:
                st.warning("Warning: Start page should be less than or equal to the end page.")
            
            ## REARRANGE INSERT AND RELATIVE POSITION
            if action == 'rearrange':
                col1, col2 = st.columns(2)
                with col1:
                    relative_pos = st.radio("Relative position", ('before', 'after'), index = 1)
                with col2:
                    new_pos = st.number_input(label = 'New position', min_value=1, max_value=pdf_file_length,
                                                step = 1, value = 2)
                
                ## WARNING OF RESULTING PDF IS SAME AS INPUT PDF

                # there are cases when in cases where the resulting pdf
                # would be the same as the input file
                # 1. new_pos value is within extract interval
                # 2. start extract interval is right after new pos
                # in these cases, warn and do not process file
                same_file_warning = (new_pos in range(start, end + 1)) or \
                                    (relative_pos == 'after' and start == new_pos + 1) or \
                                    (relative_pos == 'before' and end == new_pos - 1)
                
                # warn about output file being sames as input file
                if same_file_warning:

                    if same_file_warning and \
                        start == 1 and \
                        end == 1 and \
                        new_pos == 2:
                        
                        st.warning(f"Your selected operation does not alter the page order. PDF file will not be processed. \
                                \n\nInsertion page should be AFTER page {new_pos}.")
                    else:

                        st.warning(f"Your selected operation does not alter the page order. PDF file will not be processed. \
                                \n\nInsertion page should be before page {start - 1} or after page {end+1}.")

    elif action == 'insert':
        source_file = st.file_uploader("Select the source PDF file...", type=['pdf'],
                                       key = f"uploader_source_{st.session_state['uploader_key_counter']}")
    
        insertion_files = st.file_uploader("Select one or more PDF files to insert...", type=['pdf'],
                            key = f"multi_uploader_key_{st.session_state['multi_uploader_key_counter']}",
                            accept_multiple_files = True)

        if source_file and insertion_files:

            # get length of source file
            source_length = len(PdfReader(source_file).pages)

            # each interval of pages from insertion files must
            # fulfill that start <= end
            # I will create a list of interval_ok
            interval_ok_list = []

            # for each of the insertion files, show start and end pages widget
            for index, ins_file in enumerate(insertion_files):
                
                # Initialize counter dictionary if it's not already one
                if isinstance(st.session_state.insert_widget_counters, int):
                    st.session_state.insert_widget_counters = {}
                if index not in st.session_state.insert_widget_counters:
                    st.session_state.insert_widget_counters[index] = 0

                st.subheader(f"\nSelect page to insert file number {index + 1}")

                # get length of insertion file
                inserted_length = len(PdfReader(ins_file).pages)

                # show relative position and insertion page widgets
                col1, col2 = st.columns(2)

                # relative position
                with col1:
                    relative_pos = st.radio("Relative position", ('before', 'after'),
                                            key = f'relative_pos_{index}')

                # insert page
                with col2:
                    insert_pos = st.number_input(label = 'Insert position', min_value = 1,
                                                    max_value=source_length, step = 1, value = 1,
                                                    key = f'insert_pos_{index}')
                
                # start and end pages widgets
                st.write("Optional: Select a range of pages to insert from the insertion file.")

                col1, col2 = st.columns(2)
            
                with col1:
                    start = st.number_input(label = 'Start page', min_value = 1, max_value= inserted_length,
                                            value = 1, step = 1, key=f"start_key_{index}_{st.session_state.insert_widget_counters[index]}")
                with col2:
                    end = st.number_input(label = 'End page', min_value = 1,
                                            max_value = inserted_length, step = 1, value = 1, key=f"end_key_{index}_{st.session_state.insert_widget_counters[index]}")
                
                if st.button('Reset pages', key = f"reset_pages_{index}"):
                    st.session_state.insert_widget_counters[index] += 1
                    st.rerun()
                
                if (end < start):
                        st.warning('Please, increase end page value to be equal or greater than start page value.')
                else:
                    interval_ok_list.append(True)

    # --- Unified Button and Processing Block ---
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button('Reset operation'):
            reset(rerun=True)
    with col2:
        if action in ['extract', 'remove', 'rearrange']:
            if st.button('Reset pages'):
                reset_start_end()
    with col3:
        # Only show the action button if the necessary files are uploaded
        if (action != 'insert' and 'uploaded_file' in locals() and uploaded_file) or \
           (action == 'insert' and 'source_file' in locals() and source_file and insertion_files):
            button_label = f"{action.capitalize()} pages"
            action_button_clicked = st.button(button_label)

    if action_button_clicked:
        try:
            output_buffer, output_filename = None, None
            if action in ['extract', 'remove']:
                if end >= start:
                    output_buffer, output_filename = function(uploaded_file, start, end)
                else:
                    st.error('Error: End page must be greater than or equal to start page.')
            
            elif action == 'rearrange':
                if end >= start and not same_file_warning:
                    output_buffer, output_filename = function(uploaded_file, start, end, relative_pos, new_pos)
                elif same_file_warning:
                    st.warning('Action canceled. The selected operation does not alter the page order.')
                else:
                    st.error('Error: End page must be greater than or equal to start page.')
            
            elif action == 'insert':
                if all(interval_ok_list):
                    # Start with a list of all pages from the source file
                    final_pages = list(PdfReader(source_file).pages)

                    for index, ins_file in enumerate(insertion_files):
                        current_relative_pos = st.session_state[f'relative_pos_{index}']
                        current_insert_pos = st.session_state[f'insert_pos_{index}']
                        counter = st.session_state.insert_widget_counters[index]
                        current_start = st.session_state[f'start_key_{index}_{counter}']
                        current_end = st.session_state[f'end_key_{index}_{counter}']
                        
                        # Get the list of pages to insert
                        pages_to_insert = function(ins_file, current_start, current_end)
                        
                        # Calculate insertion position and insert the block
                        insertion_point = current_insert_pos - 1 if current_relative_pos == 'before' else current_insert_pos
                        final_pages[insertion_point:insertion_point] = pages_to_insert

                    # Now, create the writer and add the final ordered pages
                    writer = PdfWriter()
                    for page in final_pages:
                        writer.add_page(page)
                    output_buffer = io.BytesIO()
                    writer.write(output_buffer)
                    output_filename = f"{Path(source_file.name).stem}_expanded.pdf"
                else:
                    st.error("Action canceled. Please check that all 'end' pages are greater than or equal to their 'start' pages.")

            # --- Unified Download Button ---
            if output_buffer and output_filename:
                st.download_button(f"Download {action}d file", output_buffer.getvalue(), output_filename, "application/pdf")
                st.success('Processed file ready to be downloaded!')

        except Exception as e:
            st.error(f'An unexpected error occurred: {e}')
