FORM_INPUT_CLASSES = (
    "w-full rounded-lg border border-slate-300 "
    "px-3 py-2 shadow-sm "
    "focus:border-slate-500 focus:outline-none "
    "focus:ring-2 focus:ring-slate-300"
)

FORM_CHECKBOX_CLASSES = (
    "h-4 w-4 rounded border-slate-300 "
    "text-slate-900 focus:ring-slate-300"
)

FORM_RADIO_CLASSES = (
    "h-4 w-4 border-slate-300 "
    "text-slate-900 focus:ring-slate-300"
)


def apply_form_control_styles(form):
    for field in form.fields.values():
        widget = field.widget

        if widget.input_type == "checkbox":
            widget.attrs["class"] = FORM_CHECKBOX_CLASSES

        elif widget.input_type == "radio":
            widget.attrs["class"] = FORM_RADIO_CLASSES

        else:
            existing_classes = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing_classes} {FORM_INPUT_CLASSES}".strip()

    return form