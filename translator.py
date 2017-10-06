#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Dmitrii Sokolov <sokolovdp@gmail.com> wrote this file. As long as you retain
# this notice you can do whatever you want with this stuff. If we meet some day,
# and you think this stuff is worth it, you can buy me a beer in return
#
# The idea of license was borrowed from Terry Yin <terry.yinzhe@gmail.com>
#    https://github.com/terryyin/google-translate-python
# ----------------------------------------------------------------------------


import requests


class Translator:
    providers = {
        'yandex': {
            "API": 'trnsl.1.1.20170327T202730Z.19970cf342c9dcee.d664d4ea0f261d94dbee40dfc005000988b22a4f',
            "URL_TRANSLATE": 'https://translate.yandex.net/api/v1.5/tr.json/translate',
            "URL_LANGUAGES": 'https://translate.yandex.net/api/v1.5/tr.json/getLangs',
            "MAX_TEXT": 10000,
        },
        'mymemory': {
            "URL_TRANSLATE": 'http://mymemory.translated.net/api/get',
            "MAX_TEXT": 500,
        }
    }
    NO_ERROR = 200
    iso_languages = ["aa", "ab", "ae", "af", "ak", "am", "an", "ar", "as", "av", "ay", "az", "ba", "be", "bg", "bh",
                     "bi", "bm", "bn", "bo", "br", "bs", "ca", "ce", "ch", "co", "cr", "cs", "cu", "cv", "cy", "da",
                     "de", "dv", "dz", "ee", "el", "en", "eo", "es", "et", "eu", "fa", "ff", "fi", "fj", "fo", "fr",
                     "fy", "ga", "gd", "gl", "gn", "gu", "gv", "ha", "he", "hi", "ho", "hr", "ht", "hu", "hy", "hz",
                     "ia", "id", "ie", "ig", "ii", "ik", "io", "is", "it", "iu", "ja", "jv", "ka", "kg", "ki", "kj",
                     "kk", "kl", "km", "kn", "ko", "kr", "ks", "ku", "kv", "kw", "ky", "la", "lb", "lg", "li", "ln",
                     "lo", "lt", "lu", "lv", "mg", "mh", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my", "na", "nb",
                     "nd", "ne", "ng", "nl", "nn", "no", "nr", "nv", "ny", "oc", "oj", "om", "or", "os", "pa", "pi",
                     "pl", "ps", "pt", "qu", "rm", "rn", "ro", "ru", "rw", "sa", "sc", "sd", "se", "sg", "si", "sk",
                     "sl", "sm", "sn", "so", "sq", "sr", "ss", "st", "su", "sv", "sw", "ta", "te", "tg", "th", "ti",
                     "tk", "tl", "tn", "to", "tr", "ts", "tt", "tw", "ty", "ug", "uk", "ur", "uz", "ve", "vi", "vo",
                     "wa", "wo", "xh", "yi", "yo", "za", "zh", "zu"]

    def __init__(self, name='yandex', langfrom='en', langto='ru'):
        if name not in self.providers.keys():
            print('error: unknown provider, valid providers are:', *list(self.providers.keys()))
            exit()
        if name == 'yandex':
            self.provider = name
            self.API = self.providers[name]['API']
            self.URL = self.providers[name]['URL_TRANSLATE']
            self.URL_X = self.providers[name]['URL_LANGUAGES']
            self.max_text = self.providers[name]['MAX_TEXT']
            self.available_languages = self._check_yandex()  # check if service is active
            self._check_lang(langfrom, langto)
            self.started = True
            self.translate = self._yandex_translate
        elif name == 'mymemory':
            self.provider = name
            self.URL = self.providers[name]['URL_TRANSLATE']
            self.max_text = self.providers[name]['MAX_TEXT']
            self._check_mymemory()  # check if service is active
            self.available_languages = self.iso_languages
            self._check_lang(langfrom, langto)
            self.started = True
            self.translate = self._mymemory_translate
        else:
            exit()

    def _check_yandex(self):
        params = dict(key=self.API, ui='ru')
        r = requests.get(self.URL_X, params=params)
        if r.status_code != self.NO_ERROR:
            print('error: translate service of {} is not active'.format(self.provider))
            exit()
        return list(r.json()['langs'].keys())

    def _yandex_translate(self, text=''):
        if self.started:
            if len(text) > self.max_text:
                print("max length of text is {} chars, text will be truncated".format(self.max_text))
                text = text[:self.max_text]
            params = dict(key=self.API, text=text, lang=self.langfrom + '-' + self.langto)
            r = requests.get(self.URL, params=params)
            if r.status_code != self.NO_ERROR:
                print(r)
                exit()
            else:
                return ' '.join(r.json()['text'])

    def _check_mymemory(self):
        params = dict(q='hello', langpair="en" + '|' + 'ru')
        r = requests.get(self.URL, params=params)
        if r.status_code != self.NO_ERROR:
            print('error: translate service of {} is not active'.format(self.provider))
            exit()

    def _mymemory_translate(self, text):
        if self.started:
            if len(text) > self.max_text:
                print("max length of text is {} chars, text will be truncated".format(self.max_text))
                text = text[:self.max_text]
            params = dict(q=text, langpair=self.langfrom + '|' + self.langto)
            r = requests.get(self.URL, params=params)
            if r.status_code != self.NO_ERROR:
                exit()
            else:
                return r.json()['responseData']['translatedText']

    def _check_lang(self, lf, lt):
        if lf in self.available_languages:
            self.langfrom = lf
        else:
            print("invalid language code:", lf)
            exit()
        if lt in self.available_languages:
            self.langto = lt
        else:
            print("invalid language code:", lt)
            exit()


def main(serv_name, tty, text, file_to, lang_from, lang_to):
    service = Translator(serv_name, lang_from, lang_to)
    new_text = service.translate(text=text)
    file_to.write(new_text)
    file_to.close()
    if tty:
        print(new_text)
    exit()


if __name__ == "__main__":
    import argparse
    import sys


    def read_text_lines(file):  # strip '\n' and spaces, plus ignore empty lines
        lines = [line for line in list(map(lambda l: l.strip(), file.readlines())) if line != '']
        file.close()
        return ''.join(lines)


    ap = argparse.ArgumentParser(description='This is a simple text translation program')

    group1 = ap.add_mutually_exclusive_group(required=True)
    group1.add_argument("--file-from", dest="file_from", action="store", type=argparse.FileType('rt', encoding='utf8'),
                        help="file with text to be translated")
    group1.add_argument("--text", dest="text", action="store",
                        help='text to be translated must be in " " quotation marks')

    ap.add_argument("--file-to", dest="file_to", action="store", default='translated_text.txt',
                    type=argparse.FileType('wt', encoding='utf8'),
                    help="file to write translated text, default: translated_text.txt")
    ap.add_argument("--copy_to_stdout", dest="tty", action="store_true", default=False,
                    help="copy translated text to standart output")
    ap.add_argument("--lang-from", dest="lfrom", action="store", default='en',
                    help="language code, default is 'en'")
    ap.add_argument("--lang-to", dest="lto", action="store", default='ru',
                    help="language code, default is 'ru'")
    ap.add_argument("--service", dest="serv", action="store", default='yandex',
                    help="translation service provider yandex or mymemory, default is yandex")

    args = ap.parse_args(sys.argv[1:])

    if args.lfrom == args.lto:
        print("languages codes must be different:", args.lfrom, args.lto)
        exit()
    if not args.text:
        args.text = read_text_lines(args.file_from)

    main(args.serv, args.tty, args.text, args.file_to, args.lfrom, args.lto)
