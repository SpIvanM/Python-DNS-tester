# Python-DNS-tester
A script that allows testing DNS servers for their speed and the degree of blocking of malicious websites

# DNS Analyzer Script

## Project Overview

The DNS Analyzer script is a Python-based tool designed to evaluate the performance and blocking capabilities of various DNS over HTTPS (DoH) resolvers against a categorized list of domain names. The primary goal is to help users identify fast and balanced DNS resolvers that align with their desired level of content filtering.

It performs concurrent DoH queries, measures query latencies, and determines if domains are blocked based on criteria such as NXDOMAIN responses, resolution to non-routable IPs, or known blocking IPs. The results are compiled into a comprehensive Excel report, providing both a high-level overview and detailed per-resolver statistics, including:

*   **DNS Matrix:** A visual representation of which DNS resolver blocks which domain.
*   **Performance Statistics:** Minimum, maximum, median, and average query latencies for resolved domains.
*   **Error Rate:** Percentage of queries resulting in technical errors.
*   **Overall Blocking Statistics:** Percentage of domains blocked by each resolver.
*   **Categorized Blocking:** Blocking percentages for 'Useful', 'Questionable', and 'Useless' domain categories.
*   **Detailed Lists:** Specific lists of 'Useful' domains that were blocked, 'Useless' domains that were blocked, and 'Useless' domains that were allowed (resolved).

This tool empowers users to make informed decisions when selecting a DoH resolver, balancing speed with content filtering needs.

## Deployment Instructions

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone or Download the Project:** Clone this repository or download the source code to your desired directory.

2.  **Install Dependencies:** Navigate to the project directory and run:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Create Configuration Files:**
    *   **`resolvers.txt` (Required):** Create a plain text file named `resolvers.txt` in the project directory. Each line should contain a valid DoH resolver URL.
        Example `resolvers.txt`:
        ```
        https://1.1.1.1/dns-query
        https://dns.google/dns-query
        https://cloudflare-dns.com/dns-query
        https://doh.opendns.com/dns-query
        https://dns.adguard.com/dns-query
        ```
    *   **`domains.txt` (Optional):** If you wish to provide additional domains beyond the built-in list, create a plain text file named `domains.txt`. Each line should contain one domain name.
        Example `domains.txt`:
        ```
        example.com
        testdomain.org
        anotherdomain.net
        ```
    *   **`custom_blocking_ips.txt` (Optional):** If you want to include specific IP addresses as blocking indicators, create a plain text file named `custom_blocking_ips.txt`. Each line should contain one IPv4 address.
        Example `custom_blocking_ips.txt`:
        ```
        1.2.3.4
        8.8.4.4
        ```

### Usage

Run the script from your terminal using Python.

```bash
python cli/main.py --resolvers resolvers.txt [OPTIONS]
```

#### Command-Line Arguments

- `--resolvers <path/to/resolvers.txt>` (Required): Path to the text file containing DoH resolver URLs.
- `--domains <path/to/domains.txt>` (Optional): Path to a text file containing additional domain names (one per line). If not provided, a hardcoded list expanded to 100 domains is used.
- `--output <filename.xlsx>` (Optional): Path for the output Excel report. Defaults to `dns_analysis_report.xlsx`.
- `--concurrency <number>` (Optional): Maximum number of concurrent DoH queries. Defaults to 20.
- `--timeout <seconds>` (Optional): Timeout in seconds for each individual DoH query. Defaults to 5.0 seconds.
- `--custom-blocking-ips <path/to/custom_blocking_ips.txt>` (Optional): Path to a text file containing user-defined specific blocking IPv4 addresses (one per line).

#### Example Commands

Basic run with default settings (using resolvers.txt):

```bash
python cli/main.py --resolvers resolvers.txt
```

Run with custom domain list and output file:

```bash
python cli/main.py --resolvers resolvers.txt --domains my_domains.txt --output custom_report.xlsx
```

Run with increased concurrency and custom blocking IPs:

```bash
python cli/main.py --resolvers resolvers.txt --concurrency 50 --custom-blocking-ips my_block_ips.txt
```

After execution, an Excel file (e.g., `dns_analysis_report.xlsx`) will be generated in the same directory, containing the comprehensive analysis.

