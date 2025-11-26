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
            'multi_uploader_key_counter']:
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


## SHOW UPLOAD, START AND END PAGES WIDGETS
if pdf_action:

    ## EXTRACT, REMOVE, REARRANGE ACTIONS
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

            ## RESET AND PERFORM ACTION BUTTONS
            col1, col2, col3 = st.columns([1, 1, 2])

            # RESET BUTTON
            with col1:
                if st.button('Reset operation'):
                    reset(rerun = True)
            
            # RESET ONLY PAGES SELECTOR BUTTON
            with col2:
                if st.button('Reset pages'):
                    reset_start_end()
            
            ## ACTION BUTTON
            with col3:
                button_label = f"{action.capitalize()} files" if action == 'merge' else f"{action.capitalize()} pages"
                action_button_clicked = st.button(button_label)
                    
    ## INSERT ACTION
    if action == 'insert':
        source_file = st.file_uploader("Select the source PDF file...", type=['pdf'])
    
        insertion_files = st.file_uploader("Select one or more PDF files to insert...", type=['pdf'],
                            key = f"multi_uploader_key_{st.session_state['multi_uploader_key_counter']}",
                            accept_multiple_files = True)

        if source_file and insertion_files:

            # get length of source file
            source_length = len(PdfReader(source_file).pages)

            # for each of the insertion files, show start and end pages widget
            for index, ins_file in enumerate(insertion_files):

                st.subheader(f"\nSelect page to insert file number {index + 1}")

                # get length of insertion file
                inserted_length = len(PdfReader(ins_file).pages)

                # show relative position and insertion page widgets
                col1, col2 = st.columns(2)

                # relative position
                with col1:
                    relative_pos = st.radio("Relative position", ('before', 'after'),
                                            key = f'relative_pos_radio_{index}')

                # insert page
                with col2:
                    insert_pos = st.number_input(label = 'Insert position', min_value = 1,
                                                    max_value=source_length, step = 1, value = 1,
                                                    key = f'insert_pos_radio_{index}')
                
                # start and end pages widgets
                st.write("Optional: Select a range of pages to insert from the insertion file.")

                col1, col2 = st.columns(2)
                with col1:
                    start = st.number_input(label = 'Start page', min_value = 1, max_value= inserted_length,
                                            value = 1, step = 1,
                                            key = f"start_key_{index}")
                with col2:
                    end = st.number_input(label = 'End page', min_value = 1,
                                            max_value = inserted_length, step = 1, value = 1,
                                            key = f"end_key_{index}")

            ## RESET AND PERFORM ACTION BUTTONS
            col1, col2, col3 = st.columns([1, 1, 2])

            # RESET BUTTON
            with col1:
                if st.button('Reset operation'):
                    reset(rerun = True)
            
            # RESET ONLY PAGES SELECTOR BUTTON
            with col2:
                if st.button('Reset pages'):
                    reset_start_end()
            
            ## ACTION BUTTON
            with col3:
                button_label = f"{action.capitalize()} files" if action == 'merge' else f"{action.capitalize()} pages"
                action_button_clicked = st.button(button_label)

    # if action == 'merge':
    #     uploaded_files = upload_several_files()

            ## ONCE ACTION BUTTON IS CLICKED
            if action_button_clicked:
            
                ## EXTRACT, REMOVE, REARRANGE, INSERT

                # check if interval of pages is ok
                if action != 'insert':
                    # check in all cases that end page is >= start page
                    interval_ok = end >= start

                try:
                    if action in ['extract', 'remove']:
                        if interval_ok:
                            output_buffer, output_filename = function(uploaded_file, start, end)
                    
                    # elif action == 'merge':
                    #     output_buffer, output_filenames = function(uploaded_files)
                    
                    elif action == 'rearrange':
                        if interval_ok:
                            
                            # check if the output file would be same as input file
                            # read comments above
                            same_file_warning = ( new_pos in range(start, end+1) or \
                                                    (relative_pos == 'after' and start == new_pos + 1) )
                            
                            if not same_file_warning:
                                output_buffer, output_filename = function(uploaded_file, start, end, relative_pos, new_pos)
                            elif same_file_warning:
                                interval_ok = False
                    
                    elif action == 'insert':
                        if interval_ok and insertion_files:
                            output_buffer, output_filename = function(source_file, insertion_files,
                                                                        insert_pos, relative_pos,
                                                                        start, end)

                    with col3:
                        if interval_ok and action != 'insert':
                            st.download_button(f"Download {action}d file", output_buffer.getvalue(), output_filename, "application/pdf")
                        
                except Exception as e:
                    st.warning(f'Error: {e}')


                if (end < start) and action != 'insert':
                        st.warning('Please, increase end page value to be equal or greater than start page value.')
                
                elif action_button_clicked and (start > end):
                    st.error('Error: end page lower than start page. Action canceled')
                
                elif action_button_clicked and action == "rearrange" and same_file_warning:
                    st.warning('Action canceled. Observe warning message above.')

                if action_button_clicked and (start <= end) and not same_file_warning:
                    st.success('Processed file ready to be downloaded!')
    
