*** Variables ***
# A Drupal demo site
${HOME URL}       http://demo.opensourcecms.com/drupal/
${WM NAME}        admin
${WM PASS}        demo123
# Params for Selenium2Library
${BROWSER}        firefox
${DELAY}          0

*** Keywords ***
Open On Page
    [Arguments]    ${url}
    [Documentation]    Bla bla
    ...    Blo blo
    Open Browser    ${url}    firefox
    Maximize Browser Window
