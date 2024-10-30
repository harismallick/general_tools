## Vim text editor tutorial ##
# Source 1: https://www.youtube.com/watch?v=IiwGbcd8S7I
# Source 2: https://www.youtube.com/watch?v=RZ4p-saaQkc&t=531s
# Vim cheat sheet: https://devhints.io/vim


def test_func() -> None:
    print("hello world")
    return

# Vim notes:
# : brings up vim's cli
# :w to save a file without exiting the editor.
# :q to exit the editor. If changes have not been saved, then editor will throw an error.
# :wq to write changes and close editor.
# :q! to exit without saving changes.
# dd is to delete line
# i is to go into insert mode where the cursor is.
# a is insert mode one column to the right of the cursor position.
# A is to go into insert mode by taking cursor to the end of the line.
# gg is to go to the top of the file
# G is to go to bottom of file
# { is to go up a code block
# } is to do down a code block
# hjkl is to navigate. Remember LDUR -> Left Down Up Right
# u is to undo an operation is normal mode
# ^r is to redo the operation in normal mode.
# yy is to copy the whole line the cursor is on.
# y is to yank just the word the cursor is on.
# y<n>w is to copy n words from cursor position, where n is an integer.
# p is to paste the copy buffer below the cursor.
# P is to paste the copy buffer above the cursor.
# o when in normal mode creates a new line below cursor and puts vim in INSERT mode.
# O does the same as above but places line above the cursor position.
# V puts vim in visual mode and you can select multiple lines of code.
# w is to move horizontally on the line to the next word.
# b is to go backwards on the line one word at a time.
# W and B skip to the first word or letter after the next line space.
# ^ to go to the first word in a line.
# $ to go to the last word in a line.
# f and t are used to go to a specific letter or character in the line.
# t will place the cursor before the letter, while f will place cursor on the letter.
# % takes you to the closing bracket if the cursor is on the opening bracket. Useful for large code blocks.
# cw is to change the word that the cursor is on.
# dw is to delete the word the cursor is on.
# D deletes everything to the right of the cursor on the line.
# C does the same thing as D, but also puts vim in INSERT mode.
# dt <char> deletes everything to the right of the cursor up unti the specified character.
# * will find the next occurrence of the word the cursor is on.
# t <char> to find first occurrence of a char, then use ; to find all other on the same line.
# zz to position the line the cursor is on to the center of the screen.
# ~ is to change the character case, from upper to lower and vice versa.
# . is used for repeat the previous vim command.
# r <char> changes the letter at the cursor position to the specified character.
# R <string> starts an input stream where vim will start replacing as many letters is typed by the user.
# ctrl+shift+v is to paste an external text buffer into vim, similar to nano.
# 

if __name__ == '__main__':
    test_func()
