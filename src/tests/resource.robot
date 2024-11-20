*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}             localhost:5000
${DELAY}              0.5 seconds
${HOME_URL}           http://${SERVER}
${REFS_URL}           http://${SERVER}/refs
${RESET_URL}          http://${SERVER}/reset_db
${NEW_ARTICLE_URL}    http://${SERVER}/create_reference/article
${BROWSER}            chrome
${HEADLESS}           false

*** Keywords ***
Open And Configure Browser
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Main Page Should Be Open
    Title Should Be  Index
    Page Should Contain  Welcome page

Successfully Created Article
    Main Page Should Be Open

Failed To Create Article
    Title Should Be  Create article reference
    Page Should Contain  Invalid details


Reset Articles
    Go To  ${RESET_URL}
