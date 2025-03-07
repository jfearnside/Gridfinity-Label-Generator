# Hardware sticker generator

Credit: THis project is a fork of Teh Gridfinity Label Maker by Clement Roblot
CHeck out his project here: https://github.com/clement-roblot/Gridfinity-Label-Generator

This application is a label generator aimed at Niimbot users to make labels for small hardware parts containers.
ALthough this product is primarily meant for use with the Niimbot range of thermal printers it can be used by any printer. You can output labels as a PDF as a sheet of labels. 


I like these: https://www.amazon.com/dp/B07VMVYKTS
This organiser is great for these containers (and doesn't have to be used in a toolbox): https://makerworld.com/en/models/961737-husky-workbench-small-parts-storage-organization#profileId-931766


The "killer" feature of this project is the ability to dynamicaly render the 3d view of the object shown on the sticker.


## Finding 3d models

McMasterCarr is a great resource for 3D models of hardware parts. https://www.mcmaster.com/
Find the hardware part you want a label for on McMasterCarr and you can download a STEP files for the item. Place this in a folder and browse to teh STEP file in teh application. Once loaded (its a bit slow) you can use the sliders to adjust he rotation. 

## Instructions for use

THe application opens with one empty sticker loaded. You can add additional labels by clicking on the add button. 
You can also use the file menu to open a JSON file that contain preconfigured sample labels (File-->Open). 

You can save your labels as a JSON using the Save command available on the File menu (File --> Save)

CLick on teh label in the list that you want to edit. Enter information about your hardware part into line 1, 2, and 3. 
For Example
Line 1: M3 x 15mm
Line 2: Socket Hex
Line 3: Screws

You can enter a URL to create a QR code. I like to add a link to the McMasterCarr page so that I can easily reorder parts. 
On the 3D Model line click browse and navigate to a 3D STEP file of the part. You can use the Alpha and Beta sliders to rotate the part in the 3D preview window. 

Click Preview to see a preview of your label. If needed you can adjust the font sizes of the 3 lines of text. 
NOTE: The preview does not auto-refresh. Once you have made changes click the Refresh Preview button to check font size etc. 

You can also mass edit the json with the details of your labels

Once you are happy with your labels you can export them to either individual PNGs or a PDF contianing sheets of labels. 
NOTE: Only the labels that are checked on the list will export. You can use the Select All/Deselect All button to help with selecting large numebrs of labels. 

The Top/Bottom corner items int eh UI control are used to give your label rounded corners. 

