import os, sys
sys.path.append(os.getcwd())

import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox
from update_userdata import git_pull, git_push, return_data, set_data
from links import links, zone_time_data
from datetime import datetime, time, timedelta, date

import time as t

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH)

        self.userdata = self.get_userdata()
        self.booking_data = self.intialize_booking_dict()


        self.display_dashboard()

    def get_userdata(self) -> dict:
        try:
            git_pull()
            return return_data()
        except:
            return None
    
    def display_dashboard(self) -> None:
        title = tk.Label(self.master, text='ArcBooker UI', font=('calibri', 20), borderwidth=3, relief='ridge')
        title.pack(fill=tk.X)

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        if self.userdata:
            self.active_user = tk.StringVar(self.current_frame, None)

            user_frame = tk.Frame(self.current_frame)
            user_frame.pack()

            user_options = self.userdata.keys()

            user_label = tk.Label(user_frame, text='User:')
            user_label.pack(side=tk.LEFT)

            self.user_dropdown = tk.OptionMenu(user_frame, self.active_user, *user_options, command=self.handle_user_select)
            self.user_dropdown.config(width=10)
            self.user_dropdown.pack(pady=3, side=tk.RIGHT)

            self.initialize_booking_form()

            seperator = ttk.Separator(self.current_frame, orient=tk.HORIZONTAL)
            seperator.pack(fill=tk.X, pady=4)

            self.new_user_form()

        
        else:
            error_label = tk.Label(self.current_frame, text='Uh oh, could not load userdata', font=('calibri', 20))
            error_label.pack(fill=tk.BOTH, pady=100)
    
    def new_user_form(self) -> None:

        form_frame = tk.Frame(self.current_frame)
        form_frame.pack()

        name_label = tk.Label(form_frame, text='Name:')
        name_label.grid(row=0, column=0, padx=2)

        self.new_user_var = StringVar(self.master)
        name_entry = tk.Entry(form_frame, textvariable=self.new_user_var)
        name_entry.configure(width=10)
        name_entry.grid(row=1, column=0, padx=2)

        user_label = tk.Label(form_frame, text='OnQ Username:')
        user_label.grid(row=0, column=1, padx=2)

        self.username_var = StringVar(self.master)
        username_entry = tk.Entry(form_frame, textvariable=self.username_var)
        username_entry.grid(row=1, column=1, padx=2)

        pass_label = tk.Label(form_frame, text='Password:')
        pass_label.grid(row=0, column=2, padx=2)

        self.password_var = StringVar(self.master)
        password_entry = tk.Entry(form_frame, textvariable=self.password_var)
        password_entry.grid(row=1, column=2, padx=2)

        confirm_button = tk.Button(form_frame, text='Add User', command=self.add_user)
        confirm_button.grid(row=1, column=3, padx=2)
    
    def add_user(self):
        new_user = self.new_user_var.get()
        if new_user and new_user not in self.userdata.keys():
            default_booking = self.default_booking_data()
            self.userdata[new_user] = {
                'username': self.username_var.get(),
                'password': self.password_var.get(),
                'bookings': default_booking
            }

            self.active_user.set(new_user)
            self.user_dropdown['menu'].add_command(label=new_user, command=tk._setit(self.active_user, new_user, self.handle_user_select(new_user)))

            self.handle_user_select(new_user)
            set_data(self.userdata)
            git_push()
    
    
    def initialize_booking_form(self) -> None:
        

        form_frame = tk.Frame(self.current_frame)
        form_frame.pack(fill=tk.BOTH)

        booking_zones = links.keys()

        self.booking_form = dict()
        for day in WEEKDAYS:
            self.booking_form[day] = dict()

        count = 0
        for day in WEEKDAYS:
            day_label = tk.Label(form_frame, text=day+'    -->', font='bold', anchor='w', width=15)
            day_label.grid(row=count, column=0, pady=4, padx=4)

            zone_label = tk.Label(form_frame, text='Zone:', anchor='w')
            zone_label.grid(row=count, column=1, pady=4, padx=4)

            time_dropdown = tk.OptionMenu(form_frame, self.booking_data[day]['time'], None)
            time_dropdown.config(width=13)
            time_dropdown.grid(row=count, column=4, padx=4, pady=4)
            self.booking_form[day]['time'] = time_dropdown

            zone_dropdown = tk.OptionMenu(form_frame, self.booking_data[day]['booking_zone'], *booking_zones, 'None', command=self.handle_zone_select)
            zone_dropdown.config(width=13)
            zone_dropdown.grid(row=count, column=2, padx=4, pady=4)
            self.booking_form[day]['booking_zone'] = zone_dropdown

            time_label = tk.Label(form_frame, text='Time:', anchor='w')
            time_label.grid(row=count, column=3, pady=4, padx=4)

            count += 1
        
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=count+1, columnspan=6)

        update_button = tk.Button(button_frame, text='Update User', command=self.update_userdata)
        update_button.pack(side=tk.LEFT, padx=10)

        delete_button = tk.Button(button_frame, text='Delete User', command=self.delete_user)
        delete_button.pack(side=tk.RIGHT, padx=10)
    
    def handle_zone_select(self, val):
        for day, var in self.booking_data.items():
            zone = var['booking_zone'].get()
            if zone != 'None': 
                times = self.get_time_list(zone)
                time_widget = self.booking_form[day]['time']
                time_widget['menu'].delete(0, tk.END)
                for time in times:
                    time_widget['menu'].add_command(label=time, command=tk._setit(var['time'], time))
            else:
                time_widget = self.booking_form[day]['time']
                time_widget['menu'].delete(0, tk.END)
                time_widget['menu'].add_command(label=None, command=tk._setit(var['time'], None))
                var['time'].set(None)

    
    def get_time_list(self, zone):
        fh = zone_time_data[zone]['first_hour']
        fm = zone_time_data[zone]['first_minute']
        lh = zone_time_data[zone]['last_hour']
        lm = zone_time_data[zone]['last_minute']

        time_list = []

        dt = datetime.combine(date.today(), time(fh, fm))
        end_t = datetime.combine(date.today(),time(lh, lm))
        td = timedelta(hours=1, minutes=15)
        while dt <= end_t:
            time_list.append(dt.strftime('%H:%M'))
            dt = dt + td
        
        return time_list
    
    def default_booking_data(self) -> dict:
        booking_dict = dict()

        for day in WEEKDAYS:
            booking_dict[day] = {
                'zone': 'lower-squatrack',
                'time': '07:45'
            }

        return booking_dict


    def intialize_booking_dict(self) -> dict:
        booking_dict = dict()

        for day in WEEKDAYS:
            booking_dict[day] = {
                'booking_zone': tk.StringVar(self.master, 'None'),
                'time': tk.StringVar(self.master)
            }

        return booking_dict
    
    def handle_user_select(self, value):
        if value and value != '':
            current_userdata = self.userdata[value]

            for day, data in current_userdata['bookings'].items():
                self.booking_data[day]['booking_zone'].set(data['zone'])
                self.booking_data[day]['time'].set(data['time'])
            
            self.handle_zone_select(None)

    def update_userdata(self):
        active_user = self.active_user.get()
        if active_user and active_user != '':
            current_userdata = self.userdata[self.active_user.get()]

            for day, data in current_userdata['bookings'].items():
                data['zone'] = self.booking_data[day]['booking_zone'].get()
                data['time'] = self.booking_data[day]['time'].get()
        
            set_data(self.userdata)
            git_push()
            
    
    def delete_user(self):
        active_user = self.active_user.get()
        if active_user and active_user != '':
            answer = messagebox.askokcancel(title='Confirm Delete', message='Are you sure you want to delete user {}'.format(self.active_user.get()))
            if answer:
                self.userdata.pop(active_user)

                self.user_dropdown['menu'].delete(0, tk.END)
                for user in self.userdata.keys():
                    self.user_dropdown['menu'].add_command(label=user, command=tk._setit(self.active_user, user, self.handle_user_select(user)))
                
                self.active_user.set(user)

                set_data(self.userdata)
                git_push()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x450')
    app = Application(master=root)
    app.mainloop()