# Chore Tracker 500
To build:
flet build apk --arch arm64-v8a

This app was a personal project for my son. He is wanting to earn money, so I decided to create a mobile app that I could keep track of what I owe him. 

When launching the app, you will see a blank screen with the title Chore Tracker 5000 on the top. Below the title, you will see a page name with an downward arrow beside it. Clicking the arrow reveals a dropdown menu with 3 pages available to select. This allows you to keep track of up to 3 kids and their chores. 
On the row the row below the title and page selector, you will see a button with a + sign on the left and a button with a settings icon on the right. 

**The "Add" button:**
Clicking the add button will reveal 2 new text boxes, "New Chore Title" and "New Chore Price". Enter the title of the new chore you are adding (20 character limit on the mobile version and 4o character limit on the Windows version). The "Chore Price" text box will only accept numerical characters. Clicking the "Submit" button will create a new button on the page with the "Chore Title" and the amount of money earned for that chore, based from the price of the chore. Clicking the "Exit" button will do just that and exit the new chore entry boxes.

The new button will also have a pencil icon to the right. Clicking this will reveal a pop out dialog box with the text "Edit Chore. What do you want to do?". There will also be 3 buttons to choose from, "Reset to Zero", "Delete", and "Edit". 

"Reset to Zero" does just this, resetting the total money earned for the chore to $0. Before resetting, you will be prompted with a new pop out dialog with the text "Are you sure?". Clicking yes will reset the chore total and exit the "Chore Edit" pop out. If you do not wish to reset the button, clicking no will bring you back to the main "Edit Chore" pop out. 

The "Delete" button does just that, deletes the chore from the page. Before deleting, you will be prompted with a new pop out dialog with the text "Are you sure?". Clicking yes will delete the chore total and exit the "Chore Edit" pop out. If you do not wish to reset the button, clicking no will bring you back to the main "Edit Chore" pop out. 

The "Edit" button reveals a new pop put dialog asking for the new "Enter new Chore title" and "Enter new Chore price". Neither field are required. Clicking "Save" will apply the new information to the chore button and exit the "Edit Chore" pop out. 

Every time the chore button is clicked, the "Chore Price" will be added to the chore button total. This will also be added to the grand total displayed on the bottom of the page. 

If multiple buttons are added and the exceed the screen, a scroll bar will reveal itself so the chores can be scrolled up and down. 

**The "Settings" Button:**
Clicking the settings button will reveal a new pop out dialog with multiple page settings. The first settings will be used to rename the "Rename Page" ("Page 1", "Page 2", and "Page 3") to the name of a child or job. You will need to enter the "New Page Title" and select the page needing to be renamed from the dropdown box. Click submit to exit the "Settings" pop out and see the renamed page. 

Under the page rename settings you will see the "Color Theme" settings. This is controlled by a dropdown box. Select a new theme and click submit to see the new theme. There are "Tangerine" (Default), "Rose", "Cool", "Steel", and "Limon". Click submit to exit the "Settings" pop out and see the new color theme. 

Under the Page Theme settings you will see a toggle switch with the Text "Sound On/Off" above it. This will control if you want to here the "KACHING" or the "Coin Drop" sound effects when pressing the the Chore button or the payout button. 

Click "Exit" to exit the "Settings" pop out. 

At the bottom of the page you will see the "Total:" earned. Under the grand total you will see a button with a $ sign on it. Clicking this will reveal a new pop out dialog with the test "How much did you pay?". This allows you to enter an amount that was paid out. When an amount is entered here and submitted, the chore totals will reset to zero, the grand total will show the difference between the grand total and the amount paid out, and a "KACHING" sound effect will play (This can be turned off in the settings). 
