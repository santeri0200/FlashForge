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

Creating book references and viewing them
    Go To  ${NEW_BOOK_URL}
    Input Text  author  Matti
    Input Text  year  1989
    Input Text  title  Tutkimusartikkeli
    Input Text  publisher  Cambridge University Press
    Input Text  address  Cambridge
    Click Button  Create

    Go To  ${REFS_URL}
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli

    Go To  ${NEW_BOOK_URL}
    Input Text  author     Teppo
    Input Text  year       2000
    Input Text  title      Tepon kirjoitelma
    Input Text  publisher  Cambridge University Press
    Input Text  address    Cambridge
    Click Button  Create

    Go To  ${REFS_URL}
    Page Should Contain  Found 2 references:
    Page Should Contain  Tepon kirjoitelma
    Page Should Contain  Tutkimusartikkeli

Creating inproceedings references and viewing them
    Go To  ${NEW_INPROCEEDINGS_URL}
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  booktitle  Matin Artikkeli
    Input Text  year  1989
    Click Button  Create

    Go To  ${REFS_URL}
    Page Should Contain  Found 1 reference:
    Page Should Contain  Tutkimusartikkeli

    Go To  ${NEW_INPROCEEDINGS_URL}
    Input Text  author     Teppo
    Input Text  title      Tepon kirjoitelma
    Input Text  booktitle  Tepon kootut kirjoitelmat
    Input Text  year       2000
    Click Button  Create

    Go To  ${REFS_URL}
    Page Should Contain  Found 2 references:
    Page Should Contain  Tepon kirjoitelma
    Page Should Contain  Tutkimusartikkeli

Creating manual references and viewing them
    Go To  ${NEW_MANUAL_URL}
    Input Text  title  Manuaali
    Input Text  year  1989
    Click Button  Create

    Go To  ${REFS_URL}
    Page Should Contain  Found 1 reference:
    Page Should Contain  Manuaali

    Go To  ${NEW_MANUAL_URL}
    Input Text  title  Tekninen manuaali
    Input Text  year   2000
    Click Button  Create

    Go To  ${REFS_URL}
    Page Should Contain  Found 2 references:
    Page Should Contain  Manuaali
    Page Should Contain  Tekninen manuaali
