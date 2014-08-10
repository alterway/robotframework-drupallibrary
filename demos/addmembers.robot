*** Settings ***
Documentation     Adding members to the Drupal demo site
Resource          resources.robot
Library           Selenium2Library
Library           DrupalLibrary    ${HOME URL}

*** Test Cases ***
Open Home Page
    Open Browser    ${HOME URL}    ${BROWSER}
    Maximize Browser Window

Signing In
    Sign In    ${WM NAME}    ${WM PASS}    stop_on_failure=${false}

Adding Some Members
    Comment    Add regular member johndoe
    Add Member    johndoe    johndoe@foo.com    bigsecret
    Comment    Add janedoe as administrator
    Add Member    janedoe    janedoe@foo.com    bigsecret    extra_roles=administrator
    Comment    Add inactive member foobar
    Add Member    foobar    foobar@foo.com    bigsecret    active=${false}

Attempt To Duplicate A Member
    [Documentation]    We know johndoe is already registered, we don't consider following
    ...    member addition as an error since we are just checking that Drupal denies adding
    ...    this user again.
    Add Member    johndoe    johndoe@foo.com    bigsecret    exit_on_failure=${false}
