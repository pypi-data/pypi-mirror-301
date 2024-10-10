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

## Usage

Install the Titus CLI by downloading it from the Python Package Index:

```sh

```

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

Using the Titus system along the Companion in Visual Studio Code gives access to the full power of Titus by pressing shift + f7, making much easier to enter Titus variables names.
