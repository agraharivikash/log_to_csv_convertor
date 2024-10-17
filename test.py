import streamlit as st
import csv
import io
import numpy

def convert_system_log_to_csv(log_file):
    """
    Converts a system log file into a structured CSV file.

    :param log_file: The uploaded log file.
    :return: CSV file as a string object.
    """
    log_content = log_file.read().decode('utf-8')  # Read the uploaded log file content
    lines = log_content.splitlines()  # Split file into lines

    # Create an in-memory string buffer to hold CSV data
    output = io.StringIO()
    csvwriter = csv.writer(output)

    # Writing CSV headers
    csvwriter.writerow(['Timestamp', 'IP Address', 'Event Message'])

    # Extracting structured data from each line
    for line in lines:
        try:
            timestamp, ip_address, *message = line.split(maxsplit=2)  # Parse the line
            event_message = ''.join(message).strip()  # Join and clean the message
            csvwriter.writerow([timestamp, ip_address, event_message])
        except ValueError:
            continue  # Skip lines that don't match the format

    output.seek(0)  # Move to the beginning of the StringIO buffer
    return output.getvalue()  # Return the CSV content as a string


st.title("System Log to CSV Converter")

# File uploader
uploaded_file = st.file_uploader("Upload your system log file", type=['log', 'txt', 'bin', 'unknown'])

if uploaded_file is not None:
    # Convert the uploaded system log file to CSV
    csv_data = convert_system_log_to_csv(uploaded_file)

    # Provide download button for the CSV file
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="converted_system_log.csv",
        mime="text/csv"
    )
