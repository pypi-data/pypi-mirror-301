import xml.etree.ElementTree as ET
from googletrans import Translator
import logging
import re
import sys

# Android App Translator.
# Author: Mawiya
# Email: mawiya@outlook.be
# Install: pip3 install googletrans==4.0.0-rc1
# Usage: python3 translate.py <input_file> <output_file> <target_language>

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

def parse_strings_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    strings = {}

    for string in root.findall('string'):
        key = string.get('name')
        value = string.text
        is_cdata = isinstance(value, str) and value.startswith("<![CDATA[") and value.endswith("]]>")
        if is_cdata:
            value = value[9:-3]  # Remove CDATA wrapping
        strings[key] = {'value': value, 'is_cdata': is_cdata}

    return strings, tree

def escape_apostrophes(text):
    return re.sub(r"(?<!\\)'", r"\\'", text)

def translate_strings(strings, target_lang):
    translator = Translator()
    translated_strings = {}

    logging.info(f"Translating to {target_lang}")

    for key, string_data in strings.items():
        value = string_data['value']
        is_cdata = string_data['is_cdata']
        
        if value:
            try:
                translated_value = translator.translate(value, dest=target_lang).text
                translated_value = escape_apostrophes(translated_value)

                if is_cdata:
                    translated_value = f"<![CDATA[{translated_value}]]>"

                translated_strings[key] = translated_value
                logging.info(f"Word: {value} >> {translated_value}")
            except Exception as e:
                logging.error(f"Error translating word: {value} | Error: {str(e)}")
                translated_strings[key] = value  # Keep original value if translation fails
        else:
            translated_strings[key] = value  # Keep empty strings as-is

    return translated_strings

def update_strings_xml(tree, translated_strings, output_file_path):
    root = tree.getroot()

    for string in root.findall('string'):
        key = string.get('name')
        if key in translated_strings:
            string.text = translated_strings[key]

    # Write out the updated XML to the output file
    ET.ElementTree(root).write(output_file_path, encoding='utf-8', xml_declaration=True)

    # Fix any CDATA encoding issues in the output
    with open(output_file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        content = content.replace('&lt;![CDATA[', '<![CDATA[').replace(']]&gt;', ']]>')
        f.seek(0)
        f.write(content)
        f.truncate()

    logging.info(f"-----------------------\nTranslator by Mawiya\nTranslation Saved to  {output_file_path}")

def main():
    if len(sys.argv) != 4:
        logging.error("\n\n------\nNo Arg Passed Please Read below.\nUsage: apptranslate  <input_file> <output_file> <language_code>\nExample: apptranslate strings.xml string-en.xml en\nAuthor: Mawiya \nEmail: mawiya@outlook.be\n")
        sys.exit(1)

    input_file = sys.argv[1]  # Input file from command-line arguments
    output_file = sys.argv[2]  # Output file from command-line arguments
    target_language = sys.argv[3]  # Target language from command-line arguments

    logging.info("\n\nStarting Translator.\n---------------------------\nAndroid App Translator\nAuthor: Mawiya\nProject: okFlix\nEmail: mawiya@outlook.be\n--------------------\n\n")
    strings, tree = parse_strings_xml(input_file)
    logging.info(f"Found {len(strings)} strings to translate.")
    translated_strings = translate_strings(strings, target_lang=target_language)
    update_strings_xml(tree, translated_strings, output_file)

if __name__ == '__main__':
    main()
