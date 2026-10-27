# Text Transformer

A modern desktop application built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for fast, real-time text manipulation, casing adjustments, and delimiter transformations.

## ✨ Features

- **Case Conversions**:
  - UPPERCASE
  - lowercase
  - Title Case
  - First letter only (Sentence casing)
- **Delimiter Transformations**:
  - Space to underscore (`_`) or hyphen (`-`)
  - Underscore to space or hyphen (`-`)
  - Hyphen to space or underscore (`_`)
- **Real-Time Preview**: Live auto-transformation as you type.
- **Convenient Utilities**: Quick one-click "Copy Result", "Swap Input/Output", and "Clear" actions.
- **Modern UI**: Clean Material-inspired design with dark/light mode support.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aadilahammad86/TextTransformerApp.git
   cd TextTransformerApp
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
python main.py
```

## 📦 Building Executable

To bundle the application into a standalone Windows executable:

```bash
pyinstaller TextTransformer.spec
```

The resulting standalone executable will be generated inside the `dist/` directory.

## 📄 License

MIT License. Feel free to use and modify!
