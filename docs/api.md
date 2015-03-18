# Авторизация

Авторизация осуществляется путем передачи параметров *client* и *token* в заголовке HTTP-запроса. Набор допустимых пар
client-token задается в файле конфигурации *owl/settings.py*

# Загрузка файла

Запрос:

		URL: /api/files
		Method: POST

Параметры:

		file — отправляемый файл
		watermark — (1/0, необязательный, по-умолчанию 0) накладывать ли водяной знак

Ответ:

		{
			output_file: "9/6/4.jpeg"
			result: true
		}

# Получение файлов

Запрос:

		URL: /api/files
		Method: GET

Параметры:

		r — строка, содержащая список запрашиваемых файлов с фильтрами через запятую
			Пример: 8/0/4.jpeg:w50h70,c/d/test__Kopiya_4.jpeg:w150h150fill|sat60
			Фильтр начинается через двоеточие после имени файла.
			Разные фильтры отделяются друг от друга вертикальной чертой

		force — (1/0, необязательный, по-умолчанию 0) сбрасывать ли закешированные изображения
			перед созданмем новых.

Ответ:

		{
			0: {
				request_filters: "w50h70"
				request_file: "8/0/4.jpeg"
				result: false
				err_code: 303
			}
			1: {
				request_filters: "w150h150fill|sat60"
				request_file: "c/d/test__Kopiya_4.jpeg"
				result: true
				output_filesize: 8747
				output_file: "cache/c/d/test__Kopiya_4.jpeg/w150h150fill|sat60.jpeg"
			}
        }

# Удаление файлов

Запрос:

		URL: /api/files
		Method: DELETE

Параметры:

		r — строка, содержащая список удаляемых файлов через запятую
			Пример: 9/6/4.jpeg

Ответ:

		{
			0: {
				request_file: "9/6/4.jpeg"
				result: true
			}
		}