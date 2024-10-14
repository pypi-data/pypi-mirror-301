# pptx2typ

`pptx2typ` is a command-line tool that converts PowerPoint (`.pptx`) presentations into [Typst](https://typst.app/) scripts. This tool is designed to facilitate the transition from traditional slide presentations to customizable, script-based documents, a baby step before you leverage the power of Typst's typesetting capabilities.

## 📝 Features

- **Convert PPTX to Typst:** Seamlessly transform your PowerPoint presentations into Typst scripts.
- **Image Extraction:** Automatically extract and include images from slides into the Typst document.
- **Table Support:** Extract and format tables from your slides into Typst.
- **Text Formatting:** Preserve text formatting, including bold, italics, underlines, and hyperlinks.

## 🚀 Installation

You can install `pptx2typ` using [`pipx`](https://pipxproject.github.io/pipx/), which allows you to run Python applications in isolated environments.

1. **Install `pipx` (if not already installed):**

```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

You may need to restart your terminal after this step.

2. **Install pptx2typ via pipx:**

```bash
pipx install pptx2typ
```

Alternatively, if you have built the package locally, and install it using:

```bash
pipx install path/to/pptx2typ-0.1.0-py3-none-any.whl
```

## 🎯 Usage

Once installed, you can use the `pptx2typ` command in your terminal.

```bash
pptx2typ input.pptx -o output.typ -d images/ -t templates/fit_uiuc_theme.typ
```

### 📋 Command-Line Arguments

- **Positional Argument:**
  - `input_file`: Path to the input PPTX file.

- **Optional Arguments:**
  - `-o`, `--output-file`: Path to the output Typst file. Defaults to the input file's name with a `.typ` extension.
  - `-d`, `--output-dir`: Directory to save extracted images. Defaults to `cwd/"assets"`.
  - `-t`, `--theme`: Theme to use for the Typst slides. Defaults to `university`. Provide a path if using a custom theme.

### 📚 Example

```bash
pptx2typ presentation.pptx -o presentation.typ -d ./assets -t dewdrop
```

This command will:

- Convert `presentation.pptx` to `presentation.typ`.
- Extract images into the `./assets` directory.
- Apply the `dewdrop` theme.

## 🧑‍💻 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add YourFeature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

   Describe your changes and submit the pull request for review.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 📫 Contact

For any inquiries or support, please contact [your-email@example.com](mailto:your-email@example.com).

## 💡 Acknowledgements

- [python-pptx](https://python-pptx.readthedocs.io/en/latest/) for handling PowerPoint files.
- [Typst](https://typst.app/) for providing a powerful typesetting system.
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output.

