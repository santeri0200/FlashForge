*** Settings ***
Library          SeleniumLibrary
Library          Collections
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Articles

*** Test Cases ***
Viewing empty references list
    Go To  ${REFS_URL}
    Page Should Contain  No results.

Creating article references and viewing them
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  journal  Scientific American
    Input Text  year  1989
    Click Button  Create

    Go To  ${REFS_URL}
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli

    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Teppo
    Input Text  title  Tepon kirjoitelma
    Input Text  journal  Scientific American
    Input Text  year  2000
    Click Button  Create

    Go To  ${REFS_URL}
    Page Should Contain  Found 2 references:
    Page Should Contain  Tepon kirjoitelma
    Page Should Contain  Tutkimusartikkeli