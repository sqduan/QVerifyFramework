*** Settings ***
Library     ../src/VerificationLibrary.py

*** Keywords ***
Reload Image
    [Arguments]    ${IP}    ${Port}    ${Timeout}
    ${result}=     VerificationLibrary.Reload Image   ${IP}    ${Port}    ${Timeout}
    [Return]       ${result}

Reset Rumi
    [Arguments]    ${IP}    ${Port}    ${Timeout}
    ${result}=     VerificationLibrary.Reset Rumi     ${IP}    ${Port}    ${Timeout}
    [Return]       ${result}

Reset Jtag
    [Arguments]    ${IP}    ${Port}    ${Timeout}
    ${result}=     VerificationLibrary.Reset Jtag     ${IP}    ${Port}    ${Timeout}
    [Return]       ${result}

Quit Rumi
    [Arguments]    ${IP}    ${Port}    ${Timeout}
    ${result}=     VerificationLibrary.Quit Rumi      ${IP}    ${Port}    ${Timeout}
    [Return]       ${result}

Test Initialization
    [Arguments]    ${Settings}
    ${result}=     VerificationLibrary.Test Initialization    ${Settings}
    [Return]       ${result}

Print Test platform
    VerificationLibrary.Print Test Platform

Start Trace32 Process
    [Arguments]    ${platformName}
    ${result}=     VerificationLibrary.Start Trace32 Process  ${platformName}
    [Return]       ${result}

Kill Trace32 Process
    [Arguments]    ${platformName}
    ${result}=     VerificationLibrary.Kill Trace32 Process  ${platformName}
    [Return]       ${result}

Connect Trace32
    [Arguments]    ${platformName}
    ${result}=     VerificationLibrary.Connect Trace32  ${platformName}
    [Return]       ${result}

Disconnect Trace32
    [Arguments]    ${platformName}
    ${result}=     VerificationLibrary.Disconnect Trace32  ${platformName}
    [Return]       ${result}

Read Term And Compare
    [Arguments]    ${platformName}     ${keywords}
    ${result}      ${matchAll}=     VerificationLibrary.Read Term And Compare      ${platformName}    ${keywords}
    [return]       ${result}        ${matchAll}

Wait Until Not Running
    [Arguments]    ${platformName}
    ${result}      VerificationLibrary.Wait Until Not Running      ${platformName}
    [return]       ${result}

Execute Trace32 Command
    [Arguments]    ${platformName}     ${command}
    ${result}=     VerificationLibrary.Execute Trace32 Command    ${platformName}    ${command}
    [Return]       ${result}

Execute Cmm Script
    [Arguments]    ${platformName}     ${scriptPath}
    ${result}=     VerificationLibrary.Execute Cmm Script     ${platformName}    ${scriptPath}
    [return]       ${result}

Sleep
    [Arguments]    ${seconds}
    ${result}=     VerificationLibrary.Sleep For Seconds  ${seconds}
    [return]       ${result}
