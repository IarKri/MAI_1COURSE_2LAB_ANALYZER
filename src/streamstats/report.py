import json


def report(statistics, output_file):
    '''
    Формирует report и записывает файл или выводит в терминал

    Args:
        statistics: статистика из проанализированных файлов

        output_file: файл, в который надо записать report
    '''
    statistics = json.dumps(statistics, indent=2)
    if output_file:
        with open(f"reports/{output_file}", "w", encoding="utf-8") as json_file:
            json_file.write(statistics)
    else:
        print(statistics)
