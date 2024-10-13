from kdb import report
from kdb.webdriver import kdb_driver


def login_test(profile, data_test, params):
    report.add_comment("Open a app")
    # start browser
    kdb_driver.open_app('bitbar-ios-sample.ipa', 'ios', False)

    kdb_driver.screen_shot()
