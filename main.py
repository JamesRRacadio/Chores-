import json
import os
import flet as ft
import flet_audio as ftau

STORAGE_FILE = "chore_tracker_data.json"
page_font = {"segoe_script": "/fonts/segoesc.ttf"}
os.environ["FLET_EXTENSIONS"] = "flet_audio"


#This block will be where any page configurations are stored.
def main(page: ft.Page):
    #page.scroll=ft.ScrollMode.AUTO
    page.title = "Chore Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 400
    page.window.height = 800
    #page.window.width = 1000
    #page.window.height = 800
    page_theme_settings = {
        "Font": ft.Colors.ORANGE_900,
        "Back Ground": ft.Colors.ORANGE_100,
    }
    page.bgcolor = page_theme_settings["Back Ground"]
    page.fonts= page_font
    audio_player = ftau.Audio(src="/sounds/coindrop.mp3", autoplay=False, volume=1.0)
    audio_player_2 = ftau.Audio(src="/sounds/kaching.mp3", autoplay=False, volume=0.65)
    page.services.append(audio_player)
    page.services.append(audio_player_2)
    page.update()

#This block will contain any global variables needed throughout the app.
    chore_column_1 = ft.Column(visible=True)
    chore_column_2 = ft.Column(visible=False)
    chore_column_3 = ft.Column(visible=False)
    all_chore_columns = [chore_column_1, chore_column_2, chore_column_3]
    main_title = ft.Text(
                f"Chore Tracker 5000",
                size=28,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                font_family="segoe_script",
                color=page_theme_settings["Font"],
            )
    page_title = ft.Text("Page 1", size=17, weight=ft.FontWeight.BOLD)
    current_active_chore = None
    current_active_row = None
    current_action = None
    new_page_title = ft.TextField(label="New Page Title:")
    total = [0.00, 0.00, 0.00]
    total_paid = [0.00, 0.00, 0.00]
    grand_chore_total = ft.Text(f"Total: $0.00", size=20, weight=ft.FontWeight.BOLD, expand=True)
    input_field = ft.TextField(label="Enter new Chore title:")
    input_field_2 = ft.TextField(label="Enter new Chore price:")
    input_field_3 = ft.TextField()
    page_theme = ft.Dropdown(
        options=[
            ft.DropdownOption(key="Tangerine", text="Tangerine"),
            ft.DropdownOption(key="Rose", text="Rose"),
            ft.DropdownOption(key="Cool", text="Cool"),
            ft.DropdownOption(key="Steel", text="Steel"),
            ft.DropdownOption(key="Limon", text="Limon")
        ],
    )
    page_select = ft.Dropdown(
        options=[
            ft.DropdownOption(key="Page 1", text="Page 1"),
            ft.DropdownOption(key="Page 2", text="Page 2"),
            ft.DropdownOption(key="Page 3", text="Page 3"),
        ],
        bgcolor=ft.Colors.WHITE,
        fill_color=ft.Colors.WHITE,
        filled=True,
        width=120,
        on_select=lambda e: page_select_update(e)
    )
    page_select_rename = ft.Dropdown(
            options=[
                ft.DropdownOption(key="Page 1", text="Page 1"),
                ft.DropdownOption(key="Page 2", text="Page 2"),
                ft.DropdownOption(key="Page 3", text="Page 3"),
            ]
    )    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  ----------Define all of the Functions----------------
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++

# This function creates the Local Storage
    def save_app_data():
        def extract_chores(column):
            chores_list =[]
            for row in column.controls:
                if isinstance(row, ft.Row) and row.controls:
                    btn = row.controls[0]
                    if isinstance(btn, ft.ElevatedButton) and btn.data:
                        chores_list.append(btn.data)
            return chores_list

        data = {
            "total": total,
            "total_paid": total_paid,
            "selected_page": page_select.value  or "Page 1",
            "page_options": [{"key": opt.key, "text":opt.text} for opt in page_select.options],
            "theme_name": page_theme.value or "Tangerine",
            "chores": {
                "Page 1": extract_chores(chore_column_1),
                "Page 2": extract_chores(chore_column_2),
                "Page 3": extract_chores(chore_column_3),
            }
        }
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=2)

