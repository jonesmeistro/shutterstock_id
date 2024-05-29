import streamlit as st
import pandas as pd

def process_images_csv(file):
    df = pd.read_csv(file)

    # Initialize a list to store the new rows
    new_rows = []

    # Define columns of interest
    columns_of_interest = ["Best Match Image URL", "Stock Image"]

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        original_image_url = row["Original Image URL"]
        for col in df.columns:
            if any(keyword in col for keyword in columns_of_interest if keyword == "Best Match Image URL") or ("Stock Image" in col and "URL" in col):
                if pd.notna(row[col]):
                    new_row = {
                        "ID Image URL": row[col],
                        "Original Image URL": original_image_url,
                        "Tag": col
                    }
                    new_rows.append(new_row)

    # Create a new dataframe from the new rows
    new_df = pd.DataFrame(new_rows)
    return new_df

def process_licenses_csv(images_df, file):
    licences_df = pd.read_csv(file)

    # Convert Asset ID to string
    licences_df['Asset ID'] = licences_df['Asset ID'].astype(str)

    # Initialize a column in processed_images_df to mark matches
    images_df['Has License'] = False

    # Check if any Asset ID appears in the ID Image URL
    for asset_id in licences_df['Asset ID']:
        images_df['Has License'] = images_df['Has License'] | images_df['ID Image URL'].str.contains(asset_id, na=False)

    # Initialize a column to mark if "shutterstock" exists in the ID Image URL
    images_df['Shutterstock'] = images_df['ID Image URL'].str.contains("shutterstock", case=False, na=False).map({True: 'Yes', False: 'No'})

    return images_df

st.title("Image and License Processor")

st.header("Upload your collection of images as a CSV file")
st.text("The URL columns from this export will be processed")

uploaded_images_file = st.file_uploader("Choose an image collection CSV file", type="csv")

if uploaded_images_file is not None:
    st.success("Image collection CSV file uploaded successfully!")
    images_df = process_images_csv(uploaded_images_file)
    st.dataframe(images_df.head())

    st.header("Upload your list of licences")
    st.text("Make sure the column with the Asset ID is called 'Asset ID'")

    uploaded_licenses_file = st.file_uploader("Choose a licenses CSV file", type="csv")

    if uploaded_licenses_file is not None:
        st.success("Licenses CSV file uploaded successfully!")
        final_df = process_licenses_csv(images_df, uploaded_licenses_file)
        st.dataframe(final_df.head())

        st.header("Download the processed CSV file")
        processed_csv = final_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=processed_csv,
            file_name='processed_images_with_licenses.csv',
            mime='text/csv',
        )
