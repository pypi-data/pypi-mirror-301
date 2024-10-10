const {
  SvelteComponent: hl,
  assign: bl,
  create_slot: gl,
  detach: vl,
  element: kl,
  get_all_dirty_from_scope: wl,
  get_slot_changes: pl,
  get_spread_update: yl,
  init: zl,
  insert: Cl,
  safe_not_equal: Sl,
  set_dynamic_element_data: He,
  set_style: E,
  toggle_class: D,
  transition_in: xe,
  transition_out: $e,
  update_slot_base: ql
} = window.__gradio__svelte__internal;
function Hl(n) {
  let e, l, t;
  const f = (
    /*#slots*/
    n[18].default
  ), i = gl(
    f,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: l = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], a = {};
  for (let o = 0; o < s.length; o += 1)
    a = bl(a, s[o]);
  return {
    c() {
      e = kl(
        /*tag*/
        n[14]
      ), i && i.c(), He(
        /*tag*/
        n[14]
      )(e, a), D(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), D(
        e,
        "padded",
        /*padding*/
        n[6]
      ), D(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), D(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), D(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), E(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), E(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), E(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), E(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), E(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), E(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), E(e, "border-width", "var(--block-border-width)");
    },
    m(o, c) {
      Cl(o, e, c), i && i.m(e, null), t = !0;
    },
    p(o, c) {
      i && i.p && (!t || c & /*$$scope*/
      131072) && ql(
        i,
        f,
        o,
        /*$$scope*/
        o[17],
        t ? pl(
          f,
          /*$$scope*/
          o[17],
          c,
          null
        ) : wl(
          /*$$scope*/
          o[17]
        ),
        null
      ), He(
        /*tag*/
        o[14]
      )(e, a = yl(s, [
        (!t || c & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!t || c & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!t || c & /*elem_classes*/
        8 && l !== (l = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-nl1om8")) && { class: l }
      ])), D(
        e,
        "hidden",
        /*visible*/
        o[10] === !1
      ), D(
        e,
        "padded",
        /*padding*/
        o[6]
      ), D(
        e,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), D(
        e,
        "border_contrast",
        /*border_mode*/
        o[5] === "contrast"
      ), D(e, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), c & /*height*/
      1 && E(
        e,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), c & /*width*/
      2 && E(e, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), c & /*variant*/
      16 && E(
        e,
        "border-style",
        /*variant*/
        o[4]
      ), c & /*allow_overflow*/
      2048 && E(
        e,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), c & /*scale*/
      4096 && E(
        e,
        "flex-grow",
        /*scale*/
        o[12]
      ), c & /*min_width*/
      8192 && E(e, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      t || (xe(i, o), t = !0);
    },
    o(o) {
      $e(i, o), t = !1;
    },
    d(o) {
      o && vl(e), i && i.d(o);
    }
  };
}
function Ml(n) {
  let e, l = (
    /*tag*/
    n[14] && Hl(n)
  );
  return {
    c() {
      l && l.c();
    },
    m(t, f) {
      l && l.m(t, f), e = !0;
    },
    p(t, [f]) {
      /*tag*/
      t[14] && l.p(t, f);
    },
    i(t) {
      e || (xe(l, t), e = !0);
    },
    o(t) {
      $e(l, t), e = !1;
    },
    d(t) {
      l && l.d(t);
    }
  };
}
function Nl(n, e, l) {
  let { $$slots: t = {}, $$scope: f } = e, { height: i = void 0 } = e, { width: s = void 0 } = e, { elem_id: a = "" } = e, { elem_classes: o = [] } = e, { variant: c = "solid" } = e, { border_mode: _ = "base" } = e, { padding: m = !0 } = e, { type: h = "normal" } = e, { test_id: u = void 0 } = e, { explicit_call: k = !1 } = e, { container: d = !0 } = e, { visible: g = !0 } = e, { allow_overflow: b = !0 } = e, { scale: M = null } = e, { min_width: L = 0 } = e, O = h === "fieldset" ? "fieldset" : "div";
  const B = (v) => {
    if (v !== void 0) {
      if (typeof v == "number")
        return v + "px";
      if (typeof v == "string")
        return v;
    }
  };
  return n.$$set = (v) => {
    "height" in v && l(0, i = v.height), "width" in v && l(1, s = v.width), "elem_id" in v && l(2, a = v.elem_id), "elem_classes" in v && l(3, o = v.elem_classes), "variant" in v && l(4, c = v.variant), "border_mode" in v && l(5, _ = v.border_mode), "padding" in v && l(6, m = v.padding), "type" in v && l(16, h = v.type), "test_id" in v && l(7, u = v.test_id), "explicit_call" in v && l(8, k = v.explicit_call), "container" in v && l(9, d = v.container), "visible" in v && l(10, g = v.visible), "allow_overflow" in v && l(11, b = v.allow_overflow), "scale" in v && l(12, M = v.scale), "min_width" in v && l(13, L = v.min_width), "$$scope" in v && l(17, f = v.$$scope);
  }, [
    i,
    s,
    a,
    o,
    c,
    _,
    m,
    u,
    k,
    d,
    g,
    b,
    M,
    L,
    O,
    B,
    h,
    f,
    t
  ];
}
class jl extends hl {
  constructor(e) {
    super(), zl(this, e, Nl, Ml, Sl, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const Bl = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Me = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Bl.reduce(
  (n, { color: e, primary: l, secondary: t }) => ({
    ...n,
    [e]: {
      primary: Me[e][l],
      secondary: Me[e][t]
    }
  }),
  {}
);
const {
  SvelteComponent: El,
  add_iframe_resize_listener: Al,
  add_render_callback: Rl,
  append: Vl,
  attr: Dl,
  binding_callbacks: Il,
  detach: Pl,
  element: Tl,
  init: Wl,
  insert: Yl,
  noop: Ne,
  safe_not_equal: Fl,
  set_data: Gl,
  text: Jl,
  toggle_class: U
} = window.__gradio__svelte__internal, { onMount: Kl } = window.__gradio__svelte__internal;
function Ll(n) {
  let e, l = (
    /*value*/
    (n[0] ? (
      /*value*/
      n[0]
    ) : "") + ""
  ), t, f;
  return {
    c() {
      e = Tl("div"), t = Jl(l), Dl(e, "class", "svelte-84cxb8"), Rl(() => (
        /*div_elementresize_handler*/
        n[5].call(e)
      )), U(
        e,
        "table",
        /*type*/
        n[1] === "table"
      ), U(
        e,
        "gallery",
        /*type*/
        n[1] === "gallery"
      ), U(
        e,
        "selected",
        /*selected*/
        n[2]
      );
    },
    m(i, s) {
      Yl(i, e, s), Vl(e, t), f = Al(
        e,
        /*div_elementresize_handler*/
        n[5].bind(e)
      ), n[6](e);
    },
    p(i, [s]) {
      s & /*value*/
      1 && l !== (l = /*value*/
      (i[0] ? (
        /*value*/
        i[0]
      ) : "") + "") && Gl(t, l), s & /*type*/
      2 && U(
        e,
        "table",
        /*type*/
        i[1] === "table"
      ), s & /*type*/
      2 && U(
        e,
        "gallery",
        /*type*/
        i[1] === "gallery"
      ), s & /*selected*/
      4 && U(
        e,
        "selected",
        /*selected*/
        i[2]
      );
    },
    i: Ne,
    o: Ne,
    d(i) {
      i && Pl(e), f(), n[6](null);
    }
  };
}
function Ol(n, e, l) {
  let { value: t } = e, { type: f } = e, { selected: i = !1 } = e, s, a;
  function o(m, h) {
    !m || !h || (a.style.setProperty("--local-text-width", `${h < 150 ? h : 200}px`), l(4, a.style.whiteSpace = "unset", a));
  }
  Kl(() => {
    o(a, s);
  });
  function c() {
    s = this.clientWidth, l(3, s);
  }
  function _(m) {
    Il[m ? "unshift" : "push"](() => {
      a = m, l(4, a);
    });
  }
  return n.$$set = (m) => {
    "value" in m && l(0, t = m.value), "type" in m && l(1, f = m.type), "selected" in m && l(2, i = m.selected);
  }, [t, f, i, s, a, c, _];
}
class Ql extends El {
  constructor(e) {
    super(), Wl(this, e, Ol, Ll, Fl, { value: 0, type: 1, selected: 2 });
  }
}
const {
  SvelteComponent: Ul,
  append: y,
  assign: ce,
  attr: w,
  check_outros: W,
  construct_svelte_component: re,
  create_component: X,
  destroy_component: Z,
  destroy_each: x,
  detach: z,
  element: S,
  empty: te,
  ensure_array_like: A,
  get_spread_object: _e,
  get_spread_update: ue,
  group_outros: Y,
  init: Xl,
  insert: C,
  listen: I,
  mount_component: $,
  noop: Zl,
  null_to_empty: de,
  run_all: el,
  safe_not_equal: xl,
  set_data: ee,
  set_style: me,
  space: R,
  src_url_equal: je,
  stop_propagation: $l,
  svg_element: Be,
  text: K,
  toggle_class: Ee,
  transition_in: p,
  transition_out: H
} = window.__gradio__svelte__internal;
function Ae(n, e, l) {
  const t = n.slice();
  return t[52] = e[l], t;
}
function Re(n, e, l) {
  const t = n.slice();
  return t[55] = e[l], t[57] = l, t;
}
function Ve(n, e, l) {
  const t = n.slice();
  return t[59] = e[l], t;
}
function De(n, e, l) {
  const t = n.slice();
  t[2] = e[l].value, t[62] = e[l].component, t[65] = l;
  const f = (
    /*components*/
    t[3][
      /*j*/
      t[65]
    ]
  );
  return t[63] = f, t;
}
function Ie(n, e, l) {
  const t = n.slice();
  return t[66] = e[l], t[68] = l, t;
}
function Pe(n, e, l) {
  const t = n.slice();
  return t[55] = e[l], t[57] = l, t;
}
function en(n) {
  let e, l, t, f, i, s, a, o, c = A(
    /*headers*/
    n[7]
  ), _ = [];
  for (let d = 0; d < c.length; d += 1)
    _[d] = We(Ie(n, c, d));
  let m = (
    /*menu_choices*/
    n[17].length > 0 && Ye()
  ), h = A(
    /*component_meta*/
    n[27]
  ), u = [];
  for (let d = 0; d < h.length; d += 1)
    u[d] = Oe(Re(n, h, d));
  const k = (d) => H(u[d], 1, 1, () => {
    u[d] = null;
  });
  return {
    c() {
      e = S("div"), l = S("table"), t = S("thead"), f = S("tr");
      for (let d = 0; d < _.length; d += 1)
        _[d].c();
      i = R(), m && m.c(), s = R(), a = S("tbody");
      for (let d = 0; d < u.length; d += 1)
        u[d].c();
      w(f, "class", "tr-head svelte-18m81hv"), w(l, "tabindex", "0"), w(l, "role", "grid"), w(l, "class", "svelte-18m81hv"), w(e, "class", "table-wrap svelte-18m81hv");
    },
    m(d, g) {
      C(d, e, g), y(e, l), y(l, t), y(t, f);
      for (let b = 0; b < _.length; b += 1)
        _[b] && _[b].m(f, null);
      y(f, i), m && m.m(f, null), y(l, s), y(l, a);
      for (let b = 0; b < u.length; b += 1)
        u[b] && u[b].m(a, null);
      o = !0;
    },
    p(d, g) {
      if (g[0] & /*sort_order, sort_column, headers, header_sort, manual_sort*/
      786563 | g[1] & /*handleSort*/
      4) {
        c = A(
          /*headers*/
          d[7]
        );
        let b;
        for (b = 0; b < c.length; b += 1) {
          const M = Ie(d, c, b);
          _[b] ? _[b].p(M, g) : (_[b] = We(M), _[b].c(), _[b].m(f, i));
        }
        for (; b < _.length; b += 1)
          _[b].d(1);
        _.length = c.length;
      }
      if (/*menu_choices*/
      d[17].length > 0 ? m || (m = Ye(), m.c(), m.m(f, null)) : m && (m.d(1), m = null), g[0] & /*component_meta, menu_choices, active_menu, menu_icon, default_menu_icon, components, gradio, component_props, samples_dir, current_hover, root, component_map*/
      1846743096 | g[1] & /*handle_menu_click, handle_mouseenter, handle_mouseleave*/
      11) {
        h = A(
          /*component_meta*/
          d[27]
        );
        let b;
        for (b = 0; b < h.length; b += 1) {
          const M = Re(d, h, b);
          u[b] ? (u[b].p(M, g), p(u[b], 1)) : (u[b] = Oe(M), u[b].c(), p(u[b], 1), u[b].m(a, null));
        }
        for (Y(), b = h.length; b < u.length; b += 1)
          k(b);
        W();
      }
    },
    i(d) {
      if (!o) {
        for (let g = 0; g < h.length; g += 1)
          p(u[g]);
        o = !0;
      }
    },
    o(d) {
      u = u.filter(Boolean);
      for (let g = 0; g < u.length; g += 1)
        H(u[g]);
      o = !1;
    },
    d(d) {
      d && z(e), x(_, d), m && m.d(), x(u, d);
    }
  };
}
function ln(n) {
  let e, l, t = A(
    /*selected_samples*/
    n[24]
  ), f = [];
  for (let s = 0; s < t.length; s += 1)
    f[s] = Ue(Pe(n, t, s));
  const i = (s) => H(f[s], 1, 1, () => {
    f[s] = null;
  });
  return {
    c() {
      e = S("div");
      for (let s = 0; s < f.length; s += 1)
        f[s].c();
      w(e, "class", "gallery svelte-18m81hv");
    },
    m(s, a) {
      C(s, e, a);
      for (let o = 0; o < f.length; o += 1)
        f[o] && f[o].m(e, null);
      l = !0;
    },
    p(s, a) {
      if (a[0] & /*value, page, samples_per_page, gradio, selected_samples, current_hover, sample_labels, component_meta, component_props, samples_dir, root, component_map, components*/
      1261449532 | a[1] & /*handle_mouseenter, handle_mouseleave*/
      3) {
        t = A(
          /*selected_samples*/
          s[24]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const c = Pe(s, t, o);
          f[o] ? (f[o].p(c, a), p(f[o], 1)) : (f[o] = Ue(c), f[o].c(), p(f[o], 1), f[o].m(e, null));
        }
        for (Y(), o = t.length; o < f.length; o += 1)
          i(o);
        W();
      }
    },
    i(s) {
      if (!l) {
        for (let a = 0; a < t.length; a += 1)
          p(f[a]);
        l = !0;
      }
    },
    o(s) {
      f = f.filter(Boolean);
      for (let a = 0; a < f.length; a += 1)
        H(f[a]);
      l = !1;
    },
    d(s) {
      s && z(e), x(f, s);
    }
  };
}
function nn(n) {
  let e = (
    /*header*/
    n[66] + ""
  ), l;
  return {
    c() {
      l = K(e);
    },
    m(t, f) {
      C(t, l, f);
    },
    p(t, f) {
      f[0] & /*headers*/
      128 && e !== (e = /*header*/
      t[66] + "") && ee(l, e);
    },
    d(t) {
      t && z(l);
    }
  };
}
function tn(n) {
  let e, l = (
    /*header*/
    n[66] + ""
  ), t, f, i, s, a = (
    /*sort_column*/
    n[0] === /*index*/
    n[68] && Te(n)
  );
  function o() {
    return (
      /*click_handler_1*/
      n[43](
        /*index*/
        n[68]
      )
    );
  }
  return {
    c() {
      e = S("button"), t = K(l), f = R(), a && a.c(), w(e, "class", "sort-button svelte-18m81hv");
    },
    m(c, _) {
      C(c, e, _), y(e, t), y(e, f), a && a.m(e, null), i || (s = I(e, "click", o), i = !0);
    },
    p(c, _) {
      n = c, _[0] & /*headers*/
      128 && l !== (l = /*header*/
      n[66] + "") && ee(t, l), /*sort_column*/
      n[0] === /*index*/
      n[68] ? a ? a.p(n, _) : (a = Te(n), a.c(), a.m(e, null)) : a && (a.d(1), a = null);
    },
    d(c) {
      c && z(e), a && a.d(), i = !1, s();
    }
  };
}
function Te(n) {
  let e, l = (
    /*sort_order*/
    n[1] === "ascending" ? "▲" : "▼"
  ), t;
  return {
    c() {
      e = S("span"), t = K(l), w(e, "class", "sort-icon svelte-18m81hv");
    },
    m(f, i) {
      C(f, e, i), y(e, t);
    },
    p(f, i) {
      i[0] & /*sort_order*/
      2 && l !== (l = /*sort_order*/
      f[1] === "ascending" ? "▲" : "▼") && ee(t, l);
    },
    d(f) {
      f && z(e);
    }
  };
}
function We(n) {
  let e;
  function l(i, s) {
    return (
      /*header_sort*/
      i[18] || /*manual_sort*/
      i[19] ? tn : nn
    );
  }
  let t = l(n), f = t(n);
  return {
    c() {
      e = S("th"), f.c(), w(e, "class", "svelte-18m81hv");
    },
    m(i, s) {
      C(i, e, s), f.m(e, null);
    },
    p(i, s) {
      t === (t = l(i)) && f ? f.p(i, s) : (f.d(1), f = t(i), f && (f.c(), f.m(e, null)));
    },
    d(i) {
      i && z(e), f.d();
    }
  };
}
function Ye(n) {
  let e;
  return {
    c() {
      e = S("th"), e.textContent = "Actions", w(e, "class", "svelte-18m81hv");
    },
    m(l, t) {
      C(l, e, t);
    },
    d(l) {
      l && z(e);
    }
  };
}
function Fe(n) {
  let e, l, t, f, i, s;
  const a = [
    /*component_props*/
    n[4][
      /*j*/
      n[65]
    ],
    { value: (
      /*value*/
      n[2]
    ) },
    { samples_dir: (
      /*samples_dir*/
      n[30]
    ) },
    { type: "table" },
    {
      selected: (
        /*current_hover*/
        n[25] === /*i*/
        n[57]
      )
    },
    { index: (
      /*i*/
      n[57]
    ) },
    { root: (
      /*root*/
      n[12]
    ) }
  ];
  var o = (
    /*component*/
    n[62]
  );
  function c(h, u) {
    let k = {};
    for (let d = 0; d < a.length; d += 1)
      k = ce(k, a[d]);
    return u !== void 0 && u[0] & /*component_props, component_meta, samples_dir, current_hover, root*/
    1241518096 && (k = ce(k, ue(a, [
      u[0] & /*component_props*/
      16 && _e(
        /*component_props*/
        h[4][
          /*j*/
          h[65]
        ]
      ),
      u[0] & /*component_meta*/
      134217728 && { value: (
        /*value*/
        h[2]
      ) },
      u[0] & /*samples_dir*/
      1073741824 && { samples_dir: (
        /*samples_dir*/
        h[30]
      ) },
      a[3],
      u[0] & /*current_hover*/
      33554432 && {
        selected: (
          /*current_hover*/
          h[25] === /*i*/
          h[57]
        )
      },
      a[5],
      u[0] & /*root*/
      4096 && { root: (
        /*root*/
        h[12]
      ) }
    ]))), { props: k };
  }
  o && (l = re(o, c(n)));
  function _() {
    return (
      /*click_handler_2*/
      n[44](
        /*value*/
        n[2],
        /*i*/
        n[57],
        /*j*/
        n[65],
        /*sample_row*/
        n[55]
      )
    );
  }
  function m() {
    return (
      /*mouseenter_handler_1*/
      n[45](
        /*i*/
        n[57]
      )
    );
  }
  return {
    c() {
      e = S("td"), l && X(l.$$.fragment), me(
        e,
        "max-width",
        /*component_name*/
        n[63] === "textbox" ? "35ch" : "auto"
      ), w(e, "class", t = de(
        /*component_name*/
        n[63]
      ) + " svelte-18m81hv");
    },
    m(h, u) {
      C(h, e, u), l && $(l, e, null), f = !0, i || (s = [
        I(e, "click", _),
        I(e, "mouseenter", m),
        I(
          e,
          "mouseleave",
          /*mouseleave_handler_1*/
          n[46]
        )
      ], i = !0);
    },
    p(h, u) {
      if (n = h, u[0] & /*component_meta*/
      134217728 && o !== (o = /*component*/
      n[62])) {
        if (l) {
          Y();
          const k = l;
          H(k.$$.fragment, 1, 0, () => {
            Z(k, 1);
          }), W();
        }
        o ? (l = re(o, c(n, u)), X(l.$$.fragment), p(l.$$.fragment, 1), $(l, e, null)) : l = null;
      } else if (o) {
        const k = u[0] & /*component_props, component_meta, samples_dir, current_hover, root*/
        1241518096 ? ue(a, [
          u[0] & /*component_props*/
          16 && _e(
            /*component_props*/
            n[4][
              /*j*/
              n[65]
            ]
          ),
          u[0] & /*component_meta*/
          134217728 && { value: (
            /*value*/
            n[2]
          ) },
          u[0] & /*samples_dir*/
          1073741824 && { samples_dir: (
            /*samples_dir*/
            n[30]
          ) },
          a[3],
          u[0] & /*current_hover*/
          33554432 && {
            selected: (
              /*current_hover*/
              n[25] === /*i*/
              n[57]
            )
          },
          a[5],
          u[0] & /*root*/
          4096 && { root: (
            /*root*/
            n[12]
          ) }
        ]) : {};
        l.$set(k);
      }
      (!f || u[0] & /*components*/
      8) && me(
        e,
        "max-width",
        /*component_name*/
        n[63] === "textbox" ? "35ch" : "auto"
      ), (!f || u[0] & /*components*/
      8 && t !== (t = de(
        /*component_name*/
        n[63]
      ) + " svelte-18m81hv")) && w(e, "class", t);
    },
    i(h) {
      f || (l && p(l.$$.fragment, h), f = !0);
    },
    o(h) {
      l && H(l.$$.fragment, h), f = !1;
    },
    d(h) {
      h && z(e), l && Z(l), i = !1, el(s);
    }
  };
}
function Ge(n) {
  let e = (
    /*component_name*/
    n[63] !== void 0 && /*component_map*/
    n[5].get(
      /*component_name*/
      n[63]
    ) !== void 0
  ), l, t, f = e && Fe(n);
  return {
    c() {
      f && f.c(), l = te();
    },
    m(i, s) {
      f && f.m(i, s), C(i, l, s), t = !0;
    },
    p(i, s) {
      s[0] & /*components, component_map*/
      40 && (e = /*component_name*/
      i[63] !== void 0 && /*component_map*/
      i[5].get(
        /*component_name*/
        i[63]
      ) !== void 0), e ? f ? (f.p(i, s), s[0] & /*components, component_map*/
      40 && p(f, 1)) : (f = Fe(i), f.c(), p(f, 1), f.m(l.parentNode, l)) : f && (Y(), H(f, 1, 1, () => {
        f = null;
      }), W());
    },
    i(i) {
      t || (p(f), t = !0);
    },
    o(i) {
      H(f), t = !1;
    },
    d(i) {
      i && z(l), f && f.d(i);
    }
  };
}
function Je(n) {
  let e, l, t, f, i, s, a;
  function o() {
    return (
      /*click_handler_3*/
      n[47](
        /*i*/
        n[57]
      )
    );
  }
  let c = (
    /*active_menu*/
    n[26] === /*i*/
    n[57] && Ke(n)
  );
  return {
    c() {
      e = S("td"), l = S("button"), t = S("img"), i = R(), c && c.c(), je(t.src, f = /*menu_icon*/
      n[16] ? (
        /*menu_icon*/
        n[16]
      ) : (
        /*default_menu_icon*/
        n[29]
      )) || w(t, "src", f), w(t, "alt", "Menu"), w(t, "class", "menu-icon svelte-18m81hv"), me(
        t,
        "transform",
        /*menu_icon*/
        n[16] ? "none" : "rotate(90deg)"
      ), w(l, "class", "menu-button svelte-18m81hv"), w(e, "class", "menu-cell svelte-18m81hv");
    },
    m(_, m) {
      C(_, e, m), y(e, l), y(l, t), y(e, i), c && c.m(e, null), s || (a = I(l, "click", $l(o)), s = !0);
    },
    p(_, m) {
      n = _, m[0] & /*menu_icon, default_menu_icon*/
      536936448 && !je(t.src, f = /*menu_icon*/
      n[16] ? (
        /*menu_icon*/
        n[16]
      ) : (
        /*default_menu_icon*/
        n[29]
      )) && w(t, "src", f), m[0] & /*menu_icon*/
      65536 && me(
        t,
        "transform",
        /*menu_icon*/
        n[16] ? "none" : "rotate(90deg)"
      ), /*active_menu*/
      n[26] === /*i*/
      n[57] ? c ? c.p(n, m) : (c = Ke(n), c.c(), c.m(e, null)) : c && (c.d(1), c = null);
    },
    d(_) {
      _ && z(e), c && c.d(), s = !1, a();
    }
  };
}
function Ke(n) {
  let e, l, t = A(
    /*menu_choices*/
    n[17]
  ), f = [];
  for (let i = 0; i < t.length; i += 1)
    f[i] = Le(Ve(n, t, i));
  return {
    c() {
      e = S("div");
      for (let i = 0; i < f.length; i += 1)
        f[i].c();
      w(e, "class", l = de(`menu-popup ${/*component_meta*/
      n[27].length - 1 === /*i*/
      n[57] ? "last-item" : ""}`) + " svelte-18m81hv");
    },
    m(i, s) {
      C(i, e, s);
      for (let a = 0; a < f.length; a += 1)
        f[a] && f[a].m(e, null);
    },
    p(i, s) {
      if (s[0] & /*menu_choices*/
      131072 | s[1] & /*handle_menu_click*/
      8) {
        t = A(
          /*menu_choices*/
          i[17]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const o = Ve(i, t, a);
          f[a] ? f[a].p(o, s) : (f[a] = Le(o), f[a].c(), f[a].m(e, null));
        }
        for (; a < f.length; a += 1)
          f[a].d(1);
        f.length = t.length;
      }
      s[0] & /*component_meta*/
      134217728 && l !== (l = de(`menu-popup ${/*component_meta*/
      i[27].length - 1 === /*i*/
      i[57] ? "last-item" : ""}`) + " svelte-18m81hv") && w(e, "class", l);
    },
    d(i) {
      i && z(e), x(f, i);
    }
  };
}
function Le(n) {
  let e, l = (
    /*choice*/
    n[59] + ""
  ), t, f, i, s;
  function a(...o) {
    return (
      /*click_handler_4*/
      n[48](
        /*i*/
        n[57],
        /*choice*/
        n[59],
        ...o
      )
    );
  }
  return {
    c() {
      e = S("button"), t = K(l), f = R(), w(e, "class", "menu-item svelte-18m81hv");
    },
    m(o, c) {
      C(o, e, c), y(e, t), y(e, f), i || (s = I(e, "click", a), i = !0);
    },
    p(o, c) {
      n = o, c[0] & /*menu_choices*/
      131072 && l !== (l = /*choice*/
      n[59] + "") && ee(t, l);
    },
    d(o) {
      o && z(e), i = !1, s();
    }
  };
}
function Oe(n) {
  var c;
  let e, l, t, f, i = A(
    /*sample_row*/
    n[55]
  ), s = [];
  for (let _ = 0; _ < i.length; _ += 1)
    s[_] = Ge(De(n, i, _));
  const a = (_) => H(s[_], 1, 1, () => {
    s[_] = null;
  });
  let o = (
    /*menu_choices*/
    ((c = n[17]) == null ? void 0 : c.length) > 0 && Je(n)
  );
  return {
    c() {
      e = S("tr");
      for (let _ = 0; _ < s.length; _ += 1)
        s[_].c();
      l = R(), o && o.c(), t = R(), w(e, "class", "tr-body svelte-18m81hv");
    },
    m(_, m) {
      C(_, e, m);
      for (let h = 0; h < s.length; h += 1)
        s[h] && s[h].m(e, null);
      y(e, l), o && o.m(e, null), y(e, t), f = !0;
    },
    p(_, m) {
      var h;
      if (m[0] & /*components, gradio, component_meta, component_props, samples_dir, current_hover, root, component_map*/
      1242566712 | m[1] & /*handle_mouseenter, handle_mouseleave*/
      3) {
        i = A(
          /*sample_row*/
          _[55]
        );
        let u;
        for (u = 0; u < i.length; u += 1) {
          const k = De(_, i, u);
          s[u] ? (s[u].p(k, m), p(s[u], 1)) : (s[u] = Ge(k), s[u].c(), p(s[u], 1), s[u].m(e, l));
        }
        for (Y(), u = i.length; u < s.length; u += 1)
          a(u);
        W();
      }
      /*menu_choices*/
      ((h = _[17]) == null ? void 0 : h.length) > 0 ? o ? o.p(_, m) : (o = Je(_), o.c(), o.m(e, t)) : o && (o.d(1), o = null);
    },
    i(_) {
      if (!f) {
        for (let m = 0; m < i.length; m += 1)
          p(s[m]);
        f = !0;
      }
    },
    o(_) {
      s = s.filter(Boolean);
      for (let m = 0; m < s.length; m += 1)
        H(s[m]);
      f = !1;
    },
    d(_) {
      _ && z(e), x(s, _), o && o.d();
    }
  };
}
function Qe(n) {
  let e, l, t, f, i, s, a, o;
  const c = [on, fn], _ = [];
  function m(k, d) {
    return d[0] & /*component_meta, component_map, components*/
    134217768 && (l = null), /*sample_labels*/
    k[8] ? 0 : (l == null && (l = !!/*component_meta*/
    (k[27].length && /*component_map*/
    k[5].get(
      /*components*/
      k[3][0]
    ))), l ? 1 : -1);
  }
  ~(t = m(n, [-1, -1, -1])) && (f = _[t] = c[t](n));
  function h() {
    return (
      /*click_handler*/
      n[40](
        /*i*/
        n[57],
        /*sample_row*/
        n[55]
      )
    );
  }
  function u() {
    return (
      /*mouseenter_handler*/
      n[41](
        /*i*/
        n[57]
      )
    );
  }
  return {
    c() {
      e = S("button"), f && f.c(), i = R(), w(e, "class", "gallery-item svelte-18m81hv");
    },
    m(k, d) {
      C(k, e, d), ~t && _[t].m(e, null), y(e, i), s = !0, a || (o = [
        I(e, "click", h),
        I(e, "mouseenter", u),
        I(
          e,
          "mouseleave",
          /*mouseleave_handler*/
          n[42]
        )
      ], a = !0);
    },
    p(k, d) {
      n = k;
      let g = t;
      t = m(n, d), t === g ? ~t && _[t].p(n, d) : (f && (Y(), H(_[g], 1, 1, () => {
        _[g] = null;
      }), W()), ~t ? (f = _[t], f ? f.p(n, d) : (f = _[t] = c[t](n), f.c()), p(f, 1), f.m(e, i)) : f = null);
    },
    i(k) {
      s || (p(f), s = !0);
    },
    o(k) {
      H(f), s = !1;
    },
    d(k) {
      k && z(e), ~t && _[t].d(), a = !1, el(o);
    }
  };
}
function fn(n) {
  let e, l, t;
  const f = [
    /*component_props*/
    n[4][0],
    { value: (
      /*sample_row*/
      n[55][0]
    ) },
    { samples_dir: (
      /*samples_dir*/
      n[30]
    ) },
    { type: "gallery" },
    {
      selected: (
        /*current_hover*/
        n[25] === /*i*/
        n[57]
      )
    },
    { index: (
      /*i*/
      n[57]
    ) },
    { root: (
      /*root*/
      n[12]
    ) }
  ];
  var i = (
    /*component_meta*/
    n[27][0][0].component
  );
  function s(a, o) {
    let c = {};
    for (let _ = 0; _ < f.length; _ += 1)
      c = ce(c, f[_]);
    return o !== void 0 && o[0] & /*component_props, selected_samples, samples_dir, current_hover, root*/
    1124077584 && (c = ce(c, ue(f, [
      o[0] & /*component_props*/
      16 && _e(
        /*component_props*/
        a[4][0]
      ),
      o[0] & /*selected_samples*/
      16777216 && { value: (
        /*sample_row*/
        a[55][0]
      ) },
      o[0] & /*samples_dir*/
      1073741824 && { samples_dir: (
        /*samples_dir*/
        a[30]
      ) },
      f[3],
      o[0] & /*current_hover*/
      33554432 && {
        selected: (
          /*current_hover*/
          a[25] === /*i*/
          a[57]
        )
      },
      f[5],
      o[0] & /*root*/
      4096 && { root: (
        /*root*/
        a[12]
      ) }
    ]))), { props: c };
  }
  return i && (e = re(i, s(n))), {
    c() {
      e && X(e.$$.fragment), l = te();
    },
    m(a, o) {
      e && $(e, a, o), C(a, l, o), t = !0;
    },
    p(a, o) {
      if (o[0] & /*component_meta*/
      134217728 && i !== (i = /*component_meta*/
      a[27][0][0].component)) {
        if (e) {
          Y();
          const c = e;
          H(c.$$.fragment, 1, 0, () => {
            Z(c, 1);
          }), W();
        }
        i ? (e = re(i, s(a, o)), X(e.$$.fragment), p(e.$$.fragment, 1), $(e, l.parentNode, l)) : e = null;
      } else if (i) {
        const c = o[0] & /*component_props, selected_samples, samples_dir, current_hover, root*/
        1124077584 ? ue(f, [
          o[0] & /*component_props*/
          16 && _e(
            /*component_props*/
            a[4][0]
          ),
          o[0] & /*selected_samples*/
          16777216 && { value: (
            /*sample_row*/
            a[55][0]
          ) },
          o[0] & /*samples_dir*/
          1073741824 && { samples_dir: (
            /*samples_dir*/
            a[30]
          ) },
          f[3],
          o[0] & /*current_hover*/
          33554432 && {
            selected: (
              /*current_hover*/
              a[25] === /*i*/
              a[57]
            )
          },
          f[5],
          o[0] & /*root*/
          4096 && { root: (
            /*root*/
            a[12]
          ) }
        ]) : {};
        e.$set(c);
      }
    },
    i(a) {
      t || (e && p(e.$$.fragment, a), t = !0);
    },
    o(a) {
      e && H(e.$$.fragment, a), t = !1;
    },
    d(a) {
      a && z(l), e && Z(e, a);
    }
  };
}
function on(n) {
  let e, l;
  return e = new Ql({
    props: {
      value: (
        /*sample_row*/
        n[55][0]
      ),
      selected: (
        /*current_hover*/
        n[25] === /*i*/
        n[57]
      ),
      type: "gallery"
    }
  }), {
    c() {
      X(e.$$.fragment);
    },
    m(t, f) {
      $(e, t, f), l = !0;
    },
    p(t, f) {
      const i = {};
      f[0] & /*selected_samples*/
      16777216 && (i.value = /*sample_row*/
      t[55][0]), f[0] & /*current_hover*/
      33554432 && (i.selected = /*current_hover*/
      t[25] === /*i*/
      t[57]), e.$set(i);
    },
    i(t) {
      l || (p(e.$$.fragment, t), l = !0);
    },
    o(t) {
      H(e.$$.fragment, t), l = !1;
    },
    d(t) {
      Z(e, t);
    }
  };
}
function Ue(n) {
  let e, l, t = (
    /*sample_row*/
    n[55][0] && Qe(n)
  );
  return {
    c() {
      t && t.c(), e = te();
    },
    m(f, i) {
      t && t.m(f, i), C(f, e, i), l = !0;
    },
    p(f, i) {
      /*sample_row*/
      f[55][0] ? t ? (t.p(f, i), i[0] & /*selected_samples*/
      16777216 && p(t, 1)) : (t = Qe(f), t.c(), p(t, 1), t.m(e.parentNode, e)) : t && (Y(), H(t, 1, 1, () => {
        t = null;
      }), W());
    },
    i(f) {
      l || (p(t), l = !0);
    },
    o(f) {
      H(t), l = !1;
    },
    d(f) {
      f && z(e), t && t.d(f);
    }
  };
}
function Xe(n) {
  let e, l, t = A(
    /*visible_pages*/
    n[23]
  ), f = [];
  for (let i = 0; i < t.length; i += 1)
    f[i] = Ze(Ae(n, t, i));
  return {
    c() {
      e = S("div"), l = K(`Pages:
      `);
      for (let i = 0; i < f.length; i += 1)
        f[i].c();
      w(e, "class", "paginate svelte-18m81hv");
    },
    m(i, s) {
      C(i, e, s), y(e, l);
      for (let a = 0; a < f.length; a += 1)
        f[a] && f[a].m(e, null);
    },
    p(i, s) {
      if (s[0] & /*visible_pages, page*/
      10485760) {
        t = A(
          /*visible_pages*/
          i[23]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const o = Ae(i, t, a);
          f[a] ? f[a].p(o, s) : (f[a] = Ze(o), f[a].c(), f[a].m(e, null));
        }
        for (; a < f.length; a += 1)
          f[a].d(1);
        f.length = t.length;
      }
    },
    d(i) {
      i && z(e), x(f, i);
    }
  };
}
function an(n) {
  let e, l = (
    /*visible_page*/
    n[52] + 1 + ""
  ), t, f, i, s;
  function a() {
    return (
      /*click_handler_5*/
      n[49](
        /*visible_page*/
        n[52]
      )
    );
  }
  return {
    c() {
      e = S("button"), t = K(l), f = R(), w(e, "class", "svelte-18m81hv"), Ee(
        e,
        "current-page",
        /*page*/
        n[21] === /*visible_page*/
        n[52]
      );
    },
    m(o, c) {
      C(o, e, c), y(e, t), y(e, f), i || (s = I(e, "click", a), i = !0);
    },
    p(o, c) {
      n = o, c[0] & /*visible_pages*/
      8388608 && l !== (l = /*visible_page*/
      n[52] + 1 + "") && ee(t, l), c[0] & /*page, visible_pages*/
      10485760 && Ee(
        e,
        "current-page",
        /*page*/
        n[21] === /*visible_page*/
        n[52]
      );
    },
    d(o) {
      o && z(e), i = !1, s();
    }
  };
}
function sn(n) {
  let e;
  return {
    c() {
      e = S("div"), e.textContent = "...";
    },
    m(l, t) {
      C(l, e, t);
    },
    p: Zl,
    d(l) {
      l && z(e);
    }
  };
}
function Ze(n) {
  let e;
  function l(i, s) {
    return (
      /*visible_page*/
      i[52] === -1 ? sn : an
    );
  }
  let t = l(n), f = t(n);
  return {
    c() {
      f.c(), e = te();
    },
    m(i, s) {
      f.m(i, s), C(i, e, s);
    },
    p(i, s) {
      t === (t = l(i)) && f ? f.p(i, s) : (f.d(1), f = t(i), f && (f.c(), f.m(e.parentNode, e)));
    },
    d(i) {
      i && z(e), f.d(i);
    }
  };
}
function cn(n) {
  let e, l, t, f, i, s, a, o, c, _, m;
  const h = [ln, en], u = [];
  function k(g, b) {
    return (
      /*gallery*/
      g[28] ? 0 : 1
    );
  }
  a = k(n), o = u[a] = h[a](n);
  let d = (
    /*paginate*/
    n[22] && Xe(n)
  );
  return {
    c() {
      e = S("div"), l = Be("svg"), t = Be("path"), f = R(), i = K(
        /*label*/
        n[6]
      ), s = R(), o.c(), c = R(), d && d.c(), _ = te(), w(t, "fill", "currentColor"), w(t, "d", "M10 6h18v2H10zm0 18h18v2H10zm0-9h18v2H10zm-6 0h2v2H4zm0-9h2v2H4zm0 18h2v2H4z"), w(l, "xmlns", "http://www.w3.org/2000/svg"), w(l, "xmlns:xlink", "http://www.w3.org/1999/xlink"), w(l, "aria-hidden", "true"), w(l, "role", "img"), w(l, "width", "1em"), w(l, "height", "1em"), w(l, "preserveAspectRatio", "xMidYMid meet"), w(l, "viewBox", "0 0 32 32"), w(l, "class", "svelte-18m81hv"), w(e, "class", "label svelte-18m81hv");
    },
    m(g, b) {
      C(g, e, b), y(e, l), y(l, t), y(e, f), y(e, i), C(g, s, b), u[a].m(g, b), C(g, c, b), d && d.m(g, b), C(g, _, b), m = !0;
    },
    p(g, b) {
      (!m || b[0] & /*label*/
      64) && ee(
        i,
        /*label*/
        g[6]
      );
      let M = a;
      a = k(g), a === M ? u[a].p(g, b) : (Y(), H(u[M], 1, 1, () => {
        u[M] = null;
      }), W(), o = u[a], o ? o.p(g, b) : (o = u[a] = h[a](g), o.c()), p(o, 1), o.m(c.parentNode, c)), /*paginate*/
      g[22] ? d ? d.p(g, b) : (d = Xe(g), d.c(), d.m(_.parentNode, _)) : d && (d.d(1), d = null);
    },
    i(g) {
      m || (p(o), m = !0);
    },
    o(g) {
      H(o), m = !1;
    },
    d(g) {
      g && (z(e), z(s), z(c), z(_)), u[a].d(g), d && d.d(g);
    }
  };
}
function rn(n) {
  let e, l;
  return e = new jl({
    props: {
      visible: (
        /*visible*/
        n[11]
      ),
      padding: !1,
      elem_id: (
        /*elem_id*/
        n[9]
      ),
      elem_classes: (
        /*elem_classes*/
        n[10]
      ),
      scale: (
        /*scale*/
        n[14]
      ),
      min_width: (
        /*min_width*/
        n[15]
      ),
      allow_overflow: !1,
      container: !1,
      $$slots: { default: [cn] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      X(e.$$.fragment);
    },
    m(t, f) {
      $(e, t, f), l = !0;
    },
    p(t, f) {
      const i = {};
      f[0] & /*visible*/
      2048 && (i.visible = /*visible*/
      t[11]), f[0] & /*elem_id*/
      512 && (i.elem_id = /*elem_id*/
      t[9]), f[0] & /*elem_classes*/
      1024 && (i.elem_classes = /*elem_classes*/
      t[10]), f[0] & /*scale*/
      16384 && (i.scale = /*scale*/
      t[14]), f[0] & /*min_width*/
      32768 && (i.min_width = /*min_width*/
      t[15]), f[0] & /*visible_pages, page, paginate, selected_samples, value, samples_per_page, gradio, current_hover, sample_labels, component_meta, component_props, root, component_map, components, gallery, menu_choices, active_menu, menu_icon, default_menu_icon, headers, sort_order, sort_column, header_sort, manual_sort, label*/
      1073689087 | f[2] & /*$$scope*/
      128 && (i.$$scope = { dirty: f, ctx: t }), e.$set(i);
    },
    i(t) {
      l || (p(e.$$.fragment, t), l = !0);
    },
    o(t) {
      H(e.$$.fragment, t), l = !1;
    },
    d(t) {
      Z(e, t);
    }
  };
}
function _n(n) {
  return n.map((e) => e.value);
}
function un(n, e, l) {
  let t, f, i;
  var s = this && this.__awaiter || function(r, q, N, j) {
    function le(ne) {
      return ne instanceof N ? ne : new N(function(se) {
        se(ne);
      });
    }
    return new (N || (N = Promise))(function(ne, se) {
      function dl(J) {
        try {
          ke(j.next(J));
        } catch (we) {
          se(we);
        }
      }
      function ml(J) {
        try {
          ke(j.throw(J));
        } catch (we) {
          se(we);
        }
      }
      function ke(J) {
        J.done ? ne(J.value) : le(J.value).then(dl, ml);
      }
      ke((j = j.apply(r, q || [])).next());
    });
  };
  let { components: a } = e, { component_props: o } = e, { component_map: c } = e, { label: _ = "Examples" } = e, { headers: m } = e, { samples: h = null } = e, u = null, { sample_labels: k = null } = e, { elem_id: d = "" } = e, { elem_classes: g = [] } = e, { visible: b = !0 } = e, { value: M = null } = e, { root: L } = e, { proxy_url: O } = e, { samples_per_page: B = 10 } = e, { scale: v = null } = e, { min_width: pe = void 0 } = e, { menu_icon: ye = null } = e, { menu_choices: ze = [] } = e, { header_sort: fe = !1 } = e, { sort_column: P = null } = e, { sort_order: T = null } = e, { manual_sort: ie = !1 } = e, { gradio: F } = e, ll = O ? `/proxy=${O}file=` : `${L}/file=`, V = 0, he = h ? h.length > B : !1, be, oe, G = [], ae = -1, Q = null;
  function ge(r) {
    l(25, ae = r);
  }
  function ve() {
    l(25, ae = -1), setTimeout(
      () => {
        ae !== Q && l(26, Q = null);
      },
      100
    );
  }
  function Ce(r) {
    !fe && !ie || (P === r ? l(1, T = T === "ascending" ? "descending" : "ascending") : (l(0, P = r), l(1, T = "ascending")), F.dispatch("select", {
      index: P,
      value: { column: P, order: T }
    }));
  }
  function Se(r, q, N) {
    N.stopPropagation();
    const j = r + V * B;
    F.dispatch("select", {
      index: j,
      value: { menu_choice: q },
      row_value: h[j]
    }), l(26, Q = null);
  }
  let qe = [];
  function nl(r) {
    return s(this, void 0, void 0, function* () {
      l(27, qe = yield Promise.all(r && r.map((q) => s(this, void 0, void 0, function* () {
        return yield Promise.all(q.map((N, j) => s(this, void 0, void 0, function* () {
          var le;
          return {
            value: N,
            component: (le = yield c.get(a[j])) === null || le === void 0 ? void 0 : le.default
          };
        })));
      }))));
    });
  }
  const tl = (r, q) => {
    l(2, M = r + V * B), F.dispatch("click", M), F.dispatch("select", { index: M, value: q });
  }, fl = (r) => ge(r), il = () => ve(), ol = (r) => Ce(r), al = (r, q, N, j) => {
    F.dispatch("click", r), F.dispatch("select", {
      index: [q, N],
      value: r,
      row_value: _n(j)
    });
  }, sl = (r) => ge(r), cl = () => ve(), rl = (r) => l(26, Q = Q === r ? null : r), _l = (r, q, N) => Se(r, q, N), ul = (r) => l(21, V = r);
  return n.$$set = (r) => {
    "components" in r && l(3, a = r.components), "component_props" in r && l(4, o = r.component_props), "component_map" in r && l(5, c = r.component_map), "label" in r && l(6, _ = r.label), "headers" in r && l(7, m = r.headers), "samples" in r && l(35, h = r.samples), "sample_labels" in r && l(8, k = r.sample_labels), "elem_id" in r && l(9, d = r.elem_id), "elem_classes" in r && l(10, g = r.elem_classes), "visible" in r && l(11, b = r.visible), "value" in r && l(2, M = r.value), "root" in r && l(12, L = r.root), "proxy_url" in r && l(36, O = r.proxy_url), "samples_per_page" in r && l(13, B = r.samples_per_page), "scale" in r && l(14, v = r.scale), "min_width" in r && l(15, pe = r.min_width), "menu_icon" in r && l(16, ye = r.menu_icon), "menu_choices" in r && l(17, ze = r.menu_choices), "header_sort" in r && l(18, fe = r.header_sort), "sort_column" in r && l(0, P = r.sort_column), "sort_order" in r && l(1, T = r.sort_order), "manual_sort" in r && l(19, ie = r.manual_sort), "gradio" in r && l(20, F = r.gradio);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*components, sample_labels*/
    264 && l(28, f = a.length < 2 || k !== null), n.$$.dirty[0] & /*sample_labels, samples_per_page, paginate, page, visible_pages*/
    14688512 | n.$$.dirty[1] & /*samples, old_samples, page_count*/
    208 && (k ? l(35, h = k.map((r) => [r])) : h || l(35, h = []), h !== u && (l(21, V = 0), l(37, u = h)), l(22, he = h.length > B), he ? (l(23, G = []), l(24, be = h.slice(V * B, (V + 1) * B)), l(38, oe = Math.ceil(h.length / B)), [0, V, oe - 1].forEach((r) => {
      for (let q = r - 2; q <= r + 2; q++)
        q >= 0 && q < oe && !G.includes(q) && (G.length > 0 && q - G[G.length - 1] > 1 && G.push(-1), G.push(q));
    })) : l(24, be = h.slice())), n.$$.dirty[1] & /*samples*/
    16 && l(39, i = h ? [...h] : []), n.$$.dirty[0] & /*header_sort, manual_sort, sort_column, sort_order*/
    786435 | n.$$.dirty[1] & /*sortedSamples*/
    256 && fe && !ie && P !== null && T !== null && i.sort((r, q) => {
      const N = r[P], j = q[P];
      return N < j ? T === "ascending" ? -1 : 1 : N > j ? T === "ascending" ? 1 : -1 : 0;
    }), n.$$.dirty[0] & /*component_map, page, samples_per_page*/
    2105376 | n.$$.dirty[1] & /*sortedSamples*/
    256 && nl(i.slice(V * B, (V + 1) * B));
  }, l(29, t = "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/icons/three-dots-vertical.svg"), [
    P,
    T,
    M,
    a,
    o,
    c,
    _,
    m,
    k,
    d,
    g,
    b,
    L,
    B,
    v,
    pe,
    ye,
    ze,
    fe,
    ie,
    F,
    V,
    he,
    G,
    be,
    ae,
    Q,
    qe,
    f,
    t,
    ll,
    ge,
    ve,
    Ce,
    Se,
    h,
    O,
    u,
    oe,
    i,
    tl,
    fl,
    il,
    ol,
    al,
    sl,
    cl,
    rl,
    _l,
    ul
  ];
}
class dn extends Ul {
  constructor(e) {
    super(), Xl(
      this,
      e,
      un,
      rn,
      xl,
      {
        components: 3,
        component_props: 4,
        component_map: 5,
        label: 6,
        headers: 7,
        samples: 35,
        sample_labels: 8,
        elem_id: 9,
        elem_classes: 10,
        visible: 11,
        value: 2,
        root: 12,
        proxy_url: 36,
        samples_per_page: 13,
        scale: 14,
        min_width: 15,
        menu_icon: 16,
        menu_choices: 17,
        header_sort: 18,
        sort_column: 0,
        sort_order: 1,
        manual_sort: 19,
        gradio: 20
      },
      null,
      [-1, -1, -1]
    );
  }
}
export {
  dn as default
};
