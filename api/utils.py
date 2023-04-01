def get_characters_and_times(
    lines_list: list, duration: int, multiline: bool = False, pause: int = 1000
):
    """
    Returns the list of characters to be displayed and the list of keyframe times for each character to be displayed

    Notes
    -----
    If not multiline, then it is just a list of characters per line, typed then backspaced for eac line
              i.e. ['H','Ho','How', 'Ho', 'H', '', 'a', 'an', 'and', 'an ', 'a', '']
                  2 normal lines: 'How' -> backspaced, then 'and' -> backspaced
    Multiline is all lines typed seperated by a line break and all backspaced
              i.e. ['H','Ho','How' 'How\n', 'How\na', 'How\nan', 'How\nand', 'How\nan ', 'How\na', 'How\n', 'How\n' 'How', 'Ho', 'H', '']

    Parameters
    ----------
    lines_list : list
        the list of strings to be displayed
    duration : int
        the duration of the animation in milliseconds
    multiline : bool, optional
        wheather to display as multiple lines, by default False
    pause : int, optional
        the length of pauses in milliseconds, by default 1000

    Returns
    -------
    total_characters : list
        the list of characters to be displayed
    display_time : list
        the list of keyframe times for each character to be displayed
    """
    duration = duration / 1000
    total_characters = []
    if multiline:
        for line in lines_list:
            characters = list(line)
            for i in range(len(characters)):
                if i == 0:
                    if len(total_characters) == 0:
                        total_characters.append(characters[i])
                    else:
                        total_characters.append(
                            total_characters[len(total_characters) - 1] + characters[i]
                        )
                # once we reach the end of the line, add a line break
                elif i == len(characters) - 1:
                    total_characters.append(
                        total_characters[len(total_characters) - 1] + line[i]
                    )
                    total_characters.append(
                        total_characters[len(total_characters) - 1] + "\n"
                    )
                else:
                    total_characters.append(
                        total_characters[len(total_characters) - 1] + line[i]
                    )

        temp = total_characters.copy()
        for i in range(len(total_characters)):
            total_characters.append(temp.pop())

        # add a blank line at the beginning
        total_characters.insert(0, "")
        # add a blank line at the end
        total_characters.append("")

        # display_time for multiline is a list of all the times for each character to be displayed adding the pause for the each string that ends with \n
        display_time = []  # keyframes
        for i in range(len(total_characters)):
            if i == 0:
                display_time.append(pause / 1000)
                # if we're in the first half of the animation, and the last character is a line break, add the pause time to the first keyframe
            elif total_characters[i].endswith("\n") and i < len(total_characters) / 2:
                display_time.append(
                    display_time[i - 1]
                    + (duration) / len(total_characters)
                    + (pause / 1000)
                )
            # on the last character, add the pause time to the last keyframe
            elif i == len(total_characters) + 1:
                display_time.append(
                    display_time[i - 1]
                    + (duration) / len(total_characters)
                    + (pause / 1000)
                )
            else:
                display_time.append(
                    display_time[i - 1] + (duration) / len(total_characters)
                )

    elif not multiline:
        # ['H','Ho','How', 'Ho', 'H', '', 'a', 'an', 'and', 'an ', 'a', '']
        for line in lines_list:
            characters = list(line)
            for i in range(len(characters)):
                if i == 0:
                    if len(total_characters) == 0:
                        total_characters.append("")
                        total_characters.append(characters[i])
                    else:
                        total_characters.append(
                            total_characters[len(total_characters) - 1]
                        )
                        temp = total_characters.copy()
                        for j in range(len(temp)):
                            if temp[len(temp) - 1] == "":
                                break
                            else:
                                total_characters.append(temp.pop())
                        total_characters.append("")
                        total_characters.append(characters[i])
                elif i == len(characters) - 1:
                    total_characters.append(
                        total_characters[len(total_characters) - 1] + characters[i]
                    )
                    total_characters.append(
                        total_characters[len(total_characters) - 1] + ""
                    )
                else:
                    total_characters.append(
                        total_characters[len(total_characters) - 1] + characters[i]
                    )
        temp = total_characters.copy()
        for j in range(len(temp)):
            if temp[len(temp) - 1] == "":
                break
            else:
                total_characters.append(temp.pop())
        total_characters.append("")

        display_time = []  # keyframes
        for i in range(len(total_characters)):
            if i == 0:
                display_time.append(pause / 1000)
                # if we're in the first half of the animation, and the last character is a line break, add the pause time to the first keyframe
            elif total_characters[i - 1] == total_characters[i]:
                display_time.append(
                    display_time[i - 1]
                    + (duration) / len(total_characters)
                    + (pause / 1000)
                )
            elif i == len(total_characters):
                display_time.append(
                    display_time[i - 1]
                    + (duration) / len(total_characters)
                    + (pause / 1000)
                )
            else:
                display_time.append(
                    display_time[i - 1] + (duration) / len(total_characters)
                )

    return total_characters, display_time
