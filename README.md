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
python -m streamstats analyze INPUT --format csv|jsonl Report.json
python -m streamstats analyze INPUT --format csv|jsonl --skip-invalid
```

## Ошибки анализатора - переписать классы ошибок на названия

- `StreamStatsError` - родительский класс ошибок
- `UnsupportedFormatError` - 
- `InvalidEventError` -
- `InvalidTimestampError` -
- `CLIConfigError` -
- `InvalidDelimiterError` -
- `UnmatchedFormatError` -
- `` -

## Структура проекта

lab_02_analyzer\
    files\

    reports\

    src\
        streamstats\
            __init__.py
            __main__.py
            analysis.py
            errors.py
            models.py
            parsers.py
            report.py
    tests\



## Установка и создание виртуального окружения

```bash
git clone https://github.com/IarKri/MAI_1COURSE_2LAB_ANALYZER
cd lab_02_analyzer
python -m venv venv
venv/Scripts/activate
pip install -e
```