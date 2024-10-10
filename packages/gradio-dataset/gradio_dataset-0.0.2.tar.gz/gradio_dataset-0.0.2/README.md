---
tags: [gradio-custom-component, Dataset]
title: gradio_dataset
short_description: A gradio custom component
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_dataset`
<a href="https://pypi.org/project/gradio_dataset/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_dataset"></a>  

Python library for easily interacting with trained machine learning models

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

```

## `dataset`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The label for this component, appears above the component.</td>
</tr>

<tr>
<td align="left"><code>components</code></td>
<td align="left" style="width: 25%;">

```python
Sequence[gradio.components.base.Component]
    | list[str]
    | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Which component types to show in this dataset widget, can be passed in as a list of string names or Components instances. The following components are supported in a dataset: Audio, Checkbox, CheckboxGroup, ColorPicker, Dataframe, Dropdown, File, HTML, Image, Markdown, Model3D, Number, Radio, Slider, Textbox, TimeSeries, Video</td>
</tr>

<tr>
<td align="left"><code>component_props</code></td>
<td align="left" style="width: 25%;">

```python
list[dict[str, Any]] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>samples</code></td>
<td align="left" style="width: 25%;">

```python
list[list[Any]] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">a nested list of samples. Each sublist within the outer list represents a data sample, and each element within the sublist represents an value for each component</td>
</tr>

<tr>
<td align="left"><code>headers</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Column headers in the dataset widget, should be the same len as components. If not provided, inferred from component labels</td>
</tr>

<tr>
<td align="left"><code>type</code></td>
<td align="left" style="width: 25%;">

```python
"values" | "index" | "tuple"
```

</td>
<td align="left"><code>"values"</code></td>
<td align="left">"values" if clicking on a sample should pass the value of the sample, "index" if it should pass the index of the sample, or "tuple" if it should pass both the index and the value of the sample.</td>
</tr>

<tr>
<td align="left"><code>samples_per_page</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>10</code></td>
<td align="left">how many examples to show per page.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will place the component in a container - providing some extra padding around the border.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>proxy_url</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The URL of the external Space used to load this component. Set automatically when using `gr.load()`. This should not be set manually.</td>
</tr>

<tr>
<td align="left"><code>sample_labels</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A list of labels for each sample. If provided, the length of this list should be the same as the number of samples, and these labels will be used in the UI instead of rendering the sample values.</td>
</tr>

<tr>
<td align="left"><code>menu_icon</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The icon to use for the menu choices. If not provided, a default icon will be used.</td>
</tr>

<tr>
<td align="left"><code>menu_choices</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A list of menu choices to display in the action column. If provided, the length of this list should be the same as the number of samples, and these choices will be displayed in the action column.</td>
</tr>

<tr>
<td align="left"><code>header_sort</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True, the dataset will be sortable by clicking on the headers. The `select` event will return the index of the column that was clicked and the sort order.</td>
</tr>

<tr>
<td align="left"><code>manual_sort</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If True, the dataset will be sortable by clicking on the headers, but the sorting will not be done automatically. The `select` event will return the index of the column that was clicked and the sort order.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `click` | Triggered when the dataset is clicked. |
| `select` | Event listener for when the user selects or deselects the dataset. Uses event data gradio.SelectData to carry `value` referring to the label of the dataset, and `selected` to refer to state of the dataset. See EventData documentation on how to use this event data |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, passes the selected sample either as a `list` of data corresponding to each input component (if `type` is "value") or as an `int` index (if `type` is "index"), or as a `tuple` of the index and the data (if `type` is "tuple").
- **As input:** Should return, expects an `int` index or `list` of sample data. Returns the index of the sample in the dataset or `None` if the sample is not found.

 ```python
 def predict(
     value: int | list | tuple[int, list] | None
 ) -> int | list | None:
     return value
 ```
 
