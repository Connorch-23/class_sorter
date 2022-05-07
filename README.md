# class_sorter
## Welcome to Connor's Class Sorter. This program can be used to sort campers into classes at YMCA Camp Hanes. A couple things to check before you use this system.

1. Make sure you have digitized the camper preferences and updated the class files to account for capacity and whether or not a shooting sports form is needed.
2. Make sure that you know where these files are at on your computer. With most machines you can simply search the name of the file on the computer in either Finder(for Apple products) or Windows File Explorer (Microsoft products). I recommend organizing these files into a folder in order to better keep track of them later down the line. 
3. Make sure you have downloaded Java onto you computer. Its super easy and free:https://java.com/en/download/manual.jsp


# Step one: Formatting your files 
The most important part of this setup is formatting your files properly. My program reads in data in a very specific way so submitting a file in the incorrect format will cause issues. **I have provided 2 example files named Camper-test.csv and Classes-test.csv that you are more than welcome to use as a template when making the file.**

## Important Formatting Tips:
1. These formatting tips apply to both the camper file and the classes file. These must be distinct files and will be comprised of headers at the top. These headers can be renamed to anything, but they must be there.
2. It is also important that the order of the data from left to right remains the same. Changing whether this order could cause a failure of the program. The data should be in columns that read from left to right: Last Name, First Name, Age, Cabin,Can Shoot?, Pref1, Pref2, Pref3, Pref4, Pref5, Pref6.
3. It is important that each cell for every camper must have some data. **Basically, if you don't have all the information filled out for a camper, dont input them into the dataset quite yet.**
4. For the Classes file, it is also important that the order of the data from left to right remains the same. Changing whether this order could cause a failure of the program. The data should be in columns that read from left to right:Class Name	CapacityA	CapacityB	CapacityC	CapacityD	WillShoot?.
5. I apologize for the aggressiveness of this upcoming text, but it is very important to me :).
6. **MAKE SURE BOTH THE CLASSES FILE AND THE CAMPER FILES ARE IN .CSV FORMAT. THOUGH THEY MAY SOMETIMES APPEAR AS A NORMAL EXCEL SPREADSHEET, THE DATA IS ACTUALLY IN A COMMA SEPARATED VALUES FORMAT (.CSV) AND THIS SHOULD BE AT THE END OF THE FILE NAMES YOU WILL USE.**

# Step Two: Beginnnig the program
This part is pretty easy if you are on a Microsft machine that runs windows. All you have to do is find the program called class_sorter, and double click on it! 
If you are on a mac, running this program is a bit more complicated, but can be seen here:https://java.com/en/download/help/java_mac.html
To be honest, I also encourage googling if that doesn't work. But doing this on a windows based computer is just a lot easier. Let me know if I need to adjust things if the camp is moving to Apple.

It should be noted that you should not move the various contents around the program on your computer. You will recieve this file in a folder, and you should keep this folder together.
