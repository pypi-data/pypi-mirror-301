
import gradio as gr
from app import demo as app
import os

_docs = {'dataset': {'description': 'Creates a gallery or table to display data samples. This component is primarily designed for internal use to display examples.\nHowever, it can also be used directly to display a dataset and let users select examples.', 'members': {'__init__': {'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component, appears above the component.'}, 'components': {'type': 'Sequence[gradio.components.base.Component]\n    | list[str]\n    | None', 'default': 'None', 'description': 'Which component types to show in this dataset widget, can be passed in as a list of string names or Components instances. The following components are supported in a dataset: Audio, Checkbox, CheckboxGroup, ColorPicker, Dataframe, Dropdown, File, HTML, Image, Markdown, Model3D, Number, Radio, Slider, Textbox, TimeSeries, Video'}, 'component_props': {'type': 'list[dict[str, Any]] | None', 'default': 'None', 'description': None}, 'samples': {'type': 'list[list[Any]] | None', 'default': 'None', 'description': 'a nested list of samples. Each sublist within the outer list represents a data sample, and each element within the sublist represents an value for each component'}, 'headers': {'type': 'list[str] | None', 'default': 'None', 'description': 'Column headers in the dataset widget, should be the same len as components. If not provided, inferred from component labels'}, 'type': {'type': '"values" | "index" | "tuple"', 'default': '"values"', 'description': '"values" if clicking on a sample should pass the value of the sample, "index" if it should pass the index of the sample, or "tuple" if it should pass both the index and the value of the sample.'}, 'samples_per_page': {'type': 'int', 'default': '10', 'description': 'how many examples to show per page.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'proxy_url': {'type': 'str | None', 'default': 'None', 'description': 'The URL of the external Space used to load this component. Set automatically when using `gr.load()`. This should not be set manually.'}, 'sample_labels': {'type': 'list[str] | None', 'default': 'None', 'description': 'A list of labels for each sample. If provided, the length of this list should be the same as the number of samples, and these labels will be used in the UI instead of rendering the sample values.'}, 'menu_icon': {'type': 'str | None', 'default': 'None', 'description': 'The icon to use for the menu choices. If not provided, a default icon will be used.'}, 'menu_choices': {'type': 'list[str] | None', 'default': 'None', 'description': 'A list of menu choices to display in the action column. If provided, the length of this list should be the same as the number of samples, and these choices will be displayed in the action column.'}, 'header_sort': {'type': 'bool', 'default': 'False', 'description': 'If True, the dataset will be sortable by clicking on the headers. The `select` event will return the index of the column that was clicked and the sort order.'}, 'manual_sort': {'type': 'bool', 'default': 'False', 'description': 'If True, the dataset will be sortable by clicking on the headers, but the sorting will not be done automatically. The `select` event will return the index of the column that was clicked and the sort order.'}}, 'postprocess': {'value': {'type': 'int | list | None', 'description': 'Expects an `int` index or `list` of sample data. Returns the index of the sample in the dataset or `None` if the sample is not found.'}}, 'preprocess': {'return': {'type': 'int | list | tuple[int, list] | None', 'description': 'Passes the selected sample either as a `list` of data corresponding to each input component (if `type` is "value") or as an `int` index (if `type` is "index"), or as a `tuple` of the index and the data (if `type` is "tuple").'}, 'value': None}}, 'events': {'click': {'type': None, 'default': None, 'description': 'Triggered when the dataset is clicked.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the dataset. Uses event data gradio.SelectData to carry `value` referring to the label of the dataset, and `selected` to refer to state of the dataset. See EventData documentation on how to use this event data'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'dataset': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_dataset`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_dataset/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_dataset"></a>  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_dataset
```

## Usage

```python
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
                content = f\"\"\"
                    # View Profile
                    - You are viewing the profile number `{evt.index}`
                    - Profile content:
                        - {evt.row_value}\"\"\"
                return gr.update(visible=True), content
            if evt.value["menu_choice"] == "Edit":
                # Display the modal with the selected value
                content = f\"\"\"
                    # Edit Profile
                    - You are editting the profile number `{evt.index}`
                    - Profile content:
                        - {evt.row_value}\"\"\"
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

    gr.Markdown(\"\"\"
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
                \"\"\")
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
    gr.Markdown(\"\"\"
                # Test case 2
                - `menu_icon`: enable
                - `manual_sort`: True
                \"\"\")
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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `dataset`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["dataset"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["dataset"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the selected sample either as a `list` of data corresponding to each input component (if `type` is "value") or as an `int` index (if `type` is "index"), or as a `tuple` of the index and the data (if `type` is "tuple").
- **As output:** Should return, expects an `int` index or `list` of sample data. Returns the index of the sample in the dataset or `None` if the sample is not found.

 ```python
def predict(
    value: int | list | tuple[int, list] | None
) -> int | list | None:
    return value
```
""", elem_classes=["md-custom", "dataset-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          dataset: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