# This function generates the main title with the page selected.
    def main_title_update():
        nonlocal main_title, page_title
        page_selected = page_select.value #or "Page 1"
        for options in page_select.options:
            if options.key == page_select.value:
                page_selected = options.text
        page_title.value = f"{page_selected}"
        main_title.color = page_theme_settings["Font"]        
        page.update()   

#This function determines whichever column is currently selected.
    def get_current_column():
        if page_select.value == "Page 1":
            return chore_column_1
        elif page_select.value == "Page 2":
            return chore_column_2
        elif page_select.value == "Page 3":
            return chore_column_3
        else:
            return chore_column_1
        
# This function will allow users to open a popout window to reset, delete, or edit the button.
    def show_edit_choices(e):
        nonlocal current_active_chore, current_active_row
        data_dict = e.control.data
        current_active_chore = data_dict["button"]
        current_active_row = data_dict["row"]
        page.show_dialog(edit_choice_dialog)
        page.update()

# This function will prompt another popout window to confirm the users action to reset or delete the button.
    def show_edit_confirm(e):
        nonlocal current_action
        if e.control.data == "Reset to Zero":
            current_action = "reset"
        elif e.control.data == "Delete":
            current_action = "delete"
        page.pop_dialog()
        page.show_dialog(edit_confirm_dialog)
        page.update()

# This function will allow users to open a settings popout window to change the pages color scheme.
# Future enhancements will be to allow for English or Spanish text.
    def page_select_update(e):
        nonlocal page_select
        total_paid_index = 0
        if page_select.value == "Page 2":
            total_paid_index = 1
        elif page_select.value == "Page 3":
            total_paid_index = 2
        selected_page = page_select.value
        chore_column_1.visible = (selected_page == "Page 1")
        chore_column_2.visible = (selected_page == "Page 2")
        chore_column_3.visible = (selected_page == "Page 3")
        main_title_update()
        dropdown_view.visible = True
        dropdown_select_view.visible = False
        grand_chore_total.value = f"Total: ${total[total_paid_index]:.2f}"
        save_app_data()
        page.update()
    
    def page_theme_update(e):
        nonlocal page_theme, page_theme_settings, page_select
        selected_theme = page_theme.value
        if selected_theme == "Tangerine":
            page_theme_settings["Font"] = ft.Colors.ORANGE_800
            page_theme_settings["Back Ground"] = ft.Colors.ORANGE_100
        elif selected_theme == "Rose":
            page_theme_settings["Font"] = ft.Colors.RED_700
            page_theme_settings["Back Ground"] = ft.Colors.RED_100
        elif selected_theme == "Cool":
            page_theme_settings["Font"] = ft.Colors.BLUE_700
            page_theme_settings["Back Ground"] = ft.Colors.LIGHT_BLUE_100
        elif selected_theme == "Steel":
            page_theme_settings["Font"] = ft.Colors.BLUE_GREY_700
            page_theme_settings["Back Ground"] = ft.Colors.GREY_100  
        elif selected_theme == "Limon":
            page_theme_settings["Font"] = ft.Colors.LIGHT_GREEN_500
            page_theme_settings["Back Ground"] = ft.Colors.YELLOW_200  
        else:
            page_theme_settings["Font"] = ft.Colors.ORANGE_800
            page_theme_settings["Back Ground"] = ft.Colors.ORANGE_100
        
        total_paid_index = 0
        if page_select.value == "Page 2":
            total_paid_index = 1
        elif page_select.value == "Page 3":
            total_paid_index = 2
        selected_page = page_select.value
        main_title_update()
        chore_column_1.visible = (selected_page == "Page 1")
        chore_column_2.visible = (selected_page == "Page 2")
        chore_column_3.visible = (selected_page == "Page 3")

        page.bgcolor = page_theme_settings["Back Ground"]   
        new_chore_title.color = page_theme_settings["Font"]
        new_chore_price.color = page_theme_settings["Font"]
        submit_button.color =  page_theme_settings["Font"]
        main_title.color = page_theme_settings["Font"]
        add_button_view.color =  page_theme_settings["Font"]
        exit_button.color =  page_theme_settings["Font"]
        pay_out_button.color =  page_theme_settings["Font"]
        for col in all_chore_columns:
            for row in col.controls:
                if isinstance(row, ft.Row) and row.controls:
                    btn = row.controls[0]
                    if isinstance(btn, ft.ElevatedButton):
                        btn.content.controls[0].color = page_theme_settings["Font"]
                        btn.content.controls[1].color = page_theme_settings["Font"]
        grand_chore_total.value = f"Total: ${total[total_paid_index]:.2f}"
        save_app_data()
        if e is not None:
            page.pop_dialog()
        page.update()

