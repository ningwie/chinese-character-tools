# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import io
import time
import random
import math
import sys
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

INPUT_FILE = 'input.txt'
OUTPUT_LOG = 'output.txt'
OUTPUT_RAW_PATH = './out/raw/'
OUTPUT_REAL_PATH = './out/result/'

ITEMS_PER_BLOCK = 20
WAIT_BETWEEN_BLOCKS = 90 # seconds
WAIT_BETWEEN_ITEMS = 8 # seconds
RANDOM_PERCENT = 0.25 # variation in percent [0-1]

TIMEOUT_WAIT = 20 # max number of seconds to wait for page to load

MUST_CONTAIN = '：，（）' # if item doesn't contain all, warning

def read_chars_textfile(path):
    output = []
    with io.open(path, mode='r', encoding='utf-8') as txt_file:
        for line in txt_file:
            line = line.strip()
            if line == '':
                continue
            char = line.split(',')[0]
            output.append(char)
    return output

def write_output(path, output):
    with io.open(path, mode='w', encoding='utf-8') as txt_file:
        txt_file.write(output)

def write_log(char, code):
    with io.open(OUTPUT_LOG, mode='a', encoding='utf-8') as txt_file:
        txt_file.write(char + ',' + code + '\n')

def randomize_no(no, integer=False):
    margin = RANDOM_PERCENT * no
    random_margin = (random.random() * 2 * margin) - margin
    if integer:
        return int(no + random_margin)
    else:
        return (no + random_margin)

def main():
    input_chars_raw = read_chars_textfile(INPUT_FILE)
    input_chars = []
    try:
        previous_output = set(read_chars_textfile(OUTPUT_LOG))
    except IOError:
        previous_output = set()
        with io.open(OUTPUT_LOG, mode='w', encoding='utf-8') as txt_file:
            txt_file.write('')
    for char in input_chars_raw:
        if char in previous_output:
            continue
        if not char in input_chars:
            input_chars.append(char)

    print(str(len(input_chars)) + ' unique characters to scrape')
    chars_per_minute = (ITEMS_PER_BLOCK * 60) / ((ITEMS_PER_BLOCK *
        WAIT_BETWEEN_ITEMS) + WAIT_BETWEEN_BLOCKS)
    print(str(chars_per_minute) + ' characters per minute')
    print(str((1.0 / chars_per_minute) * len(input_chars) / 60.0) +
            ' hours, at least')

    print('starting firefox...')
    browser = webdriver.Firefox()

    block_count = 0
    block_size = randomize_no(ITEMS_PER_BLOCK, integer=True)
    previous = None

    for i, char in enumerate(input_chars):
        previous_output = set(read_chars_textfile(OUTPUT_LOG))
        if char in previous_output:
            continue
        print('scraping: ' + char)
        try:
            out_raw, out_real, previous, warning = sinica(
                    char, previous, browser)
        except TimeoutException:
            sys.exit('cant load page, exiting ...')
        if out_real == 'notfound':
            write_log(char, 'notfound')
        else:
            write_output(OUTPUT_RAW_PATH + char + '.html', out_raw)
            write_output(OUTPUT_REAL_PATH + char + '.csv', out_real)
            if warning:
                write_log(char, 'warning')
            else:
                write_log(char, 'ok')

        block_count += 1
        if block_count >= block_size:
            block_count = 0
            block_size = randomize_no(ITEMS_PER_BLOCK, integer=True)
            print('block completed, sleeping...')
            time.sleep(randomize_no(WAIT_BETWEEN_BLOCKS))
        else:
            time.sleep(randomize_no(WAIT_BETWEEN_ITEMS))

    browser.quit()
    print('DONE')

def sinica(char, previous, browser):
    PAGE = 'http://xiaoxue.iis.sinica.edu.tw/'
    browser.get(PAGE)
    input_box = browser.find_element_by_id('EudcFontChar')
    input_box.send_keys(char)
    input_box.send_keys(Keys.RETURN)

    # wait for element in new content
    def until_func(b):
        if not b.find_element_by_id('HiddenFrom'):
            return false
        input_box = browser.find_element_by_id('EudcFontChar')
        current = input_box.get_attribute('value')
        if current == previous:
            return false
        else:
            return current

    element = WebDriverWait(browser, TIMEOUT_WAIT).until(until_func)
    current = until_func(browser)

    whole_page = browser.page_source

    content = browser.find_element_by_id('PageResult')
    content = content.get_attribute('innerHTML')

    if '查無資料' in content:
        return whole_page, 'notfound', current

    start_index = content.rfind('<ul style="width: 95%">')
    end_index = content.rfind('</ul>')
    content = content[start_index:end_index]
    content = content.split('<li>')
    csv_out = []
    warning = False
    if len(content) <= 1:
        warning = True
    for item in content[1:]:
        text = item.strip()
        text = text.strip('</li>')
        for c in MUST_CONTAIN:
            if not c in text:
                warning = True
        text = char + ',' + text
        csv_out.append(text)

    csv_out = '\n'.join(csv_out)
    return whole_page, csv_out, current, warning

if __name__ == '__main__':
    main()
