---
name: react-components
description: Emit a JSON UI spec so the chat frontend can render React components. Currently supports component id "list".
---

# React components

You can create React components in the chat UI by returning a JSON spec alongside your text reply. The frontend owns the look and feel — you only choose the component and its data.

## When to use

Use a component whenever the user should see structured results rather than a paragraph: search hits, enumerations, ranked options, or any set of discrete items.

For a plain conversational reply (greetings, explanations, yes/no), omit the component.

## JSON structure

Every final reply is this object:

```json
{
  "text": "Short message shown above the component.",
  "component": {
    "id": "list",
    "title": "Optional heading",
    "items": ["First item", "Second item"]
  }
}
```

- `text` is always required. Keep it brief; the component carries the data.
- `component` is `null` when no widget should render.
- The only supported `id` for now is `"list"`.

### `id: "list"`

Render a list when there are two or more items (or when search/tool results are a collection).

```json
{
  "id": "list",
  "title": "Search results",
  "items": ["Acme Corp", "Acme Industries"]
}
```

Rules:

- `id` must be the string `"list"`.
- `items` is a list of strings. Do not nest objects.
- `title` is optional; use it to label the list.
- Put human-readable labels in `items`, not raw JSON dumps.
- Never put the JSON spec inside `text`. `text` is prose only.
