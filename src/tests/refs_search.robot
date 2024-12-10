*** Settings ***
Resource         resource.robot
Suite Setup      Setup Search
Suite Teardown   Close Browser
Test Setup       Go To  ${HOME_URL}



*** Test Cases ***
Search by author
    Input Text  query  Mat
    Click Button  Search
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli


Search by title
    Input Text  query  kimusart
    Click Button  Search
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli


Search by journal
    Input Text  query  merican
    Click Button  Search
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli

Search by year
    Input Text  query  1989
    Click Button  Search
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli

Search non existing
    Input Text  query  8000
    Click Button  Search
    Page Should Contain  No results.

*** Keywords ***
Setup Search
    Open And Configure Browser
    Reset Articles
    Go To  ${HOME_URL}
    Main Page Should Be Open
    Click Link  Create article reference
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  journal  Scientific American
    Input Text  year  1989
    Click Button  Create
    Main Page Should Be Open
