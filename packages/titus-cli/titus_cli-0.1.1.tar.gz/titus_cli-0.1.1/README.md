# Titus CLI

![Titus-logo](titus-logo-text-medium.png)

**Titus** is a toolkit composed by a CSS template system, a theming tool and a developer companion, targeted to the CSS artisan that likes to work by hand, with full control over the code, without sacrificing simplicity and ease of use.

This is the CLI tool that will generate the Titus CSS system files for any kind of frontend project that uses CSS.

## Features

- Generate CSS theme files with a predefined structure.
- Define and manage CSS variables and templates.
- Automatically generates a complete CSS system with:
    - a CSS reset (the classic <http://meyerweb.com/eric/tools/css/reset/>);
    - absolute and relative general sizes;
    - absolute and relative font sizes;
    - a fully fledged five colors palette, with tints and shades for every color, based on the user's main color input;
    - a border, shadows and breakpoints pre-established system.
- And more, very soon!

## Requirements

The Titus CLI tool is distributed as a Python package, and it requires **Python 3.8** or upwards. It is designed to work in combination with the [**Visual Studio Code Extension Titus Companion**](https://github.com/devluxor/titus-vscode-companion), which greatly improves the developer experience by providing a keyboard shortcut to easily enter Titus variables.

## Installation

Install the Titus CLI by downloading it from the Python Package Index:

```sh
pip install titus-cli
```

or 

```sh
pip install --user titus-cli
```

The difference between `pip install` and `pip install --user` is primarily where the Python packages are installed: `pip install` installs the package globally for the entire system, and `pip install --user` Installs the package for the current user only, without needing administrative permissions.  `pip install --user` provides an isolated and safer installation method for personal use without affecting the global environment.

### Usage

Once installed in the system, go to the target folder in which the main CSS files for the project will be: usually, these are named `styles`, `stylesheets`, `css`, or similar. Once there, enter:

```sh
titus init
```

You will be prompted for a main color, and Titus will generate a full CSS system based on that input.

Then, import the `reset.css` and `titus-system.css` files from your other CSS files:

```css
@import(reset.css);
@import(titus-system.css);
```

You can also add them via HTML tags, or using `import` in a React application, e.g.

Using the Titus system along the Companion in Visual Studio Code gives access to the full power of Titus by pressing shift + f7, making much easier to enter Titus variables names. *Please, read the following section.*

### Variable codes

This is an example of how a Titus variable looks like:

```css
:root {

  --TITUS-srA: calc(1rem * 0.25);

}
```

Each Titus variable is formed by:

- The necessary double slash `--`
- A `TITUS` prefix to differentiate it from other variables
- A single slash `-` that separates the prefix from the *variable code*
- A variable code. In this example, it's `sr`, for **S**ize **R**elative. Each type of variable has its own code. For instance, `s` for absolute sizes (`--TITUS-sH`), or `mc` for the **M**ain app **C**olor
- An uppercase letter. In this example, `A`. This letter indicates the scale or intensity, where `A` is the minimum and `Z` the maximum. In the Titus color system, it refers to the lightness: letter `E` corresponds to the base color, `A` to the lightest tint, and `N` to the darkest shade.

### Reference

#### Quick Reference Table

| Category                | Variable Code | Example            |
|-------------------------|---------------|--------------------|
| General Absolute Sizes  | `s`           | `--TITUS-sA`       |
| General Relative Sizes  | `sr`          | `--TITUS-srA`      |
| Absolute Font Sizes     | `f`           | `--TITUS-fA`       |
| Relative Font Sizes     | `fr`          | `--TITUS-fr`       |
| Font Weights*           | `fw`          | `--TITUS-fwt`      |
| Main Color              | `mc`          | `--TITUS-mcA`      |
| Complementary Color     | `cc`          | `--TITUS-ccA`      |
| Accent Color #1         | `ac1`         | `--TITUS-ac1A`     |
| Accent Color #2         | `ac2`         | `--TITUS-ac2A`     |
| Accent Color #3         | `ac3`         | `--TITUS-ac3A`     |
| Accent Color #4         | `ac4`         | `--TITUS-ac4A`     |

*Font Weight Scale:

- `wt`: 100, Thin
- `wel`: 200, Extra Light
- `wl`: 300, Light
- `wn`: 400, Neutral
- `wm`: 500, Medium
- `wsb`: 600, Semi Bold
- `wb`: 700, Bold
- `web`: 800, Extra Bold
- `wbl`: 900, Black
