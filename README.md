# django-opencrm

[![Python Linting](https://github.com/JonneSaloranta/django-opencrm/actions/workflows/linting.yml/badge.svg?branch=master)](https://github.com/JonneSaloranta/django-opencrm/actions/workflows/linting.yml)

**django-opencrm** is a reusable Django CRM app designed for NGOs and small businesses. It provides a flexible CRM system that can be integrated into any Django project to manage co   ntacts, organizations, and related workflows.

---

## Features

- Manage contacts, organizations, and interactions
- Configurable settings via `python-decouple`
- Fully compatible with Django 5.x
- Easy integration into existing Django projects

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/JonneSaloranta/django-opencrm.git
cd django-opencrm
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

We use **pip-tools** to manage dependencies:

```bash
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

---

## Usage

1. Add `opencrm` to your `INSTALLED_APPS` in Django:

```python
INSTALLED_APPS = [
    ...
    "opencrm",
]
```

2. Run migrations:

```bash
python manage.py migrate opencrm
```

3. Start using the CRM models in your project.

---

## Development

We follow these development practices:

- **Code formatting:** [Black](https://black.readthedocs.io/en/stable/)
- **Linting:** [Flake8](https://flake8.pycqa.org/en/latest/)
- **Testing:** [pytest](https://docs.pytest.org/en/latest/)
- **Pre-commit hooks** to enforce formatting and linting

Run tests:

```bash
pytest
```

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on setup, workflow, and commit message guidelines.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Contact

Created by Jonne Saloranta.  
For questions or suggestions, open an issue on GitHub.
