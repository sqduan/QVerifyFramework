*** Variables ***
${SETTINGS}
${PLATFORM_CONFIG}

*** Settings ***
Resource           ../../resources/common.resource

Suite Setup        Set Initialization    ${SETTINGS}

*** Test Cases ***
Trace32 Start
    ${result}=     Start Trace32 Process     TestPlatform1
    Should be equal    ${result}    ${0}

Show Test Platform
    Print Test Platform

Enumeration
    ${result}=     Set Initialization    ${SETTINGS}
    Should be equal     ${result}    ${0}

Set Bulk Transfer
    ${result}=     Set Initialization    ${SETTINGS}
    Should be equal     ${result}    ${0}

Do Bulk Transfer
    ${result}=     Set Initialization    ${SETTINGS}
    Should be equal     ${result}    ${0}

Set Interrupt Transfer
    ${result}=     Set Initialization    ${SETTINGS}
    Should be equal     ${result}    ${0}

Trace32 Kill
    ${result}=     Kill Trace32 Process     TestPlatform1
    Should be equal    ${result}    ${0}