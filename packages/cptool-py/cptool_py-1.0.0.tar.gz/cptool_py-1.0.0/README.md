# cp-tool
A command-line interface (CLI) for creating competitive programming problem files.

## Configuration
To set up your templates, copy them to `~/.local/share/cp-tool/template.<extension>`.  
*(If you're using Windows or Mac, please [install Linux](https://github.com/Amog-OS/AmogOS).)*

## Usage
```
cpt <commands> [args]
```

## Commands
- **Create a Problem:**
  ```bash
  cpt problem <name>
  ```
  Creates a folder containing a template for the specified problem name.

- **Create a Contest:**
  ```bash
  cpt contest <num_problems> <name>
  ```
  Creates a folder with `<num_problems>` problem files.

- **Create or Replace a Template:**
  ```bash
  cpt template <file>
  ```
  Creates a new template file or replaces an existing one with the specified name.

## Arguments
- **File Extension:**
  ```bash
  --extension=<ext> or -e=<ext>
  ```
  Use this parameter to specify the file extension for the templates and problem files.

## Automatic Directory Change
To avoid manually changing directories to the newly created folders, you can run the command with:
```bash
source cpt <arguments>
```
Alternatively, you can create an alias in your shell profile to make `cpt` execute with `source` automatically:
```bash
alias cpt='source cpt'
```
