<script lang="ts">
  import "./styles.css";
  import { Block } from "@gradio/atoms";
  import type { SvelteComponent, ComponentType } from "svelte";
  import type { Gradio, SelectData } from "@gradio/utils";
  import { BaseExample } from "@gradio/textbox";
  export let components: string[];
  export let component_props: Record<string, any>[];
  export let component_map: Map<
    string,
    Promise<{
      default: ComponentType<SvelteComponent>;
    }>
  >;
  export let label = "Examples";
  export let headers: string[];
  export let samples: any[][] | null = null;
  let old_samples: any[][] | null = null;
  export let sample_labels: string[] | null = null;
  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;
  export let value: number | null = null;
  export let root: string;
  export let proxy_url: null | string;
  export let samples_per_page = 10;
  export let scale: number | null = null;
  export let min_width: number | undefined = undefined;
  export let menu_icon: string | null = null;
  export let menu_choices: string[] = [];
  export let header_sort = false;
  export let sort_column: number | null = null;
  export let sort_order: "ascending" | "descending" | null = null;
  export let manual_sort: boolean = false;
  export let gradio: Gradio<{
    click: number;
    select: SelectData;
  }>;

  $: default_menu_icon =
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/icons/three-dots-vertical.svg";

  // Although the `samples_dir` prop is not used in any of the core Gradio component, it is kept for backward compatibility
  // with any custom components created with gradio<=4.20.0
  let samples_dir: string = proxy_url
    ? `/proxy=${proxy_url}file=`
    : `${root}/file=`;
  let page = 0;

  $: gallery = components.length < 2 || sample_labels !== null;
  let paginate = samples ? samples.length > samples_per_page : false;

  let selected_samples: any[][];
  let page_count: number;
  let visible_pages: number[] = [];

  let current_hover = -1;
  let active_menu: number | null = null;

  function simplifyRowData(row: any[]): string[] {
    return row.map((item) => item.value);
  }

  function handle_mouseenter(i: number): void {
    current_hover = i;
  }

  function handle_mouseleave(): void {
    current_hover = -1;
    // Only close menu if mouse leaves the entire row
    setTimeout(() => {
      if (current_hover !== active_menu) {
        active_menu = null;
      }
    }, 100);
  }

  function handleSort(columnIndex: number) {
    if (!header_sort && !manual_sort) return;

    if (sort_column === columnIndex) {
      sort_order = sort_order === "ascending" ? "descending" : "ascending";
    } else {
      sort_column = columnIndex;
      sort_order = "ascending";
    }

    gradio.dispatch("select", {
      index: sort_column,
      value: { column: sort_column, order: sort_order },
    });
  }

  $: sortedSamples = samples ? [...samples] : [];
  $: {
    if (
      header_sort &&
      !manual_sort &&
      sort_column !== null &&
      sort_order !== null
    ) {
      sortedSamples.sort((a, b) => {
        const aValue = a[sort_column];
        const bValue = b[sort_column];
        if (aValue < bValue) return sort_order === "ascending" ? -1 : 1;
        if (aValue > bValue) return sort_order === "ascending" ? 1 : -1;
        return 0;
      });
    }
  }

  function handle_menu_click(
    index: number,
    menu_choice: string,
    event: MouseEvent
  ) {
    event.stopPropagation();
    const actualIndex = index + page * samples_per_page;
    gradio.dispatch("select", {
      index: actualIndex,
      value: { menu_choice },
      row_value: samples[actualIndex],
    });
    active_menu = null;
  }

  $: {
    if (sample_labels) {
      samples = sample_labels.map((e) => [e]);
    } else if (!samples) {
      samples = [];
    }
    if (samples !== old_samples) {
      page = 0;
      old_samples = samples;
    }
    paginate = samples.length > samples_per_page;
    if (paginate) {
      visible_pages = [];
      selected_samples = samples.slice(
        page * samples_per_page,
        (page + 1) * samples_per_page
      );
      page_count = Math.ceil(samples.length / samples_per_page);
      [0, page, page_count - 1].forEach((anchor) => {
        for (let i = anchor - 2; i <= anchor + 2; i++) {
          if (i >= 0 && i < page_count && !visible_pages.includes(i)) {
            if (
              visible_pages.length > 0 &&
              i - visible_pages[visible_pages.length - 1] > 1
            ) {
              visible_pages.push(-1);
            }
            visible_pages.push(i);
          }
        }
      });
    } else {
      selected_samples = samples.slice();
    }
  }

  let component_meta: {
    value: any;
    component: ComponentType<SvelteComponent>;
  }[][] = [];

  async function get_component_meta(selected_samples: any[][]): Promise<void> {
    component_meta = await Promise.all(
      selected_samples &&
        selected_samples.map(
          async (sample_row) =>
            await Promise.all(
              sample_row.map(async (sample_cell, j) => {
                return {
                  value: sample_cell,
                  component: (await component_map.get(components[j]))
                    ?.default as ComponentType<SvelteComponent>,
                };
              })
            )
        )
    );
  }

  $: component_map,
    get_component_meta(
      sortedSamples.slice(
        page * samples_per_page,
        (page + 1) * samples_per_page
      )
    );
