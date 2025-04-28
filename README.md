# SCRIPTWRITER INSTRUCTIONS
## CREATED BY HOLY AND MAI IN JANUARY 2025

### Creating the text file
- You can use any text editor that can export text files in UTF-8.
- There is an example text file (Test.txt) in the repository for your reference

**Syntax for text file:**  
- The first symbol at the start of each line determines how it is formatted  
- No header/anything else: Descriptions will be left-aligned with normal margins  
- "title:"	= name of your script on the title page, please only use it once at the start  
- "author:"	= author name on the title page, please only use it once at the start  
- "/"		= Chapter title, these titles will be added to a table of contents; make sure they don't repeat, or the script will break  
- "."		= Location, line will be converted to all caps and left aligned  
- "@"		= Character name, line will be converted to all caps, and special margins  
- "("		= parenthesis, usually used to indicate specific emotion or action before or during dialogue, converts line to special margins; unlike all of the other commands, the parentheses symbols will be included in the output  
- " ' "		= Dialogue, line will be converted to special margins for dialogue  
- "#"		= Comments, will be ignored in output  
"=" 		= page break, will start a new page, anything written on this line will be ignored


### Exporting the text file

- Use these commands in the cmd/anaconda prompt; you need Python installed on your device  

- Go to your folder where you have both your text files and the scriptwriter.py is located  

`cd C:\Scripts
`

- How to use the command lines =  
`python scriptwriter.py`	(always put this to call the Python script)  
`--input yourTextFile.txt`	(File path/name of target txt file (from current directory))  
`--output newScript.pdf`	(file path/name of output pdf file (from current directory))  
`--subscript "Hello"`	(text at the bottom of each page)  
`--font Ubuntu`		(font family used to render all text, available from the font folder, you can add your own fonts in the script)  

- Write the command in one line, just like below  

`python scriptwriter.py --input Chapter1-Text.txt --output Chapter1-Script.pdf --subscript "Created by User" --font UbuntuMono`  

- The Python script will render the script and output the message below if there are no errors.  

`Creating Table of Contents...`  
`Rendering Main Content...`  
`PDF created successfully: Chapter1-Script.pdf`  

## Done and enjoy writing!

