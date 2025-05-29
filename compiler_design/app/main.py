import streamlit as st
from analyzer import detect_syntax_errors, detect_logical_errors
from complexity import analyze_time_complexity, analyze_space_complexity
from optimizer import optimize_code

def add_line_numbers(code):
    if not code:
        return ""
    lines = code.split('\n')
    numbered_lines = [f"{i+1:3d} | {line}" for i, line in enumerate(lines)]
    return '\n'.join(numbered_lines)

def main():
    st.set_page_config(
        page_title='Code Analyzer',
        page_icon='💻',
        layout='wide'
    )

    st.title('💻 Code Analyzer')
    st.write('Analyze and optimize your code with AI-powered tools.')

    # Sidebar for language selection
    language = st.sidebar.selectbox(
        'Select Language',
        ['Python', 'C++', 'Java']
    )

    # Main content area with line numbers
    code = st.text_area(
        'Enter your code here:',
        height=300,
        help='Paste your code here for analysis'
    )

    # Display code with line numbers
    if code:
        st.subheader('Code Preview with Line Numbers')
        st.code(add_line_numbers(code), language=language.lower())

    if st.button('Analyze Code'):
        if not code.strip():
            st.error('Please enter some code before analyzing.')
            return

        try:
            # Create columns for different analyses
            col1, col2 = st.columns(2)

            with col1:
                st.subheader('Syntax Analysis')
                syntax_result = detect_syntax_errors(code, language)
                st.info(syntax_result)

                st.subheader('Logical Analysis')
                logic_result = detect_logical_errors(code, language)
                st.info(logic_result)

            with col2:
                st.subheader('Complexity Analysis')
                time_complexity = analyze_time_complexity(code, language)
                space_complexity = analyze_space_complexity(code, language)
                st.info(f'Time Complexity: {time_complexity}')
                st.info(f'Space Complexity: {space_complexity}')

            # Code Optimization
            st.subheader('Code Optimization')
            optimized_code = optimize_code(code, language)
            st.code(add_line_numbers(optimized_code), language=language.lower())

            # Add download button for optimized code
            st.download_button(
                label='Download Optimized Code',
                data=optimized_code,
                file_name=f'optimized_code.{language.lower()}',
                mime='text/plain'
            )
        except Exception as e:
            st.error(f'An error occurred during analysis: {str(e)}')

if __name__ == '__main__':
    main()