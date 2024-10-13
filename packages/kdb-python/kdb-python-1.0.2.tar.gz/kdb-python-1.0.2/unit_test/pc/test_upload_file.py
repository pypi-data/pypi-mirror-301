from kdb import report
from kdb.webdriver import kdb_driver


def upload_file_test():
    # add command to the report
    report.add_comment("Test upload_file keyword/api")
    # start browser
    kdb_driver.start_browser()
    # loads login page in the current browser session.
    kdb_driver.open_url('https://davidwalsh.name/demo/multiple-file-upload.php')

    # verify fileList before
    kdb_driver.verify_text_on_page('No Files Selected', timeout=5)
    # take screenshot
    kdb_driver.screen_shot()

    # upload single file
    kdb_driver.upload_file('id=filesToUpload', 'Domains.txt')

    # verify fileList after upload single file
    kdb_driver.verify_text_on_page('Domains.txt', timeout=5)
    kdb_driver.verify_text_on_page('No Files Selected', reverse=True, timeout=1)
    # take screenshot
    kdb_driver.screen_shot()

    # upload single file
    kdb_driver.upload_file('id=filesToUpload', 'ProductIDs.txt', timeout=2)

    # verify fileList after upload single file
    kdb_driver.verify_text_on_page('ProductIDs.txt', timeout=5)
    kdb_driver.verify_text_on_page('Domains.txt', reverse=True, timeout=0)
    kdb_driver.verify_text_on_page('No Files Selected', reverse=True, timeout=0)
    # take screenshot
    kdb_driver.screen_shot()

    # negative cases
    try:
        # not support multiple files
        # the file_path is only accept str
        kdb_driver.upload_file('id=filesToUpload', ('Domains.txt', 'ProductIDs.txt'), log=False)
        assert False
    except:
        assert True
    #
    try:
        # raise exception if file path is not exist
        kdb_driver.upload_file('id=filesToUpload', 'file_not_found.txt', log=False)
        assert False
    except:
        assert True

    # close browser
    kdb_driver.close_browser()
