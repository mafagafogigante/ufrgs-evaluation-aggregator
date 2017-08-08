import PyPDF2
import urllib.error
import urllib.request
import os
import sys
import logging

sources_url = 'http://www.ufrgs.br/sai/dados-resultados/painel-qualidade/dados-2016-1/serie-historica-discente/curso/'
sources_root = './sources'


def ensure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == os.errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def ensure_sources_root_exists():
    ensure_path_exists(sources_root)


def initialize_sources(logger):
    ensure_sources_root_exists()
    # Download all XX.pdf until we get a 404.
    logger.info('Started downloading data files...')
    for i in range(1, 100):
        filename = '{:02}.pdf'.format(i)
        full_url = sources_url + filename
        source_path = os.path.join(sources_root, filename)
        urllib.request.urlretrieve(full_url, source_path)
        try:
            urllib.request.urlretrieve(full_url, source_path)
        except urllib.error.HTTPError:
            downloaded = i - 1
            logger.info('Stopped after downloading {} file{}.'.format(downloaded, '' if downloaded else's'))
            break
        except:
            logger.error('Unhandled exception!')
            raise
    logger.info('Finished downloading data files.')


class Aggregate():
    def __init__(self):
        self.data = {}

    def append(self, course, indicator, date, value):
        pass


def extract_text(pdf_filename):
    with open(pdf_filename, 'rb') as file_handle:
        reader = PyPDF2.PdfFileReader(file_handle)
        contents = reader.getPage(0).extractText().split('\n')
        return contents


def make_logger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger


if __name__ == '__main__':
    logger = make_logger('log.txt')
    initialize_sources(logger)