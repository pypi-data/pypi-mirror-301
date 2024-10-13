# https://www.ditig.com/256-colors-cheat-sheet
# https://en.wikipedia.org/wiki/X11_color_names
# https://vim.fandom.com/wiki/Xterm256_color_names_for_console_Vim
# https://ss64.com/bash/syntax-colors.html
# https://en.wikipedia.org/wiki/X11_color_names
# https://en.wikipedia.org/wiki/Web_colors
# https://unix.stackexchange.com/questions/148/colorizing-your-terminal-and-shell-environment

xterm_256_colors = []

# Generate the color cube (216 colors)
for r in range(0, 6):
    for g in range(0, 6):
        for b in range(0, 6):
            xterm_256_colors.append((r * 40, g * 40, b * 40))

# Generate the grayscale ramp (24 colors)
for shade in range(0, 24):
    gray_value = shade * 10 + 8
    xterm_256_colors.append((gray_value, gray_value, gray_value))

# Now, xterm_256_colors contains a list of all Xterm-256 colors

# Example: Print the first 16 colors in the list
for i, color in enumerate(xterm_256_colors):
    print(f"Color {i}: RGB{color}")
