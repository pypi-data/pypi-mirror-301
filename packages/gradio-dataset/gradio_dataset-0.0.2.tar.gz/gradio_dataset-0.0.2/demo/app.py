import gradio as gr
from gradio_dataset import dataset
from gradio_modal_component import modal_component


# Initialize a three-column dataset for testing
def init_ds_three_col():
    ds = [
        [
            "Text 1",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 1",
        ],
        [
            "Text 2",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 2",
        ],
        [
            "Text 3",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 3",
        ],
        [
            "Text 4",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 4",
        ],
        [
            "Text 5",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 5",
        ],
    ]
    return ds


# Function to handle selection
def get_selection(evt: gr.SelectData):
    print("Selection Event Triggered")
    print(f"Index: {evt.index}")
    print(f"Value: {evt.value}")
    print(f"RowData: {evt.row_value}")
    try:
        # Check the action taken and display the modal accordingly
        if isinstance(evt.value, dict):
            if evt.value["menu_choice"] == "View Profile":
                # Display the modal with the selected value
                content = f"""
                    # View Profile
                    - You are viewing the profile number `{evt.index}`
                    - Profile content:
                        - {evt.row_value}"""
                return gr.update(visible=True), content
            if evt.value["menu_choice"] == "Edit":
                # Display the modal with the selected value
                content = f"""
                    # Edit Profile
                    - You are editting the profile number `{evt.index}`
                    - Profile content:
                        - {evt.row_value}"""
                return gr.update(visible=True), content
    except Exception as e:
        pass

    # Return to hide the modal
    return gr.update(visible=False), ""


with gr.Blocks() as demo:
    # Modal that shows the content dynamically based on user selection
    with modal_component(
        visible=False, width=500, height=300, bg_blur=0
    ) as profileModal:
        modal_text = gr.Markdown(f"")

    gr.Markdown("""
                # Dataset Component
                - Trigger click envents, this will tracking and return (check log in terminal):
                    - `evt.index`: **list[row, col]** - index of the selected cell
                    - `evt.value`: **str** - The selected cell value
                    - `evt.row_value`: **list[str]** - The selected row value by this you can get the value of a specific column by `evt.row_value[col]`

                - Action column:
                    - `menu_choice`: **list[str]** - Modify the menu choices to add the action column
                    - `menu_icon`: **str** - Add the icon to the menu choices, if not there will be a default icon
                    - When user select the action, it will trigger an event:
                        - `evt.index`: **str** - index of the selected row
                        - `evt.value`: **dict{"menu_choice": "action"}** - The selected action value
                        - `evt.row_value`: **list[str]** - The selected row value

                - Header Sort:
                    - `header_sort`: **bool** - Enable the header sort
                        - This will sort the dataset based on the header column at UI level, however this event will be trigger
                        - `evt.index`: **str** - index of the selected Col
                        - `evt.value`: **dict{"columns": col, "order": "descending" | "ascending"}** - Column and order of the sort
                - Manual Sort:
                    - `manual_sort`: **bool** - Enable the manual sort
                    - This will enable sort icon on UI and sort event only (for trigger purpose), User will have to tracking the event and sort the dataset manually
                ## Test case 1:
                - `menu_icon`: not set
                - `header_sort`: True
                """)
    # Define the three-column dataset
    three_col_ds = dataset(
        components=[
            gr.Textbox(visible=False, interactive=True),
            gr.HTML(visible=False),
            gr.Textbox(visible=False, interactive=True),  # Added third column
        ],
        headers=[
            "Textbox",
            "Image",
            "Description",
        ],  # Updated headers for three columns
        label="Test Case 1",
        samples=init_ds_three_col(),  # Use the new three-column dataset
        menu_choices=["View Profile", "Edit", "Delete"],
        # menu_icon="https://cdn-icons-png.flaticon.com/512/18/18659.png",
        header_sort=True,
        # manual_sort=True,
    )

    # Set the select event to update modal visibility and content
    three_col_ds.select(
        fn=get_selection, inputs=None, outputs=[profileModal, modal_text]
    )

    ## Test Case 2
    gr.Markdown("""
                # Test case 2
                - `menu_icon`: enable
                - `manual_sort`: True
                """)
    # Define the three-column dataset
    three_col_ds2 = dataset(
        components=[
            gr.Textbox(visible=False, interactive=True),
            gr.HTML(visible=False),
            gr.Textbox(visible=False, interactive=True),  # Added third column
        ],
        headers=[
            "Textbox",
            "Image",
            "Description",
        ],  # Updated headers for three columns
        label="Test Case 2",
        samples=init_ds_three_col(),  # Use the new three-column dataset
        menu_choices=["View Profile", "Edit", "Delete"],
        menu_icon="https://cdn-icons-png.flaticon.com/512/18/18659.png",
        # header_sort=True,
        manual_sort=True,
    )

    # Set the select event to update modal visibility and content
    three_col_ds2.select(
        fn=get_selection, inputs=None, outputs=[profileModal, modal_text]
    )


if __name__ == "__main__":
    demo.launch()