# This function will allow the user to edit the chore name and chore price.
    def show_button_edit(e):
        nonlocal current_active_chore
        page.pop_dialog()
        if current_active_chore and current_active_chore.data:
            input_field.value = current_active_chore.data["title"]
            input_field_2.value = str(current_active_chore.data["price"])
        page.show_dialog(edit_button_dialog)
        page.update()
 
    def show_pay_chore(e):
        nonlocal input_field_3
        page.show_dialog(pay_chore_dialog)
        page.update()

#This block creates a method to create dynamic buttons and keep a running total.
    def show_input_view():
        main_view.visible = False
        input_view.visible = True
        page.update()

    def show_settings_view():
        page.show_dialog(settings_dialog)
        page.update()
        
    def submit(e):
        nonlocal page_select
        title_text = new_chore_title.value
        try:
            price_text = float(new_chore_price.value)
        except ValueError:
            price_text = 0.00

        chore_row = create_chore_row(title_text, price_text)
        new_chore_title.value = ""
        new_chore_price.value = ""
        current_column = get_current_column()
        current_column.controls.append(chore_row)
        
        input_view.visible = False
        main_view.visible = True
        update_total_add()
        page.update()

# This function will create the new chore.
    def create_chore_row(title_text, price_text, initial_sum=0.00):
        initial_data = {"title": title_text, "price": price_text, "sum": initial_sum}            
        target_button = ft.ElevatedButton(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=190,
                #width=500,
                controls=[
                    ft.Text(
                        f"{title_text}:",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color=page_theme_settings["Font"],
                    ), 
                    ft.Text(
                        f"${initial_data['sum']:.2f}",
                        size=15,
                        color=page_theme_settings["Font"]
                    )
                ]
            ),
            bgcolor=ft.Colors.WHITE,
        data = initial_data,
        on_click=button_click,
        )

        action_button = ft.IconButton(                
            ft.Icon(ft.Icons.EDIT, size=30),                    
            on_click = show_edit_choices,
            data = {"button": target_button, "row": None}
        )

        chore_row = ft.Row(
            controls=[
                target_button,
                action_button
            ],
            alignment=ft.MainAxisAlignment.START
        )
        chore_row.controls[1].data["row"] = chore_row
        return chore_row
    
#This function will handle the action of resetting or deleting the button.
    def action_handler_yes(e):
        nonlocal current_action
        if current_action == "reset":
            reset_button(e)
        elif current_action == "delete":
            delete_button(e)
        current_action=None
        page.pop_dialog()
        page.update()
  
#This function creates a method to reset the buttons sum back to $0.00.    
    def reset_button(e):
        nonlocal current_active_chore
        if current_active_chore and current_active_chore.data and "price" in current_active_chore.data:
            current_active_chore.data["sum"] = float(0.00)
            current_active_chore.content.controls[1].value =f"${current_active_chore.data['sum']:.2f}"
        current_active_chore = None
        update_total_add()
 
