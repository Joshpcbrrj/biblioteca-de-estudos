"""images.py: free-license photos from Wikimedia Commons and screenshots of the book's application."""
import sys
import types

import images
import pytest

ENIAC = {
    'title': 'File:Eniac.jpg', 'imageinfo': [{
        'thumburl': 'https://upload.wikimedia.org/eniac-1280.jpg', 'mime': 'image/jpeg', 'width': 1280,
        'height': 960, 'descriptionurl': 'https://commons.wikimedia.org/wiki/File:Eniac.jpg',
        'extmetadata': {'LicenseShortName': {'value': 'Public domain'},
                        'Artist': {'value': '<a href="x">U.S. Army</a> Photo'},
                        'LicenseUrl': {'value': ''}}}]}
LOGO = {
    'title': 'File:Some logo.png', 'imageinfo': [{
        'thumburl': 'https://upload.wikimedia.org/logo.png', 'mime': 'image/png', 'width': 400, 'height': 400,
        'descriptionurl': 'https://commons.wikimedia.org/wiki/File:Some_logo.png',
        'extmetadata': {'LicenseShortName': {'value': 'Logo'}, 'NonFree': {'value': 'true'}}}]}
HOPPER = {
    'title': 'File:Grace Hopper.jpg', 'imageinfo': [{
        'thumburl': 'https://upload.wikimedia.org/hopper-1280.jpg', 'mime': 'image/jpeg', 'width': 1280,
        'height': 1600, 'descriptionurl': 'https://commons.wikimedia.org/wiki/File:Grace_Hopper.jpg',
        'extmetadata': {'LicenseShortName': {'value': 'CC BY-SA 4.0'}, 'Artist': {'value': 'Jane Doe'},
                        'LicenseUrl': {'value': 'https://creativecommons.org/licenses/by-sa/4.0'}}}]}


@pytest.fixture
def commons(monkeypatch):
    """Fake Commons API: returns the pages given, and records downloads instead of fetching."""
    state = {'pages': [], 'downloads': []}
    monkeypatch.setattr(images, 'api', lambda params: {'query': {'pages': {str(i): p for i, p in
                                                                             enumerate(state['pages'])}}})

    def download(url, path):
        state['downloads'].append(url)
        with open(path, 'wb') as f:
            f.write(b'\xff\xd8 fake jpeg')
    monkeypatch.setattr(images, 'download', download)
    return state


@pytest.mark.parametrize('license_name, free', [
    ('Public domain', True), ('PD-US', True), ('CC0', True), ('CC BY 4.0', True), ('CC BY-SA 3.0', True),
    ('CC BY-NC 4.0', False), ('CC BY-ND 4.0', False), ('Logo', False), ('', False),
])
def test_only_free_licenses_are_accepted(license_name, free):
    assert images.free_license(license_name) is free


def test_search_lists_only_free_images_with_their_credit(cli, commons):
    commons['pages'] = [ENIAC, LOGO, HOPPER]
    code, r = cli('images', 'search', 'eniac')
    assert code == 0 and [i['title'] for i in r['results']] == ['File:Eniac.jpg', 'File:Grace Hopper.jpg']
    assert r['results'][0]['author'] == 'U.S. Army Photo' and r['results'][1]['license'] == 'CC BY-SA 4.0'
    assert r['left_out'] == 1


def test_fetch_saves_the_image_and_its_credit(cli, book, commons):
    commons['pages'] = [HOPPER]
    code, r = cli('images', 'fetch', 'File:Grace Hopper.jpg', '--name', 'c02-hopper', '--book', book)
    assert code == 0 and (book / 'img' / 'c02-hopper.jpg').exists()
    credits = (book / 'img' / 'CREDITS.md').read_text(encoding='utf-8')
    assert credits.startswith('# Image credits' + chr(10) * 2 + '- c02-hopper.jpg:') and 'CC BY-SA 4.0' in credits
    assert 'Jane Doe' in credits and 'commons.wikimedia.org' in credits
    assert r['markdown'].startswith('![') and '../img/c02-hopper.jpg' in r['markdown']
    assert 'Jane Doe' in r['caption'] and 'CC BY-SA 4.0' in r['caption']


def test_fetch_refuses_a_non_free_image(cli, book, commons):
    commons['pages'] = [LOGO]
    code, r = cli('images', 'fetch', 'File:Some logo.png', '--name', 'c02-logo', '--book', book)
    assert code == 1 and 'free license' in r['error'] and not commons['downloads']


def test_fetch_of_a_missing_file_is_an_error(cli, book, commons):
    commons['pages'] = [{'title': 'File:Nope.jpg', 'missing': ''}]
    code, r = cli('images', 'fetch', 'File:Nope.jpg', '--name', 'c02-x', '--book', book)
    assert code == 1 and 'not found' in r['error']


def test_a_second_fetch_does_not_repeat_the_credit(cli, book, commons):
    commons['pages'] = [HOPPER]
    cli('images', 'fetch', 'File:Grace Hopper.jpg', '--name', 'c02-hopper', '--book', book)
    cli('images', 'fetch', 'File:Grace Hopper.jpg', '--name', 'c02-hopper', '--book', book)
    credits = (book / 'img' / 'CREDITS.md').read_text(encoding='utf-8')
    assert credits.count('c02-hopper.jpg') == 1


def test_screenshot_without_playwright_explains_what_to_do(cli, book, monkeypatch):
    monkeypatch.setitem(sys.modules, 'playwright', None)
    code, r = cli('images', 'screenshot', 'http://localhost:8080', '--name', 'c05-app', '--book', book)
    assert code == 1 and 'playwright install chromium' in r['error'] and 'ask the user' in r['error']


def test_screenshot_saves_the_page_and_its_credit(cli, book, monkeypatch):
    shots = []

    class Page:
        def goto(self, url, wait_until):
            shots.append(url)

        def screenshot(self, path, full_page):
            open(path, 'wb').write(b'\x89PNG fake')

    class Browser:
        def new_page(self, viewport):
            return Page()

        def close(self):
            pass

    class Playwright:
        chromium = types.SimpleNamespace(launch=lambda: Browser())

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    sync_api = types.ModuleType('playwright.sync_api')
    sync_api.sync_playwright = Playwright
    monkeypatch.setitem(sys.modules, 'playwright', types.ModuleType('playwright'))
    monkeypatch.setitem(sys.modules, 'playwright.sync_api', sync_api)
    code, r = cli('images', 'screenshot', 'http://localhost:8080', '--name', 'c05-app', '--book', book)
    assert code == 0 and shots == ['http://localhost:8080'] and (book / 'img' / 'c05-app.png').exists()
    assert 'c05-app.png' in (book / 'img' / 'CREDITS.md').read_text(encoding='utf-8')
