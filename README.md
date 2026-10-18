# Analyzer

Анализатор csv и jsonl файлов с валидацией обязательных полей

## Описание

Основной инструмент проекта:

- **Анализатор** - сбор статистики с поступающих на вход csv и jsonl файлов.

    - **Пример статистики**
        `total_events`: 15,
        `events_by_level`: 
            "INFO": 4,
            "ERROR": 5,
            "WARNING": 2,
            "CRITICAL": 3,
            "DEBUG": 1
        
        `events_by_source`: 
            "api": 4,
            "database": 4,
            "worker": 3,
            "auth": 2,
            "server": 2
        
        `top_error_sources`: 
            "api": 4,
            "database": 4,
            "worker": 3,
            "auth": 2,
            "server": 2
        
        `first_timestamp`: "2026-10-13T11:55:00",
        `last_timestamp`: "2026-10-13T13:00:00"
    
    - `total_events` - общее количество проанализированных событий

    - `events_by_level` - количество проанализированных событий с определенным level

    - `events_by_source` - количество проанализированных событий с определенным source

    - `top_error_source` - 5 самых частых sorce, с которых пришли событыя с level.ERROR или level.CRITICAL

    - `first_timestamp` - время самого раннего события

    - `last_timestamp` - время самого позднего события

## Основные команды

```bash
python -m streamstats analyze INPUT --format csv|jsonl
python -m streamstats analyze INPUT --format csv|jsonl --output Report.json
python -m streamstats analyze INPUT --format csv|jsonl --skip-invalid
```
- `analyze` - анализирует поступившие на вход файлы csv и jsonl
- `--format` - указывает на формат анализируемого файла
- `--output` - создается кастомный файл в папке Reports, в который будет записан отчет
- `--skip-invalid` - при наличии этой команды, строки с ошибками будут записываться в лог.
                     Программа при этом проанализирует файлы до конца, не включив ошибочные события в подсчет

## Ошибки анализатора 

- `StreamStatsError` - родительский класс ошибок (используется для общего отлавливания оишбок)
- `UnsupportedFormatError` - Тип файла не поддерживается анализатором
- `InvalidEventError` - Ошибка анализируемого события
- `InvalidTimestampError` - Ошибка записи timestamp
- `CLIConfigError` - Ошибка записи аргументов командной строки
- `InvalidDelimiterError` - Использование недопустимого разделителя
- `UnmatchedFormatError` - Несовместимость файла и соотвественного ему аргумента из --format


## Структура проекта

lab_02_analyzer\
    reports\
    src\
        streamstats\
            __init__.py
            __main__.py
            analysis.py
            constants.py
            errors.py
            models.py
            parsers.py
            report.py
    tests\
        several_files_test.py
        test_cli.py
        test_empty_files.py
        unit_test.py
    tests_invalid_data\
        data_for_parser_skip_invalid.csv
        data_for_parser_skip_invalid.jsonl
        skip_invalid_test_large.csv
        skip_invalid_test_large.jsonl
    tests_valid_data\
        data_for_unicode-test.csv
        data_for_unicode-test.jsonl
    pyproject.toml
    README.md


## Установка и создание виртуального окружения

```bash
git clone https://github.com/IarKri/MAI_1COURSE_2LAB_ANALYZER
cd lab_02_analyzer
python -m venv venv
venv/Scripts/activate
pip install -e
```