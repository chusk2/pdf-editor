import streamlit as st
import io
from pathlib import Path
#import base64

from PyPDF2 import PdfReader, PdfWriter

from scripts.extract_pages      import extract_pages
from scripts.insert_pages       import insert_pages
from scripts.merge_files        import merge_files
from scripts.rearrange_pages    import rearrange_pages
from scripts.remove_pages       import remove_pages

# ## SET BACKGROUND IMAGE

# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def set_background_image(image_path):
#     bin_str = get_base64_of_bin_file(image_path)
#     # The selector '.stApp' or '[data-testid="stAppViewContainer"]' works for the main app body
#     page_bg_img = f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/png;base64,{bin_str}");
#         background-size: cover;
#     }}
#     </style>
#     """
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# # Example usage: Make sure 'my_background.png' is in your script's directory
# # set_background_image("./assets/background_faded.png")


st.title('PDF Editor')

st.sidebar.markdown('# Choose an action')
#st.sidebar.subheader('Select an action from the list below to perform on a pdf file')

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
        "caption": "concatenate several pdf files into a final, merged pdf file",
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

## function to insert start and end number_input widgets
def interval_pages_widgets(pdf_file_length):
    col1, col2 = st.columns(2)
    with col1:
        # first page of interval
        start = st.number_input(label = 'Start page', min_value = 1, max_value= pdf_file_length,
                                value = 1, step = 1,
                                key = f"start_key_{st.session_state['start_widget_counter']}")
    with col2:
        # last page of interval
        end = st.number_input(label = 'End page', min_value = 1,
                                max_value = pdf_file_length, step = 1, value = 1,
                                key = f"end_key_{st.session_state['end_widget_counter']}")
    
    return start, end


# SIDEBAR MENU
pdf_action = st.sidebar.radio(label = "",
        options = [f"{action['label']} {action['icon']}" for action in PDF_ACTIONS.values()],
        captions = [action['caption'] for action in PDF_ACTIONS.values()],
        key = 'action_active',
        on_change = reset
)

# function to upload a SINGLE file
def upload_single_file():
    return st.file_uploader("Select PDF file...", type=['pdf'],
                            key = f"file_uploader_{st.session_state['uploader_key_counter']}")