# This fucntion edits the chore title and/or chore price.
    def edit_button(e):
        nonlocal current_active_chore
        if current_active_chore and current_active_chore.data:
            if input_field.value.strip():
                current_active_chore.data["title"] = input_field.value.strip()
            if input_field_2.value.strip():
                try:
                    current_active_chore.data["price"] = float(input_field_2.value.strip())
                except ValueError:
                    pass
            new_title = current_active_chore.data["title"]
            new_price = current_active_chore.data["price"]
            current_active_chore.content.controls[0].value =(f"{new_title}:")
        input_field.value = ""
        input_field_2.value = ""
        page.pop_dialog()
        update_total_add()
        current_active_chore = None
            
#This function creates a method to delete the button. 
    def delete_button(e):
        nonlocal current_active_row, current_active_chore
        current_column = get_current_column()
        if current_active_row and current_column.controls:
            if current_active_chore in current_column.controls:
                current_column.controls.remove(current_active_chore)
            if current_active_row in current_column.controls:
                current_column.controls.remove(current_active_row)
        current_active_row = None    
        current_active_chore = None  
        update_total_add()

#This function creates a method to increase the button's sum by the price of the chore.
    async def button_click(e):
        button = e.control
        if button.data and "price" in button.data:
            button.data["sum"] += button.data["price"]
            button.content.controls[1].value =f"${button.data['sum']:.2f}"
        update_total_add()
        await play_audio()
        page.update()

#this function ensures a clean closing of the dialog boxes.
    def close_dialog(e):
        page.pop_dialog()
        page.show_dialog(edit_choice_dialog)
        page.update()

#This function ensures a clean closing of the settings dialog box.    
    def close_dialog_2(e):
        page.pop_dialog()
        page.update()

#This functions keeps a running total of the buttons everytime one is created, the button is clicked, the button is reset, and the button is deleted.
    def update_total_add():
        nonlocal total, total_paid
        total_paid_index = 0
        if page_select.value == "Page 2":
            total_paid_index = 1
        elif page_select.value == "Page 3":
            total_paid_index = 2
        current_total = total_paid[total_paid_index]
        current_column = get_current_column()
        for row in current_column.controls:
            if isinstance(row, ft.Row) and row.controls:
                control = row.controls[0]
                if isinstance(control, ft.ElevatedButton) and control.data:
                    current_total += control.data.get("sum", 0.0)
        total[total_paid_index] = current_total
        grand_chore_total.value = f"Total: ${total[total_paid_index]:.2f}"
        save_app_data()
        page.update()

#This function prompts a popout window to ask how much was paid out.
    async def update_total_sub():
        nonlocal input_field_3, total_paid, total
        total_paid_index = 0
        if page_select.value == "Page 2":
            total_paid_index = 1
        elif page_select.value == "Page 3":
            total_paid_index = 2
        current_total = total[total_paid_index]
        current_total -= float(input_field_3.value) if input_field_3.value else 0.00
        total_paid[total_paid_index] = current_total
        input_field_3.value = ""
        reset_button_all()
        await play_audio_2()

# This function will reset all of the button sums to $0 after an ammount was paid out.
    def reset_button_all():
        current_page = get_current_column()
        for row in current_page.controls:
            if isinstance(row, ft.Row) and row.controls:
                buttons = row.controls[0]   
                if isinstance(buttons, ft.ElevatedButton) and buttons.data:
                    buttons.data["sum"] = 0.0
                    buttons.content.controls[1].value =f"${buttons.data['sum']:.2f}"        
        page.pop_dialog()
        update_total_add()

# This function hide the input fields of a new chore.
    def hide_input_view():
        input_view.visible = False
        main_view.visible = True
        page.update()

# This function updates the text of the dropdown menu for page select.
    def rename_page_select_options(e):
        nonlocal page_select, page_select_rename, new_page_title
        new_title = new_page_title.value.strip()
        selected_page = page_select_rename.value
        if not new_title or not selected_page:
            return
        for options in page_select.options:
            if options.key == selected_page:
                options.text = new_title
                break
        for options in page_select_rename.options:
            if options.key == selected_page:
                options.text = new_title
                break  
        page_select.value = selected_page
        page_select_update(None)
        new_page_title.value = "" 
        page_select_rename.value = ""
        page.pop_dialog()         
        page.update()

