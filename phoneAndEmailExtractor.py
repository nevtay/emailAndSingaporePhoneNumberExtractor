#! python3
# phoneAndEmailExtractor.py
# extract emails and singaporean phone numbers from copied text

from curses.ascii import isalnum
import re
import pyperclip


def extractSingaporePhoneNumbers(copiedTextNoNewlines):
    foundNumbersString = 'Numbers found: '
    sgPhoneRegex = re.compile(
        r'''
            (65)?                   # checks for country code prefix (e.g. 65, 65-, 65 , 65., optional)
            (\s|-|\.)?
            ([986]                  # checks if first digit is 9, 8, or 6
            \d{3}                   # checks if 3 digits follow after the first 9, 8, or 6
            \s?                     # checks if a space comes after the 4th digit (optional)
            \d{4})                  # checks if there are 4 digits after the 4th digit and/or space
            ''', re.VERBOSE)
    foundNumbers = sgPhoneRegex.findall(copiedTextNoNewlines)
    if (len(foundNumbers) == 0):
        foundNumbersString = 'No Singaporean phone numbers found.'
    else:
        for i, v in enumerate(foundNumbers):
            tempString = ('').join(v).strip()
            if not isalnum(tempString[0]):
                tempString = tempString[1:]
            if i == len(foundNumbers) - 1:
                foundNumbersString = foundNumbersString + tempString
            elif i == len(foundNumbers) - 2:
                foundNumbersString = foundNumbersString + tempString + ' and '
            else:
                foundNumbersString = foundNumbersString + tempString + ', '
    return foundNumbersString


def extractEmailAddresses(copiedTextNoNewlines):
    emailString = 'Emails found: '
    copiedTextNoNewlines = copiedTextNoNewlines.replace("\n", " ")
    emailRegex = re.compile(
        r'''                        # a valid email should have 3 parts - (username)(@domain)(.com)
        (\S{1,})                    # at least 1 character in username, no spaces allowed
        (@\S{1,})                   # a single @ symbol followed by first part of domain name, no spaces allowed
        ([.]\S{1,})                 # extension name of at least 1 character, preceded by a period, no spaces allowed      
        ''', re.VERBOSE)
    foundEmails = emailRegex.findall(copiedTextNoNewlines)
    foundEmails = list(foundEmails)
    if len(foundEmails) == 0:
        return 'No emails found'
    for i, v in enumerate(foundEmails):
        tempString = ''.join(v)
        if not isalnum(tempString[-1]):
            tempString = tempString[0:len(tempString) - 1]
        if i == len(foundEmails) - 1:
            emailString += tempString
        elif i == len(foundEmails) - 2:
            emailString += (tempString + " and ")
        else:
            emailString += (tempString + ", ")
    return emailString


def getEmailAndPhoneNumbersFromCopiedText():
    copiedText = pyperclip.paste()
    copiedTextNoNewlines = copiedText.replace("\n", " ")

    extractedSGPhoneNumbers = extractSingaporePhoneNumbers(
        copiedTextNoNewlines)
    extractedEmailAddresses = extractEmailAddresses(copiedTextNoNewlines)

    combinedString = extractedEmailAddresses + "\n" + extractedSGPhoneNumbers
    pyperclip.copy(combinedString)


getEmailAndPhoneNumbersFromCopiedText()