---

# Описание проекта на русском

## Как работает проект

Проект **Python-DNS-tester** представляет собой инструмент для тестирования DNS-серверов (резолверов) на основе протокола DNS over HTTPS (DoH). Основная цель — оценить скорость работы резолверов и степень блокировки вредоносных или нежелательных доменов.

### Архитектура проекта

Проект построен по модульной архитектуре, где каждый модуль отвечает за определённую функциональность:

- **`cli/`** — интерфейс командной строки. Основной файл `main.py` является точкой входа, которая оркестрирует весь процесс анализа. Он парсит аргументы командной строки, загружает конфигурации и запускает анализ.
  
- **`config/`** — модули для загрузки конфигураций:
  - `domain_loader.py` — загружает список доменов для тестирования (встроенные и пользовательские).
  - `resolver_loader.py` — загружает список DoH-резолверов из файла.
  - `blocking_ips.py` — загружает IP-адреса и диапазоны, которые считаются признаками блокировки.
  - `settings.py` — общие настройки проекта.

- **`dns_client/`** — клиент для выполнения DoH-запросов. `doh_client.py` отправляет асинхронные запросы к резолверам и измеряет время отклика.

- **`data/`** — хранение данных. `query_store.py` сохраняет результаты всех запросов для дальнейшего анализа. `models.py` определяет структуры данных (например, `QueryResult`).

- **`analysis/`** — анализ результатов:
  - `blocking_detector.py` — определяет, заблокирован ли домен (на основе NXDOMAIN, не маршрутизируемых IP или известных блокирующих IP).
  - `statistics_analyzer.py` — рассчитывает статистику производительности (минимальное, максимальное, среднее время) и блокировки (процент заблокированных доменов по категориям).
  - `models.py` — модели данных для анализа.

- **`utils/`** — утилиты:
  - `excel_generator.py` — генерирует отчёт в формате Excel с матрицей блокировки, статистикой и детальными списками.
  - `ip_utils.py` — вспомогательные функции для работы с IP-адресами.

- **`dns_analyzer_script.py`** — это отдельный файл, который, по-видимому, содержит альтернативную реализацию анализа в одном скрипте (без модульной структуры). Он может быть использован как пример монолитного подхода.

### Процесс работы

1. **Загрузка конфигураций:** Программа загружает список доменов (категоризированных как "Useful", "Questionable", "Useless"), резолверов и блокирующих IP.

2. **Выполнение запросов:** Для каждой комбинации домен + резолвер отправляется DoH-запрос. Запросы выполняются асинхронно с ограничением concurrency для избежания перегрузки.

3. **Анализ результатов:** Для каждого ответа проверяется, заблокирован ли домен. Рассчитывается время отклика и другие метрики.

4. **Генерация отчёта:** Результаты компилируются в Excel-файл с:
   - Матрицей блокировки (какой резолвер блокирует какой домен).
   - Статистикой производительности.
   - Процентом блокировки по категориям доменов.
   - Списками заблокированных полезных доменов, заблокированных бесполезных и пропущенных бесполезных.

### Можно ли собрать всё в один основной Python-скрипт?

Да, технически возможно собрать всю функциональность в один файл, импортируя или копируя код из модулей. Файл `dns_analyzer_script.py` может быть попыткой такого подхода, но он кажется неполным. Однако это не рекомендуется по следующим причинам:

- **Модульность упрощает поддержку и расширение:** Разделение на модули позволяет легко изменять отдельные части (например, добавить новый тип анализа) без влияния на остальной код.
- **Переиспользование:** Модули можно импортировать в другие проекты.
- **Читаемость:** Один большой файл сложно поддерживать.
- **Тестирование:** Модульная структура облегчает написание unit-тестов.

Если вы хотите создать один скрипт, вы можете скопировать содержимое всех модулей в один файл, но лучше оставить текущую структуру. Основной "скрипт с ссылками" — это `cli/main.py`, который импортирует все необходимые модули и запускает процесс.

### Запуск

Основная команда для запуска:

```bash
python cli/main.py --resolvers resolvers.txt
```

Это импортирует все модули и выполняет анализ.
