from kdb import report
from kdb.webdriver import kdb_driver


def test_mobile_web():
    # start browser
    report.add_comment("Test mobile web")
    kdb_driver.start_browser("android")
    # load page for test.
    kdb_driver.open_url('https://google.com')
    kdb_driver.screen_shot()

    kdb_driver.close_browser()
