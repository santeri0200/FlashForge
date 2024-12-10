*** Settings ***
Library          SeleniumLibrary
Library          Collections
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Setup Order

*** Variables ***
${SORT_BUTTON}   //button[text()='Sort']
${LINK_NEW_TO_OLD}        //a[text()='Year New To Old']
${LINK_OLD_TO_NEW}        //a[text()='Year Old To New']
${LINK_AUTHOR_A_TO_Z}        //a[text()='Author (a-z)']
${LINK_AUTHOR_Z_TO_A}        //a[text()='Author (z-a)']

*** Test Cases ***
Creating references and order them by year
    Mouse Over    ${SORT_BUTTON}
    Wait Until Element Is Visible    ${LINK_NEW_TO_OLD}
    Click Element    ${LINK_NEW_TO_OLD}

    Mouse Over    ${SORT_BUTTON}
    Wait Until Element Is Visible    ${LINK_OLD_TO_NEW}
    Click Element    ${LINK_OLD_TO_NEW}

Creating references and order them by author
    Mouse Over    ${SORT_BUTTON}
    Wait Until Element Is Visible    ${LINK_AUTHOR_A_TO_Z}
    Click Element    ${LINK_AUTHOR_A_TO_Z}

    Mouse Over    ${SORT_BUTTON}
    Wait Until Element Is Visible    ${LINK_AUTHOR_Z_TO_A}
    Click Element    ${LINK_AUTHOR_Z_TO_A}

*** Keywords ***
Setup Order
    Reset Articles
    Go To  ${NEW_ARTICLE_URL}
    Input Text  author  Matti
    Input Text  title  Tutkimusartikkeli
    Input Text  journal  Scientific American
    Input Text  year  1989
    Click Button  Create

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