</script>

<Block
  {visible}
  padding={false}
  {elem_id}
  {elem_classes}
  {scale}
  {min_width}
  allow_overflow={false}
  container={false}
>
  <div class="label">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      aria-hidden="true"
      role="img"
      width="1em"
      height="1em"
      preserveAspectRatio="xMidYMid meet"
      viewBox="0 0 32 32"
    >
      <path
        fill="currentColor"
        d="M10 6h18v2H10zm0 18h18v2H10zm0-9h18v2H10zm-6 0h2v2H4zm0-9h2v2H4zm0 18h2v2H4z"
      />
    </svg>
    {label}
  </div>
  {#if gallery}
    <div class="gallery">
      {#each selected_samples as sample_row, i}
        {#if sample_row[0]}
          <button
            class="gallery-item"
            on:click={() => {
              value = i + page * samples_per_page;
              gradio.dispatch("click", value);
              gradio.dispatch("select", {
                index: value,
                value: sample_row,
              });
            }}
            on:mouseenter={() => handle_mouseenter(i)}
            on:mouseleave={() => handle_mouseleave()}
          >
            {#if sample_labels}
              <BaseExample
                value={sample_row[0]}
                selected={current_hover === i}
                type="gallery"
              />
            {:else if component_meta.length && component_map.get(components[0])}
              <svelte:component
                this={component_meta[0][0].component}
                {...component_props[0]}
                value={sample_row[0]}
                {samples_dir}
                type="gallery"
                selected={current_hover === i}
                index={i}
                {root}
              />
            {/if}
          </button>
        {/if}
      {/each}
    </div>
  {:else}
    <div class="table-wrap">
      <table tabindex="0" role="grid">
        <thead>
          <tr class="tr-head">
            {#each headers as header, index}
              <th>
                {#if header_sort || manual_sort}
                  <button
                    on:click={() => handleSort(index)}
                    class="sort-button"
                  >
                    {header}
                    {#if sort_column === index}
                      <span class="sort-icon">
                        {sort_order === "ascending" ? "▲" : "▼"}
                      </span>
                    {/if}
                  </button>
                {:else}
                  {header}
                {/if}
              </th>
            {/each}
            {#if menu_choices.length > 0}
              <th>Actions</th>
            {/if}
          </tr>
        </thead>
        <tbody>
          {#each component_meta as sample_row, i}
            <tr class="tr-body">
              {#each sample_row as { value, component }, j}
                {@const component_name = components[j]}
                {#if component_name !== undefined && component_map.get(component_name) !== undefined}
                  <td
                    style="max-width: {component_name === 'textbox'
                      ? '35ch'
                      : 'auto'}"
                    class={component_name}
                    on:click={() => {
                      gradio.dispatch("click", value);
                      gradio.dispatch("select", {
                        index: [i, j],
                        value: value,
                        row_value: simplifyRowData(sample_row),
                      });
                    }}
                    on:mouseenter={() => handle_mouseenter(i)}
                    on:mouseleave={() => handle_mouseleave()}
                  >
                    <svelte:component
                      this={component}
                      {...component_props[j]}
                      {value}
                      {samples_dir}
                      type="table"
                      selected={current_hover === i}
                      index={i}
                      {root}
                    />
                  </td>
                {/if}
              {/each}

              {#if menu_choices?.length > 0}
                <td class="menu-cell">
                  <button
                    class="menu-button"
                    on:click|stopPropagation={() =>
                      (active_menu = active_menu === i ? null : i)}
                  >
                    <img
                      src={menu_icon ? menu_icon : default_menu_icon}
                      alt="Menu"
                      class="menu-icon"
                      style="transform: {menu_icon ? 'none' : 'rotate(90deg)'}"
                    />
                  </button>

                  {#if active_menu === i}
                    <div
                      class={`menu-popup ${component_meta.length - 1 === i ? "last-item" : ""}`}
                    >
                      {#each menu_choices as choice}
                        <button
                          class="menu-item"
                          on:click={(e) => handle_menu_click(i, choice, e)}
                        >
                          {choice}
                        </button>
                      {/each}
                    </div>
                  {/if}
                </td>
              {/if}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
  {#if paginate}
    <div class="paginate">
      Pages:
      {#each visible_pages as visible_page}
        {#if visible_page === -1}
          <div>...</div>
        {:else}
          <button
            class:current-page={page === visible_page}
            on:click={() => (page = visible_page)}
          >
            {visible_page + 1}
          </button>
        {/if}
      {/each}
    </div>
  {/if}
</Block>

<style>
  .wrap {
    display: inline-block;
    width: var(--size-full);
    max-width: var(--size-full);
    color: var(--body-text-color);
    background: violet;
  }

  .hide {
    display: none;
  }

  .label {
    display: flex;
    align-items: center;
    margin-bottom: var(--size-2);
    color: var(--block-label-text-color);
    font-weight: var(--block-label-text-weight);
    font-size: var(--block-label-text-size);
    line-height: var(--line-sm);
  }

  svg {
    margin-right: var(--size-1);
  }

  .gallery {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-lg);
  }

  .gallery-item {
    border: 1px solid var(--border-color-primary);
    border-radius: var(--button-large-radius);
    overflow: hidden;
  }

  .gallery-item:hover {
    border-color: var(--border-color-accent);
    background: var(--table-row-focus);
  }

  .table-wrap {
    border: 1px solid var(--border-color-primary);
    border-radius: var(--table-radius);
    width: var(--size-full);
    table-layout: auto;
    overflow-x: auto;
    line-height: var(--line-sm);
    color: var(--table-text-color);
  }

  table {
    width: var(--size-full);
  }

  .tr-head {
    box-shadow: var(--shadow-drop-lg);
    border-bottom: 1px solid var(--border-color-primary);
  }

  .tr-head > * + * {
    border-right-width: 0px;
    border-left-width: 1px;
    border-color: var(--border-color-primary);
  }

  th {
    padding: var(--size-2);
    white-space: nowrap;
  }

  .tr-body {
    cursor: pointer;
    border-bottom: 1px solid var(--border-color-primary);
    background: var(--table-even-background-fill);
  }

  .tr-body:last-child {
    border: none;
  }

  .tr-body:nth-child(odd) {
    background: var(--table-odd-background-fill);
  }

  .tr-body:hover {
    background: var(--table-row-focus);
  }

  .tr-body > * + * {
    border-right-width: 0px;
    border-left-width: 1px;
    border-color: var(--border-color-primary);
  }

  .tr-body:hover > * + * {
    border-color: var(--border-color-accent);
  }

  td {
    padding: var(--size-2);
    text-align: center;
  }

  .paginate {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--spacing-sm);
    margin-top: var(--size-2);
    color: var(--block-label-text-color);
    font-size: var(--text-sm);
  }

  button.current-page {
    font-weight: var(--weight-bold);
  }

  .menu-cell {
    position: relative;
    width: 40px;
    padding: var(--size-2);
  }

  .menu-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 2px;
    border-radius: 4px;
  }

  .menu-button:hover {
    background: var(--color-accent-soft);
  }

  .menu-icon {
    width: 20px;
    height: 20px;
    display: block;
  }

  .menu-popup {
    position: absolute;
    right: 75%;
    top: 50%;
    transform: translateY(-50%);
    background: var(--background-fill-primary);
    border: 1px solid var(--border-color-primary);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-drop-lg);
    z-index: 1000;
    min-width: 100px;
    width: max-content;
    padding: 4px 8px;
  }

  .menu-popup.last-item {
    top: unset;
    bottom: 0;
    transform: unset;
  }

  .menu-item {
    display: block;
    width: 100%;
    padding: var(--size-1) var(--size-2);
    text-align: left;
    background: none;
    border: none;
    cursor: pointer;
    background-size: 0 100%;
    background-repeat: no-repeat;
    transition: all 0.4s;
  }

  .menu-item:hover {
    background-image: linear-gradient(to right, #fff3eb, #fff3eb);
    background-repeat: no-repeat;
    background-size: 100% 100%;
    transition: all 0.4s;
  }

  .menu-item + .menu-item {
    border-top: 1px solid var(--border-color-primary);
  }

  .sort-button {
    background: none;
    border: none;
    cursor: pointer;
    font-weight: inherit;
    color: inherit;
    padding: 0;
    width: 100%;
    position: relative; /* Add this */
    display: flex;
    justify-content: center;
  }

  /* Add a wrapper for the header text */
  .header-text {
    text-align: center;
  }

  /* Style for the sort icon */
  .sort-icon {
    position: absolute; /* Add this */
    right: 0; /* Add this */
    top: 50%; /* Add this */
    transform: translateY(-50%); /* Add this */
    margin-left: 0.5em;
  }
</style>
