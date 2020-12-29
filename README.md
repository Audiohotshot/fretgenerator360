# fretgenerator360
v1.0 
Fretboard generator for guitarbuilders in Fusion360

Author: www.Audiohotshot.nl

Instruction video: https://www.youtube.com/watch?v=hlhe1uPf3LY

*PLEASE DO NOT CHANGE THIS FILE, IT'S GOING TO BE OVERWRITEN ON EACH UPGRADE*

# Purpose:
This Addin for Fusion360 is meant for making fretboards for guitars.
The plugin draws a fretboard with fretlines. You can enter the scale of the fretboard; it wil draw the whole board including the frets. It also draws the line for the tremolo-part so you know what (when slanted) the exact direction of the trem is. 

The plugin also draws a construction centre line. The whole fretboard is drawn on the centre of the x-axis.
You can use this generator as a base for you guitardesign, as it draws a centre construction line. Also by selecting the whole fretboard and extruding it, you have the basis for a neck and fretboard.

If you like this plugin and/or have suggestions for improvements, you're welcome to let me know. Have fun drawing!

# Installation:
Copy all files to your Addin folder of Fusion360

On Windows, these are the folder paths:
For an Add-In, %appdata%\Autodesk\Autodesk Fusion 360\API\AddIns

On macOS, these are the folder paths:
For an add-in, the path is ~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns

# Launch plugin:
Locate the plugin in the addin-panel of Fusion360 and press RUN.
The plugin will stay resident in the addinpanel as long as its running.

# Features:
- Scale high - holds the scale for normal scales.
- Slanted - will reveal the options for slanted fretboards
- Scale low - holds the scale for slanted fretboards
- Centre fret - holds the fretnumber which will be the centre of the slanted board
- Number of frets - the amount of frets the boards will have (max 36)
- Width - the width of the fret board
- Show dots - will reveal and draw the positiondots
- Diameter - the diameters of the dots
- Draws a scale construction line in the centre of the fretboard
- Draws a line to indicate centre and direction of bridge/tremolo

This was developed on a Mac running Fusion360 and Spyder2

# Known issues:
Use realistic numbers; negative numbers or insane big numbers do not guarantee a normal result.

# Disclaimer:
The software is made available "AS IS". It seems quite stable, but it is in
an early stage of development.  Hence there should be plenty of bugs not yet
spotted.