# This function will change the view from dropdown_view to dropdown_select_view
    def dropdown_view_select(e=None):
            dropdown_select_view.visible = True
            dropdown_view.visible = False
            page.update()
        
# This function will allow the sound effects to play when a chore button is clicked.
    async def play_audio():
        await audio_player.play()

    async def play_audio_2():
        await audio_player_2.play()

    async def audio_sound_control(e: ft.Event[ft.Switch]):
        audio_player.volume = 1.0 if e.control.value else 0.0
        audio_player_2.volume = 0.65 if e.control.value else 0.0
        
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  ----------Build all of the Dialog Popouts------------
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++

   
    settings_dialog = ft.AlertDialog(
        modal = True,
        title = ft.Text("Settings"),
        content = ft.Column(
            controls=[
                ft.Text("Rename Page:"),
                new_page_title,
                page_select_rename,
                ft.ElevatedButton(content=ft.Text("submit"), on_click=lambda e: rename_page_select_options(e)),
                ft.Divider(height=0),
                ft.Text("Color Theme:"),
                page_theme, 
                ft.ElevatedButton(content=ft.Text("submit"), on_click=page_theme_update), 
                ft.Divider(height=0), 
                ft.Text("Sound On/Off"),
                ft.Switch(value=True, on_change=audio_sound_control),
            ],
            tight=True
        ),
        actions=[
            ft.ElevatedButton("Exit", on_click=lambda e: close_dialog_2(e)),  
        ],
    )

    edit_choice_dialog = ft.AlertDialog(
        modal = True,
        title = ft.Text("Edit Chore"),
        content = ft.Text("What do you want to do?"),
        actions=[
            ft.ElevatedButton("Reset to Zero", on_click=show_edit_confirm, data="Reset to Zero"),
            ft.ElevatedButton("Delete", on_click=show_edit_confirm, data="Delete"),
            ft.ElevatedButton("Edit title/price", on_click=show_button_edit),
        ],
    )

    edit_confirm_dialog = ft.AlertDialog(
        modal = True,
        title = ft.Text("Edit Chore"),
        content = ft.Text("Are you sure?"),
        actions=[
            ft.ElevatedButton("Yes", on_click=action_handler_yes),
            ft.ElevatedButton("No", on_click=lambda e: close_dialog(e)), 
        ],
    )

    edit_button_dialog = ft.AlertDialog(
        modal = True,
        title = ft.Text("Edit Chore"),
        content = ft.Column([input_field, input_field_2], tight=True),
        actions=[
            ft.ElevatedButton("Save", on_click=lambda e: edit_button(e))
        ],
    )

    pay_chore_dialog = ft.AlertDialog(
        modal=True,
        title = ft.Text("How much did you pay?!"),
        content = ft.Column([input_field_3], tight=True),
        actions=[
            ft.ElevatedButton("Save", on_click=update_total_sub)
        ],
    )


