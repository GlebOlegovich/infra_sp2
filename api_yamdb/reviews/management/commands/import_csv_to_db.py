import os
import datetime as dt
from tqdm import tqdm
import csv
from django.core.management.base import BaseCommand

from ._settings_for_import import DIR_CSV, NEED_TO_PARSE, TIME_FORMAT


class Command(BaseCommand):

    def _read_and_write_to_DB(self, file, Model):
        file_name = str(os.path.join(DIR_CSV, file))
        with open(file_name, encoding='utf-8') as r_file:
            # Создаем объект reader, указываем символ-разделитель ","
            file_reader = csv.reader(r_file, delimiter=",")
            # Счетчик для подсчета количества строк и вывода заголовка столбцов
            count = 0
            # Считывание данных из CSV файла
            index_of_date = None
            for row in file_reader:
                if count == 0:
                    fields = row
                    # if 'pub_date' in row:
                    try:
                        index_of_date = row.index('pub_date')
                    except Exception:
                        pass

                else:
                    # Так не работает, приходится котстыль делать,который ниже,
                    # с еще одним save
                    # if index_of_date is not None:
                    #     time_str = row[index_of_date]
                    #     time_dt_obj = dt.datetime.strptime(
                    #         time_str,
                    #         TIME_FORMAT
                    #     )
                    #     row[index_of_date] = time_dt_obj
                    data = dict(zip(fields, row))
                    obj, _ = Model.objects.get_or_create(**data)
                    if index_of_date is not None:
                        time_str = row[index_of_date]
                        time_dt_obj = dt.datetime.strptime(
                            time_str,
                            TIME_FORMAT
                        )
                        obj.pub_date = time_dt_obj
                        obj.save()
                count += 1
            print(f'    Добавлено {count} записей в {Model} из {file}')

    def handle(self, *args, **options):
        for file, model in tqdm(NEED_TO_PARSE.items()):
            print(file, model, sep=' - ')
            self._read_and_write_to_DB(file, model)
