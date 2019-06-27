# mpl_colors

A python 3.6+ library to make matplotlib's [named colors](https://matplotlib.org/examples/color/named_colors.html) more discoverable.

Defines enums for each of matplotlib's sets of named colours (base, Tableau, xkcd and CSS4), and one which combines all of them (where Tableau and xkcd names are prepended with `TAB_` and `XKCD_` respectively, like matplotlib).
Color names are in `SCREAMING_SNAKE_CASE`, as recommended.
Names originally containing a slash (`/`) replace it with the `_SLASH_` (necessary to prevent collisions).

Instances of these enums are also instances of a named tuple with members `r`, `g`, and `b` (all floats between 0 and 1).
They also support a number of methods for conversion into `colour.Color` objects, and RGBA, HSL, HSV, and YIQ tuples.
Also, 256-color hex strings (prepended with `#`) and `colour`'s "web" format (whichever is shortest of W3C named color, 16-color hex, or 256-color hex, preferring named as a tie-break).

The enums are automatically generated directly from `matplotlib.colors` using the included `make_colors.py`.
Like matplotlib, they support both spellings of the word "grey"/"gray".
