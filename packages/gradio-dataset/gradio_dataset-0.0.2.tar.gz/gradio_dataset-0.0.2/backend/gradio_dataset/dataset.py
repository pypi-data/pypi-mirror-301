"""gr.Dataset() component."""

from __future__ import annotations

import warnings
from typing import Any, Literal, Sequence, List, Callable

from gradio_client.documentation import document
import gradio as gr
from gradio import processing_utils
from gradio.components.base import (
    Component,
    get_component_instance,
)
from gradio.events import Events, SelectData


class dataset(Component):
    """
    Creates a gallery or table to display data samples. This component is primarily designed for internal use to display examples.
    However, it can also be used directly to display a dataset and let users select examples.
    """

    EVENTS = [Events.click, Events.select]

    def __init__(
        self,
        *,
        label: str | None = None,
        components: Sequence[Component] | list[str] | None = None,
        component_props: list[dict[str, Any]] | None = None,
        samples: list[list[Any]] | None = None,
        headers: list[str] | None = None,
        type: Literal["values", "index", "tuple"] = "values",
        samples_per_page: int = 10,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        proxy_url: str | None = None,
        sample_labels: list[str] | None = None,
        menu_icon: str | None = None,
        menu_choices: list[str] | None = None,
        header_sort: bool = False,
        manual_sort: bool = False,
    ):
        """
        Parameters:
            label: The label for this component, appears above the component.
            components: Which component types to show in this dataset widget, can be passed in as a list of string names or Components instances. The following components are supported in a dataset: Audio, Checkbox, CheckboxGroup, ColorPicker, Dataframe, Dropdown, File, HTML, Image, Markdown, Model3D, Number, Radio, Slider, Textbox, TimeSeries, Video
            samples: a nested list of samples. Each sublist within the outer list represents a data sample, and each element within the sublist represents an value for each component
            headers: Column headers in the dataset widget, should be the same len as components. If not provided, inferred from component labels
            type: "values" if clicking on a sample should pass the value of the sample, "index" if it should pass the index of the sample, or "tuple" if it should pass both the index and the value of the sample.
            samples_per_page: how many examples to show per page.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            proxy_url: The URL of the external Space used to load this component. Set automatically when using `gr.load()`. This should not be set manually.
            sample_labels: A list of labels for each sample. If provided, the length of this list should be the same as the number of samples, and these labels will be used in the UI instead of rendering the sample values.
            menu_icon: The icon to use for the menu choices. If not provided, a default icon will be used.
            menu_choices: A list of menu choices to display in the action column. If provided, the length of this list should be the same as the number of samples, and these choices will be displayed in the action column.
            header_sort: If True, the dataset will be sortable by clicking on the headers. The `select` event will return the index of the column that was clicked and the sort order.
            manual_sort: If True, the dataset will be sortable by clicking on the headers, but the sorting will not be done automatically. The `select` event will return the index of the column that was clicked and the sort order.
        """
        super().__init__(
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
        )
        self.container = container
        self.scale = scale
        self.min_width = min_width
        self._components = [get_component_instance(c) for c in components or []]

        self.menu_icon = menu_icon
        self.menu_choices = menu_choices or []
        self.header_sort = header_sort
        self.sort_column = None
        self.sort_order = None
        self.manual_sort = manual_sort

        if component_props is None:
            self.component_props = [
                component.recover_kwargs(
                    component.get_config(),
                    ["value"],
                )
                for component in self._components
            ]
        else:
            self.component_props = component_props

        # Narrow type to Component
        if not all(isinstance(c, Component) for c in self._components):
            raise TypeError(
                "All components in a `dataset` must be subclasses of `Component`"
            )
        self._components = [c for c in self._components if isinstance(c, Component)]
        self.proxy_url = proxy_url
        for component in self._components:
            component.proxy_url = proxy_url
        self.raw_samples = [[]] if samples is None else samples
        self.samples: list[list] = []
        for example in self.raw_samples:
            self.samples.append([])
            for component, ex in zip(self._components, example):
                # If proxy_url is set, that means it is being loaded from an external Gradio app
                # which means that the example has already been processed.
                if self.proxy_url is None:
                    # We do not need to process examples if the Gradio app is being loaded from
                    # an external Space because the examples have already been processed. Also,
                    # the `as_example()` method has been renamed to `process_example()` but we
                    # use the previous name to be backwards-compatible with previously-created
                    # custom components
                    ex = component.as_example(ex)
                self.samples[-1].append(
                    processing_utils.move_files_to_cache(
                        ex, component, keep_in_cache=True
                    )
                )
        self.type = type
        self.label = label
        if headers is not None:
            self.headers = headers
        elif all(c.label is None for c in self._components):
            self.headers = []
        else:
            self.headers = [c.label or "" for c in self._components]
        self.samples_per_page = samples_per_page
        self.sample_labels = sample_labels

    def api_info(self) -> dict[str, str]:
        return {"type": "integer", "description": "index of selected example"}
    # def api_info(self) -> dict[str, Any]:
    #     return {
    #         "type": {
    #             "payload": "object",
    #             "properties": {
    #                 "index": {"type": "integer"},
    #                 "sort": {
    #                     "type": "object",
    #                     "properties": {
    #                         "column": {"type": "integer"},
    #                         "order": {
    #                             "type": "string",
    #                             "enum": ["ascending", "descending"],
    #                         },
    #                     },
    #                 },
    #             },
    #         },
    #         "description": "index of selected example or sorting information",
    #     }

    def get_config(self):
        config = super().get_config()

        config["components"] = []
        config["component_props"] = self.component_props
        config["sample_labels"] = self.sample_labels
        config["component_ids"] = []
        config["menu_icon"] = self.menu_icon
        config["menu_choices"] = self.menu_choices

        for component in self._components:
            config["components"].append(component.get_block_name())

            config["component_ids"].append(component._id)

        config["header_sort"] = self.header_sort
        config["manual_sort"] = self.manual_sort
        config["sort_column"] = self.sort_column
        config["sort_order"] = self.sort_order
        return config

    def sort_samples(self, column_index: int, order: str):
        if not self.header_sort or self.manual_sort:
            return

        self.sort_column = column_index
        self.sort_order = order

        def sort_key(sample):
            return sample[column_index]

        self.samples.sort(key=sort_key, reverse=(order == "descending"))

    def preprocess(self, payload: int | None) -> int | list | tuple[int, list] | None:
        """
        Parameters:
            payload: the index of the selected example in the dataset
        Returns:
            Passes the selected sample either as a `list` of data corresponding to each input component (if `type` is "value") or as an `int` index (if `type` is "index"), or as a `tuple` of the index and the data (if `type` is "tuple").
        """
        if isinstance(payload, dict) and "menu_choice" in payload:
            return {"index": payload["index"], "menu_choice": payload["menu_choice"]}
        # if "sort" in payload:
        #     self.sort_samples(payload["sort"]["column"], payload["sort"]["order"])
        #     if self.manual_sort:
        #         return {"index": payload["sort"]["column"], "value": payload["sort"]}
        #     return None
        elif "index" in payload:
            index = payload["index"]
            if self.type == "index":
                return index
            elif self.type == "values":
                return self.raw_samples[index]
            elif self.type == "tuple":
                return index, self.raw_samples[index]
        return None

    def postprocess(self, value: int | list | None) -> int | None:
        """
        Parameters:
            value: Expects an `int` index or `list` of sample data. Returns the index of the sample in the dataset or `None` if the sample is not found.
        Returns:
            Returns the index of the sample in the dataset.
        """
        if value is None or isinstance(value, int):
            return value
        if isinstance(value, list):
            try:
                index = self.samples.index(value)
            except ValueError:
                index = None
                warnings.warn(
                    "The `dataset` component does not support updating the dataset data by providing "
                    "a set of list values. Instead, you should return a new dataset(samples=...) object."
                )
            return index

    def example_payload(self) -> Any:
        return 0

    def example_value(self) -> Any:
        return []

    def select(
        self,
        fn: Callable,
        inputs: list[gr.components.Component] | None = None,
        outputs: list[gr.components.Component] | None = None,
        api_name: str | None = None,
        **kwargs,
    ) -> gr.EventListener:
        """
        Enhanced select event handler that handles both row clicks and menu selections.
        """
        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []

        def wrapped_fn(evt: SelectData | dict) -> Any:
            # Handle menu selection events
            if isinstance(evt, dict):
                if "menu_choice" in evt:
                    return fn(SelectData(evt["index"], evt["menu_choice"]))
                # elif "sort" in evt:
                #     # Handle sorting event
                #     if self.manual_sort:
                #         return fn(SelectData(target=self, data=evt["sort"]))
                #     self.sort_samples(evt["sort"]["column"], evt["sort"]["order"])
                #     return fn(SelectData(target=self, data=evt["sort"]))
                elif "index" in evt:
                    index = evt["index"]
                    if self.type == "index":
                        return fn(SelectData(target=self, data={"index": index, "value": index}))
                    elif self.type == "values":
                        return fn(SelectData(target=self, data={"index": index, "value": self.samples[index]}))
                    else:  # type == "tuple"
                        return fn(SelectData(target=self, data={"index": index, "value": (index, self.samples[index])}))

            # Handle any other select events
            return fn(evt)

        # Register both click and select events
        self.click(
            fn=wrapped_fn, inputs=inputs, outputs=outputs, api_name=api_name, **kwargs
        )
        return self.on(
            "select", wrapped_fn, inputs, outputs, api_name=api_name, **kwargs
        )