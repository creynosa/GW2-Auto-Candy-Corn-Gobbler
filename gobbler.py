#!/usr/bin/env python3.9

import math
from pathlib import Path
from typing import Union

import pyautogui


def printInstructions() -> None:
    """Prints a set of basic instructions on how to use this program."""
    print("\n======================================================================")
    text = (
        "To avoid any issues when using this program, do the following:\n\n"
        "1. You'll need Guild Wars 2 to be on your main display.\n"
        "2. Your resources must be visible somewhere on your screen at all times.\n"
        "3. Avoid moving the mouse unless it is to exit this console window.\n"
        "4. Feel free to move this window to any other monitor.\n"
        "5. A message will appear once this program has finished running.\n\n"
        "Press enter to continue: "
    )

    input(text)


def askForMethod() -> str:
    """Asks the user what method is preferred for running the program and returns it: clicks or duration."""
    methods = {
        1: "clicks",
        2: "time",
    }

    print("\n======================================================================")
    response = input(
        "Would you like to automate your resources for a set number of clicks or for a set length of "
        "time?\n\n"
        "1. Number of Clicks\n"
        "2. Length of Time\n"
        "\n"
    )
    validResponses = ("1", "2")
    while response not in validResponses:
        response = input(
            "\nInvalid selection. Enter the number corresponding to your choice. Please try again: "
        )

    response = int(response)
    return methods[response]


def askForNumberOfClicks() -> int:
    """Asks and returns the number of clicks the user would like to automate the resources for."""
    print("\n======================================================================")
    response = input(
        "Please enter the number of clicks you'd like to run the resources for: "
    )
    validResponse = response.isdigit()
    while not validResponse:
        response = input("\nInvalid number of clicks. Please try again: ")
        validResponse = response.isdigit()

    clicks = int(response)
    if clicks == 1:
        clickText = "click"
    else:
        clickText = "clicks"
    print(f"\nProgram set to run for {clicks} {clickText}!\n")
    return clicks


def askForUnitOfTime() -> str:
    """Asks and returns the unit of time the user would like to automate the resources for."""
    unitsOfTime = {
        1: "seconds",
        2: "minutes",
        3: "hours",
        4: "days",
    }

    print("\n======================================================================")
    response = input(
        "Please enter the unit of time you would like to run the resources for: \n\n"
        "1. Seconds\n"
        "2. Minutes\n"
        "3. Hours\n"
        "4. Days\n"
        "\n"
    )
    validResponses = ("1", "2", "3", "4")
    while response not in validResponses:
        response = input(
            "\nInvalid selection. Enter the number corresponding to your choice. Please try again: "
        )

    response = int(response)
    return unitsOfTime[response]


def askForTime() -> Union(int, str):
    """Asks and returns the time the user would like to automate the resources for."""
    unitOfTime = askForUnitOfTime()

    print("\n======================================================================")
    response = input(
        f"Please enter how many {unitOfTime} you would like to run the resources for: \n\n"
    )
    validResponse = response.isdigit()
    while not validResponse:
        response = input("\nInvalid duration of time. Please try again: ")
        validResponse = response.isdigit()

    duration = int(response)
    if duration == 1:
        unitOfTime = unitOfTime[:-1]
    print(f"\nProgram set to run for {duration} {unitOfTime}.")
    return duration, unitOfTime


def calculateLoopsFromClicks(clicks: int) -> int:
    """Calculates the number of loops the program will execute based on the inputted number of clicks."""
    loops = clicks
    return loops


def calculateLoopsFromTime(time: tuple[int, str]) -> int:
    """Calculates the number of loops the program will execute based on the inputted length of time."""
    duration, unit = time
    multiplier = None
    if unit in ("seconds", "second"):
        multiplier = 1
    elif unit in ("minutes", "minute"):
        multiplier = 60
    elif unit in ("hours", "hour"):
        multiplier = 60 * 60
    elif unit in ("days", "day"):
        multiplier = 60 * 60 * 60

    durationSeconds = duration * multiplier
    loops = max(math.floor(durationSeconds / 5), 1)
    return loops


def getGobblerLocation(gobbler: str):
    """Finds and returns the location of the resources on the main screen."""
    gobblerImagePath = str(
        Path(__file__).parent / "resources" / f"{gobbler}-gobbler.png"
    )

    print("\n======================================================================")
    location = None
    while location is None:
        print("Searching for resources...\n")
        location = pyautogui.locateCenterOnScreen(
            gobblerImagePath, grayscale=True, confidence=0.9
        )
    print("Gobbler found!")
    return location


def clickGobbler(location, loops: int) -> None:
    """Clicks on the resources for a determined amount of time or clicks."""
    print("\n======================================================================")
    print("To cancel, please close this window at anytime.\n\n")

    pyautogui.doubleClick(location)
    loopsRemaining = loops - 1
    loopsFinished = 1
    print("{:.1%} completed...".format(loopsFinished / loops), end="\r")
    while loopsRemaining:
        pyautogui.sleep(5)
        pyautogui.doubleClick(location)
        loopsFinished += 1
        loopsRemaining -= 1
        print("{:.1%} completed...".format(loopsFinished / loops), end="\r")
    print("")
    print("\n======================================================================")
    print("Finished! Enjoy!")


def printCandyCornRequired(loops: int) -> None:
    """Prints a message with the number of candy corn that is required for a given number of loops."""
    candyPerLoop = 3
    totalCandy = candyPerLoop * loops
    maxCandyStack = 250

    stacks, individual = divmod(totalCandy, maxCandyStack)

    if stacks and individual:
        stackSuffix = "" if stacks == 1 else "s"
        pieceSuffix = "" if individual == 1 else "s"
        text = (
            f"You will need {stacks} stack{stackSuffix} and {individual} piece{pieceSuffix} of candy corn in your "
            f"inventory."
        )
    elif stacks and individual == 0:
        stackSuffix = "" if stacks == 1 else "s"
        text = f"You will need {stacks} stack{stackSuffix} of candy corn in your inventory."
    elif stacks == 0 and individual:
        pieceSuffix = "" if individual == 1 else "s"
        text = f"You will need {individual} piece{pieceSuffix} of candy corn in your inventory."
    else:
        text = "No candy corn is required in your inventory."

    print("\n======================================================================")
    print(text)
    print("\n")


def verifyUserHasCandyCorn() -> None:
    """Asks the user to confirm they have the required candy corn before proceeding."""
    input(
        "Press enter once you have verified you have the required amount of candy corn to commence: "
    )


if __name__ == "__main__":

    printInstructions()

    gobblerMethod = askForMethod()

    if gobblerMethod == "clicks":
        gobblerClicks = askForNumberOfClicks()
        gobblerLoops = calculateLoopsFromClicks(gobblerClicks)
    else:
        lengthOfTime = askForTime()
        gobblerLoops = calculateLoopsFromTime(lengthOfTime)

    # noinspection PyUnboundLocalVariable

    printCandyCornRequired(gobblerLoops)
    verifyUserHasCandyCorn()

    gobblerLocation = getGobblerLocation("candy-corn")
    clickGobbler(gobblerLocation, gobblerLoops)
