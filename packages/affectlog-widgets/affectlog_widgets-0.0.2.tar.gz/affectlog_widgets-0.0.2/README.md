# AffectLog Widgets

This repository contains the `affectlog-widgets` library, which is used for creating interactive, visual Responsible AI tools. This project provides a set of widgets for model assessment, fairness analysis, error detection, and more, built on top of machine learning frameworks.

## Requirements for Development

To contribute to `affectlog-widgets`, make sure to install the following dependencies.

### Testing Dependencies

For running tests with code coverage and mocking, use the following:

```bash
pytest==7.0.1
pytest-cov
pytest-mock==3.6.1
```

### Parser Dependencies

For parsing requirements, use:

```bash
requirements-parser==0.2.0
```

### Package Building

Ensure you have the necessary tools for building the package:

```bash
wheel
```

### Machine Learning & Fairness Libraries

Install the following libraries to enable machine learning and fairness evaluation tools:

```bash
fairlearn==0.7.0
ml-wrappers>=0.4.0
sktime
pmdarima
```

**Note**: For Windows users running Python 3.7, add the following fix for `joblib` compatibility:

```bash
joblib<1.3.0; python_version <= '3.7' and sys_platform == 'win32'
```

### Notebook Testing

To test notebooks and perform notebook validation, install:

```bash
nbformat
papermill
scrapbook
jupyter
nbval
```

### Documentation Dependencies

For generating documentation, install the following:

```bash
docutils<=0.19
sphinx==5.0.2
sphinx-gallery==0.10.0
pydata-sphinx-theme==0.7.2
```

## Setting up the Development Environment

Follow these steps to set up your local development environment:

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd affectlog-widgets
    ```

2. **Install Dependencies**:
    You can install all dependencies via pip:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run Tests**:
    To ensure everything is working, run the tests:
    ```bash
    pytest
    ```

## Local Installation

For local development, ensure that `trustworthyai` is available in your project. You can use the relative path for local development:

```bash
../trustworthyai/.
```

Add this path when running your local environment so the necessary modules can be accessed.

## Contributing

If you're interested in contributing, please create a feature branch from `main`, make your changes, and open a pull request. Ensure that all tests pass and documentation is updated where necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.