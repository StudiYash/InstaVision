# InstaVision Project Structure

This document maps the repository for new users, students, contributors, recruiters, and technical reviewers.

## High-Level Hierarchy

```text
InstaVision/
|-- Certificates/
|   |-- Project Copyright/
|   `-- Project Representation/
|-- Project Backend/
|   |-- Image Generation Models/
|   `-- Image Editing Models/
|-- Project Frontend/
|   |-- Main Page/
|   |-- Image Generation/
|   `-- Image Editing/
|-- Project Real-life Usage/
|   |-- Alampata 2024/
|   `-- VoltzFest 2025/
|-- Project Telegram Bot/
|   |-- InstaVision_Telegram_Bot.py
|   |-- Telegram Bot Individual Models/
|   `-- Support Files/
|-- Project Test Inputs/
|-- Project Windows Application/
|-- requirements/
|   |-- frontend.txt
|   |-- backend.txt
|   |-- telegram-main.txt
|   |-- telegram-individual.txt
|   |-- dev.txt
|   `-- all-components.txt
|-- scripts/
|   `-- check_setup.py
|-- tests/
|   |-- test_repository_structure.py
|   |-- test_env_template.py
|   |-- test_requirements_files.py
|   |-- test_setup_checker.py
|   |-- test_path_portability.py
|   `-- test_import_safety.py
|-- runtime_outputs/              # generated locally and ignored by git
|-- Support Files/
|-- README.md
|-- requirements.txt
|-- LOCAL_SETUP_GUIDE.md
|-- PROJECT_STRUCTURE.md
|-- CONFIGURATION.md
|-- COMPONENT_RUN_GUIDE.md
|-- TROUBLESHOOTING.md
|-- .env.example
`-- .gitignore
```

## Root Files

- `README.md`: Main project story, methodology, showcase, links, license, and high-level project context.
- `LICENSE`: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CLA.md`, `CONTRIBUTORS.md`: Community and contribution documents.
- `InstaVision Logo.png`, `InstaVision Logo 2.png`: Root project logos.
- `.env.example`: Template for local configuration values.
- `.gitignore`: Safe ignore rules for local runtime outputs and secrets.
- `requirements.txt`: Convenience installer for all Python-based project components.
- `requirements/`: Component-specific dependency files for frontend, backend, Telegram, and development workflows.
- `scripts/check_setup.py`: Local setup validator that inspects structure, configuration, dependencies, and runtime folders without running project components.
- `tests/`: Lightweight pytest smoke tests for repository structure, configuration, requirements, setup checker behavior, path portability, and import safety.
- `runtime_outputs/`: Created locally by supported backend and Telegram components for generated files, watermarked files, uploads, metrics, and model-specific output copies.

## Project Backend

`Project Backend/` contains standalone backend/model scripts.

- `Image Generation Models/`: Replicate-based text-to-image model scripts and README.
- `Image Editing Models/`: Replicate-based image editing model scripts and README.

Runnable components: yes. Each Python file is an individual model script.

Documentation/assets: README files explain model lists and basic setup.

## Project Frontend

`Project Frontend/` contains desktop UI scripts and visual assets.

- `Main Page/`: Main navigation UI script, logo, screenshot, README.
- `Image Generation/`: Image generation UI script, logo, screenshot, README.
- `Image Editing/`: Image editing UI script, logo, screenshot, README.
- `InstaVision UI.drawio`: UI design/source diagram.

Runnable components: yes. The Python files are Tkinter-based UI scripts.

## Project Telegram Bot

`Project Telegram Bot/` contains the main Telegram bot and individual model bot components.

- `InstaVision_Telegram_Bot.py`: Main multi-model Telegram bot.
- `requirements.txt`: Main Telegram bot dependency file.
- `Telegram Bot Individual Models/`: Separate DALL-E 3, Flux Schnell, Google Imagen3, and SDXL Lightning bot folders.
- `Support Files/`: Folder-specific support READMEs.

Runnable components: yes. The main bot and individual bot scripts are available runtime components.

## Project Windows Application

`Project Windows Application/` contains the packaged Windows project interface.

- `InstaVision.exe`: Windows executable.
- Installer screenshots and app screenshots.
- `README.md`: Installation guide and app overview.

Runnable component: yes. This is an available project interface.

## Project Real-life Usage

`Project Real-life Usage/` contains event-tested usage history.

- `Alampata 2024/`: Event report and generated images.
- `VoltzFest 2025/`: Event report and generated images.
- `README.md`: Event usage summary.

Runnable components: no. These files are showcase and evidence assets and should be preserved.

## Project Test Inputs

`Project Test Inputs/` contains prompt text files for testing and comparing model behavior.

Runnable components: no. These are input examples for experiments and demos.

## Certificates

`Certificates/` contains project representation certificates and copyright material.

Runnable components: no. These are important project showcase and ownership documents.

## Support Files

`Support Files/` contains methodology visuals, supported language document, Mark Model Index PDF, and introduction media.

Runnable components: no. These are documentation and showcase assets.
