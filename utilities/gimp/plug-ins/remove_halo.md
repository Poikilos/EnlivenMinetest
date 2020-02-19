# Channel Tools

https://github.com/poikilos/channel_tools.git

## [git] - 2020-02-19
### Removed
- This may have worked after additoinal fixes.
  - https://www.youtube.com/watch?v=YHXX3KuB23Q (outdated)
  - https://jacksonbates.wordpress.com/2015/09/14/python-fu-6-accepting-user-input/
```python
register(
    "python_fu_remove_halo",
    "Remove Halo",
    "Remove alpha",
    "Jake Gustafson", "Jake Gustafson", "2020",
    "Remove Halo",  # caption
    "RGBA",  # RGB* would mean with or without alpha.
    [
        (PF_SPINNER, "threshold", "Minimum alpha to fix", 254, (0, 255, 1)),
        (PF_BOOL, "make_opaque", "Make the fixed parts opaque.", True),
        (PF_DRAWABLE, "drawable", "Input layer", None),
    ],
    [],
    remove_layer_halo,
    menu="<Image>/Layer"
)
```

- This may be deprecated, even though it matches the docs.
  - https://www.gimp.org/docs/python/index.html
```python
register(
    "python_fu_remove_halo",
    "Remove Halo",
    "Remove Halo (Redo the edge)",
    "Jake Gustafson",
    "Jake Gustafson",
    "2020",
    "<Image>/Layer",
    "RGBA",  # RGB* would mean with or without alpha.
    [
        (PF_SPINNER, "threshold", "Minimum alpha to fix", 254, (0, 255, 1)),
        (PF_BOOL, "make_opaque", "Make the fixed parts opaque.", True),
        (PF_DRAWABLE, "drawable", "Input layer", None),
    ],
    [],
    remove_layer_halo
)
```