#This block will create the new text fields, dropdowns, and buttons.
    new_chore_title = ft.TextField(
        label = "New Chore Title",
        max_length=40,
        #width=550,
        border_radius=30,
        border_color=ft.Colors.GREY_500,
        bgcolor=ft.Colors.WHITE,
        read_only=False,
        text_align=ft.TextAlign.CENTER,
        color=page_theme_settings["Font"], 
        border_width=0)
    
    new_chore_price = ft.TextField(
        label = "New Chore Price", 
        input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",
            replacement_string=""
        ), 
       # width=550,
        color=page_theme_settings["Font"],  
        border_width=0,
        border_radius=30,
        text_align=ft.TextAlign.CENTER,
        border_color=ft.Colors.GREY_500,
        bgcolor=ft.Colors.WHITE,
    )
    
    submit_button = ft.ElevatedButton(
        content="SUBMIT", 
        on_click=submit,
        color=page_theme_settings["Font"],
        bgcolor=ft.Colors.WHITE,
    )


    exit_button = ft.ElevatedButton(
        content="Exit",
        on_click = hide_input_view,
        color=page_theme_settings["Font"],
        bgcolor=ft.Colors.WHITE
    )
    
    add_button_view = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, size=30)
            ],
        ),
        on_click=show_input_view,
        color=page_theme_settings["Font"],
        bgcolor=ft.Colors.WHITE,
    )

    settings_button = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.SETTINGS, size=30)
            ],
        ),
        on_click=show_settings_view,
        color=ft.Colors.BLACK_87,
        bgcolor=ft.Colors.WHITE
    )

    pay_out_button = ft.ElevatedButton(
        content=ft.Column(
            [ft.Icon(ft.Icons.ATTACH_MONEY, size=30)
            ],
        ),
        on_click=show_pay_chore,
        color=page_theme_settings["Font"],
        bgcolor=ft.Colors.WHITE,        
    )
                        
    main_view =ft.Column(
        controls=[
            ft.Row(
                controls=[
                    add_button_view,
                    settings_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        ],
        visible = True,
    )
      
    input_view = ft.Column(
        controls=[
        new_chore_title,
        new_chore_price,
        ft.Row(
            controls=[
                submit_button,
                exit_button,
            ]
        )
        ],
        visible = False
    )

    dropdown_view = ft.Row(
        controls=[
            page_title,
            ft.IconButton(ft.Icons.ARROW_DROP_DOWN, on_click= dropdown_view_select)
        ],
        visible = True
    )

    dropdown_select_view = ft.Column(
        controls=[
        page_select
        ],
        visible = False
    )

# This block will load the saved state from client storage.
    def load_app_data():
        nonlocal total, total_paid
        if os.path.exists(STORAGE_FILE):
            try:
                with open(STORAGE_FILE, "r") as f:
                    stored_data = json.load(f)
                total = stored_data.get("total", [0.0, 0.0, 0.0])
                total_paid = stored_data.get ("total_paid", [0.0, 0.0, 0.0])

                #Load stored dropdown page names
                stored_options = stored_data.get("page_options", [])
                if stored_options:
                    for i, opt_data in enumerate(stored_options):
                        if i < len(page_select.options):
                            page_select.options[i].text = opt_data["text"]
                            page_select_rename.options[i].text = opt_data["text"]
                # Load the chores into columns before the UI displays update
                chores_by_page = stored_data.get("chores", {})
                column_mapping = {
                    "Page 1": chore_column_1,
                    "Page 2": chore_column_2,
                    "Page 3": chore_column_3,
                }
                for p_key, col_target in column_mapping.items():
                    for chore in chores_by_page.get(p_key, []):
                        row = create_chore_row(chore["title"], chore["price"], chore["sum"])
                        col_target.controls.append(row)

                #Set theme and selected page without triggering a wipe.
                saved_theme = stored_data.get("theme_name", "Tangerine")
                page_theme.value = saved_theme
                page_select.value = stored_data.get("selected_page", "Page 1")
                page_theme_update(None)
                page_select_update(None)
                
    
            except Exception as err:
                print("Failed to load client storage state", err)

    #Call the load_app_data function before UI renders.
    load_app_data()

    #This block creates the columns.
    page.scroll = None

    page.add(
        ft.Container(
            margin=ft.Margin.all(20),
            expand=True,
            content=ft.Column(
                scroll=None,
                expand= True,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                    main_title,
                                    dropdown_view,
                                    dropdown_select_view,
                                ],
                            ), 
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=30), 
                    main_view,
                    input_view,
                    ft.Divider(height=30),
                    ft.Column(
                        scroll=ft.ScrollMode.ADAPTIVE,
                        expand=True,
                        controls=[
                            chore_column_1,
                            chore_column_2,
                            chore_column_3,
                            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ],
                    ),
                    ft.Divider(height=30),
                    ft.Column(
                        controls=[
                            grand_chore_total,
                        ],
                    ),
                    pay_out_button,
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ],
            )
        )
    )


#This block allows the code to be ran.
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")