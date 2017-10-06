## Translate
Simple CLI offline translate program

## Usage
```
usage: translator.py [-h] (--file-from FILE_FROM | --text TEXT)
                     [--file-to FILE_TO] [--copy_to_stdout]
                     [--lang-from LFROM] [--lang-to LTO] [--service SERV]

This is a simple text translation program

optional arguments:
  -h, --help            show this help message and exit
  --file-from FILE_FROM
                        file with text to be translated
  --text TEXT           text to be translated must be in " " quotation marks
  --file-to FILE_TO     file to write translated text, default:
                        translated_text.txt
  --copy_to_stdout      copy translated text to standart output
  --lang-from LFROM     language code, default is 'en'
  --lang-to LTO         language code, default is 'ru'
  --service SERV        translation service provider yandex or mymemory,
                        default is yandex
```