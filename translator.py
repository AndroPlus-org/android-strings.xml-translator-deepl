import xml.etree.ElementTree as ElementTree
import os
import time
import requests

# MIT License

# Copyright (c) 2018 Cuneyt AYYILDIZ

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# run as "python3 translator.py"

API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx:fx'

INFILE = input("Enter strings.xml file path") or "./data/strings.xml"
INPUTLANGUAGE = input("Enter input language, such as (EN, JA)") or "ZH"
OUTPUTLANGUAGE = input("Enter output language(s), such as: tr or (EN, JA)") or "JA"

default_output_languages = ['JA']


def create_directory_if_not_exists(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def create_directories(dir_language):
    create_directory_if_not_exists("translated")

    file_directory = "translated/" + "values-" + dir_language.lower()

    create_directory_if_not_exists(file_directory)
    return file_directory

languages_from_translate = INPUTLANGUAGE
languages_to_translate = OUTPUTLANGUAGE.split(",")

if INFILE is None:
    INFILE = "strings.xml"

if OUTPUTLANGUAGE:
    if len(languages_to_translate) == 0:
        languages_to_translate = [OUTPUTLANGUAGE.strip()]
else:
    languages_to_translate = default_output_languages

for language_name in languages_to_translate:
    language_to_translate = language_name.strip()

    translated_file_directory = create_directories(language_to_translate)
    print(" -> " + language_to_translate + " =========================")

    tree = ElementTree.parse(INFILE)
    root = tree.getroot()
    for i in range(len(root)):

        if 'translatable' not in root[i].attrib:
            value = root[i].text

            if value is not None:
                params = {
                    'auth_key' : API_KEY,
                    'text' : value,
                    'source_lang' : languages_from_translate,
                    "target_lang": language_to_translate
                }
                request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
                result = request.json()
                root[i].text = result["translations"][0]["text"].strip()
                print(value + "-->" + root[i].text)
                time.sleep(0.3)

    translated_file = translated_file_directory + "/strings.xml"

    tree.write(translated_file, encoding='utf-8')