## GENERATE ACTION DESCRIPTION
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

    ## EXTRACT, REMOVE AND REARRANGE UI
    if action in ['extract', 'remove', 'rearrange']:

        # upload just one file
        uploaded_file = upload_single_file()

        # work out the number of pages of pdf file
        if uploaded_file:
            pdf_file_length = len(PdfReader(uploaded_file).pages)
        
            # header for start and end pages of the interval
            if action != 'extract':
                st.subheader(f'Select interval of pages to be {action}d.')
            else:
                st.subheader(f'Select interval of pages to be {action}ed.')

            start, end = interval_pages_widgets(pdf_file_length)

            # show warning if lower limit of interval is greater than upper limit
            if start > end:
                st.warning("End page value must be at least equal to start page. Please, increase end page value.")
            
            ## REARRANGE: INSERT AND RELATIVE POSITION
            # in case of rearrange action, a pair of additional widgets
            # must be added: relative position and insert position
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
                # 3. the extract interval will be placed just before the insert page
                
                # in these cases, warn and do not process file
                no_pages_order_change = (new_pos in range(start, end + 1)) or \
                                    (relative_pos == 'after' and start == new_pos + 1) or \
                                    (relative_pos == 'before' and end == new_pos - 1)
                
                # if rearrangement will not produce a change, warn about it
                if no_pages_order_change:

                    if start == 1 and \
                        end == 1 and \
                        new_pos == 2:
                        
                        st.warning(f"Pages should be inserted after page {new_pos}. \
                                \n\nYour selected operation does not alter the page order. \
                                   PDF file will not be processed.")
                    
                    else:
                        st.warning(f"Pages should be inserted before page {start - 1} or after page {end+1}. \
                                   \n\nYour current operation parameters do not alter the page order.\
                                   PDF file will not be processed.")

    ## INSERT UI
    elif action == 'insert':

        st.subheader('Upload main file')

        main_file = st.file_uploader("Select the main file to insert pages into ...", type=['pdf'],
                                       key = f"uploader_source_{st.session_state['uploader_key_counter']}")
     
        st.subheader("Upload additional file(s)")
        additional_files = st.file_uploader("Select the PDF file(s) containing the pages to add.", type=['pdf'],
                            key = f"multi_uploader_key_{st.session_state['multi_uploader_key_counter']}",
                            accept_multiple_files = True)

        # once the main file and at least one addition file is uploaded
        # proceed to set the parameters for insertion
        if main_file and additional_files:

            # get length of source file
            source_length = len(PdfReader(main_file).pages)

            # check if start page <= end page
            # for each insertion file
            # Store the result of each checking in a list interval_check_list
            interval_check_list = []

            # for each of the insertion files, show start and end pages widget
            for index, add_file in enumerate(additional_files):
                
                # Initialize counter dictionary if it's not already one
                if isinstance(st.session_state.insert_widget_counters, int):
                    st.session_state.insert_widget_counters = {}
                if index not in st.session_state.insert_widget_counters:
                    st.session_state.insert_widget_counters[index] = 0

                st.subheader(f"\nSelect page where additional file {index + 1} will be inserted.")

                # get length of insertion file
                add_file_length = len(PdfReader(add_file).pages)

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
                st.write("Optional: select a range of pages from additional file to be inserted.")

                col1, col2 = st.columns(2)
            
                with col1:
                    start = st.number_input(label = 'Start page', min_value = 1, max_value= add_file_length,
                                            value = 1, step = 1, key=f"start_key_{index}_{st.session_state.insert_widget_counters[index]}")
                with col2:
                    end = st.number_input(label = 'End page', min_value = 1,
                                            max_value = add_file_length, step = 1, value = 1, key=f"end_key_{index}_{st.session_state.insert_widget_counters[index]}")
                
                if st.button('Reset page values', key = f"reset_pages_{index}"):
                    st.session_state.insert_widget_counters[index] += 1
                    st.rerun()
                
                if (end < start):
                        st.warning('End page value must be at least equal to start page. Please, increase end page value.')
                else:
                    interval_check_list.append(True)

    ## MERGE UI
    elif action == 'merge':
        st.subheader("Upload files to merge ...")
        files_to_merge = st.file_uploader("Select two or more PDF files to combine.", type=['pdf'],
                                          key=f"multi_uploader_key_{st.session_state['multi_uploader_key_counter']}",
                                          accept_multiple_files=True)
        if files_to_merge and len(files_to_merge) < 2:
            st.warning("Please upload at least two files to merge.")

    ## BUTTONS FOR RESET OR PROCESS ACTION
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button('Reset operation'):
            reset(rerun=True)
    with col2:
        if action in ['extract', 'remove', 'rearrange']:
            if st.button('Reset interval pages'):
                reset_start_end()
    with col3:
        # show action button ONLY if necessary files have been uploaded
        if (action != 'insert' and 'uploaded_file' in locals() and uploaded_file) or \
           (action == 'insert' and 'main_file' in locals() and main_file and additional_files) or \
           (action == 'merge' and 'files_to_merge' in locals() and files_to_merge and len(files_to_merge) >= 2):
            button_label = f"{action.capitalize()} pages"
            action_button_clicked = st.button(button_label)

    ## ONCE ACTION BUTTON HAS BEEN CLICKED
    if action_button_clicked:
        try:
            
            # initialize buffer and filename output variables
            output_buffer, output_filename = None, None

            # check interval pages
            if action in ['extract', 'remove']:
                if end >= start:
                    output_buffer, output_filename = function(uploaded_file, start, end)
                else:
                    st.error('Error: End page must be greater than or equal to start page.')
            
            # check interval pages
            elif action == 'rearrange':
                if end >= start:

                    # operation ACTUALLY changes pdf pages order
                    if not no_pages_order_change:
                        output_buffer, output_filename = function(uploaded_file, start, end, relative_pos, new_pos)

                    # current rearrangement parameters do not produce pages order change
                    elif no_pages_order_change:
                        st.warning('Action canceled. The current parameters for this operation do not alter the page order.')
                else:
                    st.error('Error: End page must be greater than or equal to start page.')
            
            elif action == 'insert':
                if all(interval_check_list):
                    # Start with a list of all pages from the source file
                    final_pages = list(PdfReader(main_file).pages)

                    for index, ins_file in enumerate(additional_files):
                        current_relative_pos = st.session_state[f'relative_pos_{index}']
                        current_insert_pos = st.session_state[f'insert_pos_{index}']
                        counter = st.session_state.insert_widget_counters[index]
                        current_start = st.session_state[f'start_key_{index}_{counter}']
                        current_end = st.session_state[f'end_key_{index}_{counter}']
                        
                        # Get the list of pages to insert
                        pages_to_insert = function(additional_files, current_start, current_end)
                        
                        # Calculate insertion position and insert the block
                        insertion_point = current_insert_pos - 1 if current_relative_pos == 'before' else current_insert_pos
                        final_pages[insertion_point : insertion_point] = pages_to_insert

                    # Now, create the writer and add the final ordered pages
                    writer = PdfWriter()
                    for page in final_pages:
                        writer.add_page(page)
                    output_buffer = io.BytesIO()
                    writer.write(output_buffer)
                    output_filename = f"{Path(smain_file.name).stem}_expanded.pdf"
                else:
                    st.error("Action canceled. Please check that end page value is greater than or equal to start page value for all additional files.")

            elif action == 'merge':
                if files_to_merge and len(files_to_merge) >= 2:
                    output_buffer, output_filename = function(files_to_merge)

            # --- Unified Download Button ---
            if output_buffer and output_filename:
                st.download_button(f"Download {action}d file", output_buffer.getvalue(), output_filename, "application/pdf")
                st.success('File successfuly processed. File ready to be downloaded!')

        except Exception as e:
            st.error(f'An unexpected error occurred: {e}')
