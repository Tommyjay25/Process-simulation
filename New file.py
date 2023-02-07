from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.chip import MDChip
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu
import random as rnd
import pandas as pd
from statsmodels.tsa.api import SimpleExpSmoothing
import numpy
from kivymd.uix.list import MDList, OneLineListItem
"""
from kivy.uix.textinput import TextInput
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from datetime import date, datetime
import pandas as pd
from firebase import firebase
from kivy.properties import StringProperty
ThreeLineListItem, TwoLineListItem, TwoLineAvatarIconListItem,IRightBodyTouch, IconLeftWidget, OneLineIconListItem
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDIconButton
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
from kivymd.theming import ThemableBehavior
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from pyzbar.pyzbar import decode"""

class MyWidget(MDChip):
    def __init__(self, **kwargs):
        self.label = App.get_running_app().title
        super().__init__(**kwargs)


class Process(MDApp):
    def __init__(self, **kwargs):
        self.title = "Balance App"
        super().__init__(**kwargs)
        self.kv = Builder.load_file('Materia.kv')
        Window.size = (800, 800)

        flavor_pick = ("Lemon", "Pineapple", "Orange")
        menu_flavors = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in flavor_pick
        ]
        self.menu = MDDropdownMenu(
            caller=self.kv.ids.add_rm,
            items=menu_flavors,
            width_mult=4,
        )

    def menu_callback(self, x):
        self.add_flavor=Label(size_hint=(0.1,0.1),pos_hint={"x":0.15,"y":0.48},color=(0,0,0,1))
        self.add_flavor.text=f'{x}'
        self.root.ids.pagina_principal.add_widget(self.add_flavor)
        self.number_of_units=MDTextField(size_hint=(0.08,0.08),pos_hint={"x":0.08,"y":0.46},on_text_validate=self.accept)
        self.root.ids.pagina_principal.add_widget(self.number_of_units)
        self.menu.dismiss()
    def accept(self,*args):
        if self.number_of_units.text!="":
            self.btn_accept=Button(size_hint=(0.08,0.05),pos_hint={"x":0.18,"y":0.46},text="accept",on_release=self.add_to_RMWH)
            self.root.ids.pagina_principal.add_widget(self.btn_accept)
        else:
            pass
    def add_to_RMWH(self,*args):
        self.RM_containers[self.add_flavor.text]=int(self.RM_containers[self.add_flavor.text])+int(self.number_of_units.text)
        self.root.ids.pagina_principal.remove_widget(self.add_flavor)
        self.root.ids.pagina_principal.remove_widget(self.number_of_units)
        self.root.ids.pagina_principal.remove_widget(self.btn_accept)
    """Creating a  dictionary to get the most I can get from any stage hourly
    they produce random ammounts of unities"""

    stage={"stage_1":rnd.randrange(1800,2000), "stage_2":rnd.randrange(2100,2300),
           "stage_3": rnd.randrange(2400,2600)}


    """Defining previous demand per month"""
    DF=pd.read_excel(r'demand_Database.xlsx')

    """Units can be transport everyday to the customers"""
    units_transported_daily=2500

    """When you change a product there's one hour and a half of cleaning"""
    cleaning_process=1
    RM_containers = {"Lemon": 900, "Pineapple": 1000, "Orange": 1000}
    def RMWH(self):
        """Use to define what's in every container to take it when is necessary"""

        try:
            if self.RM_containers[self.flavor] >= 180:
                try:
                    self.root.ids.pagina_principal.remove_widget(self.raw_mat_quantities)
                    self.raw_mat_quantities = Label(pos_hint={"x": 0.15, "y": 0.75}, size_hint=(0.10, 0.05), color=(0, 0, 0, 1))
                    self.raw_mat_quantities.text = f'Warehouse stock:\n {round(self.RM_containers[self.flavor], 2)} containers\nof {self.flavor} juice' \
                                                   f'\nStock: \n Lemon: {round(float(self.RM_containers["Lemon"]),2)}\n Pineapple: {round(float(self.RM_containers["Pineapple"]),2)}\n Orange: {round(float(self.RM_containers["Orange"]),2)}'
                    self.root.ids.pagina_principal.add_widget(self.raw_mat_quantities)
                except:
                    self.raw_mat_quantities = Label(pos_hint={"x": 0.15, "y": 0.75}, size_hint=(0.10, 0.05), color=(0, 0, 0, 1))
                    self.raw_mat_quantities.text = f'Warehouse stock:\n {round(self.RM_containers[self.flavor], 2)} containers\nof {self.flavor} juice' \
                                                   f'\nStock: \n Lemon: {round(float(self.RM_containers["Lemon"]), 2)}\n Pineapple: {round(float(self.RM_containers["Pineapple"]), 2)}\n Orange: {round(float(self.RM_containers["Orange"]), 2)}'
                    self.root.ids.pagina_principal.add_widget(self.raw_mat_quantities)
            else:
                try:
                    self.root.ids.pagina_principal.remove_widget(self.raw_mat_quantities)
                    self.raw_mat_quantities = Label(pos_hint={"x": 0.15, "y": 0.75}, size_hint=(0.10, 0.05),
                                                    color=(0, 0, 0, 1))
                    self.raw_mat_quantities.text = f'Add stock of {self.flavor} \nStock: \n Lemon: {round(float(self.RM_containers["Lemon"]), 2)}\n Pineapple: {round(float(self.RM_containers["Pineapple"]), 2)}\n Orange: {round(float(self.RM_containers["Orange"]), 2)}'
                    self.root.ids.pagina_principal.add_widget(self.raw_mat_quantities)
                except:
                    self.raw_mat_quantities = Label(pos_hint={"x": 0.15, "y": 0.75}, size_hint=(0.10, 0.05),
                                                    color=(0, 0, 0, 1))
                    self.raw_mat_quantities.text = f'Add stock of {self.flavor} \nStock: \n Lemon: {round(float(self.RM_containers["Lemon"]), 2)}\n Pineapple: {round(float(self.RM_containers["Pineapple"]), 2)}\n Orange: {round(float(self.RM_containers["Orange"]), 2)}'
                    self.root.ids.pagina_principal.add_widget(self.raw_mat_quantities)
        except:
            try:
                self.root.ids.pagina_principal.remove_widget(self.raw_mat_quantities)
                self.raw_mat_quantities = Label(pos_hint={"x": 0.15, "y": 0.75}, size_hint=(0.10, 0.05), color=(0, 0, 0, 1))
                self.raw_mat_quantities.text = f'\nStock: \n Lemon: {round(float(self.RM_containers["Lemon"]), 2)}\n Pineapple: {round(float(self.RM_containers["Pineapple"]), 2)}\n Orange: {round(float(self.RM_containers["Orange"]), 2)}'
                self.root.ids.pagina_principal.add_widget(self.raw_mat_quantities)
            except:
                self.raw_mat_quantities = Label(pos_hint={"x": 0.15, "y": 0.75}, size_hint=(0.10, 0.05),
                                                color=(0, 0, 0, 1))
                self.raw_mat_quantities.text = f'\nStock: \n Lemon: {round(float(self.RM_containers["Lemon"]), 2)}\n Pineapple: {round(float(self.RM_containers["Pineapple"]), 2)}\n Orange: {round(float(self.RM_containers["Orange"]), 2)}'
                self.root.ids.pagina_principal.add_widget(self.raw_mat_quantities)


    """This is going to be the method to add raw material to the warehouse"""


    def S1(self):

            try:
                if self.RM_containers[self.flavor] >= 180:
                    """In case someone wants to start the process without the documentation"""
                    try:
                        self.root.ids.pagina_principal.remove_widget(self.S1_sumary)
                        """Number of containers need it"""
                        self.containers_needed=self.real_forcast/150
                        """This one code reduce the amount of containers when they are used for the manufacturing process"""
                        self.RM_containers[self.flavor]=int(self.RM_containers[self.flavor])-self.containers_needed
                        """Number of hours need it"""
                        self.total_hours=self.real_forcast/int(self.stage["stage_1"])
                        self.S1_sumary=Label(pos_hint={"x":0.40,"y":0.65},size_hint=(0.25,0.30),color=(0,0,0,1))
                        self.S1_sumary.text=f"Units worked: {self.real_forcast} \nRemaining quantity in warehouse {round(self.RM_containers[self.flavor],2)} \nContainers needed: {round(self.containers_needed,2)} \nTotal hours: {round(self.total_hours,2)} hours"
                        self.root.ids.pagina_principal.add_widget(self.S1_sumary)
                        self.Total_hours_list_s1.append(self.total_hours)
                    except:
                        """Number of containers need it"""
                        self.containers_needed=self.real_forcast/150
                        """This one code reduce the amount of containers when they are used for the manufacturing process"""
                        self.RM_containers[self.flavor]=int(self.RM_containers[self.flavor])-self.containers_needed
                        """Number of hours need it"""
                        self.total_hours=self.real_forcast/int(self.stage["stage_1"])
                        self.S1_sumary=Label(pos_hint={"x":0.40,"y":0.65},size_hint=(0.25,0.30),color=(0,0,0,1))
                        self.S1_sumary.text=f"Units worked: {self.real_forcast} \nRemaining quantity in warehouse {round(self.RM_containers[self.flavor],2)} \nContainers needed: {round(self.containers_needed,2)} \nTotal hours: {round(self.total_hours,2)} hours"
                        self.root.ids.pagina_principal.add_widget(self.S1_sumary)
                        self.Total_hours_list_s1.append(self.total_hours)
                else:
                    self.root.ids.pagina_principal.remove_widget(self.S1_sumary)
                    self.S1_sumary = Label(pos_hint={"x": 0.40, "y": 0.65}, size_hint=(0.25, 0.30), color=(0, 0, 0, 1))
                    self.S1_sumary.text = "Check Raw material stock"
                    self.root.ids.pagina_principal.add_widget(self.S1_sumary)
            except:
                """Process can't start without proper documentation"""
                self.S1_sumary = Label(pos_hint={"x": 0.40, "y": 0.65}, size_hint=(0.25, 0.30), color=(0, 0, 0, 1))
                self.S1_sumary.text = "Production order has not been released"
                self.root.ids.pagina_principal.add_widget(self.S1_sumary)
    scrap_list_p1=[]
    scrap_list_p2 = []
    scrap_list_p3 = []
    def S2(self):
        if self.S1_sumary.text == "Check Raw material stock":
            self.root.ids.pagina_principal.remove_widget(self.S2_sumary)
            self.S2_sumary = Label(pos_hint={"x": 0.40, "y": 0.45}, size_hint=(0.25, 0.30), color=(0, 0, 0, 1))
            self.S2_sumary.text = "Check Raw material stock"
            self.root.ids.pagina_principal.add_widget(self.S2_sumary)
        else:
            try:
                try:
                    self.root.ids.pagina_principal.remove_widget(self.S2_sumary)
                    """Number of hours need it"""
                    self.units_received=self.real_forcast-self.real_forcast*rnd.uniform(0,0.03)
                    self.total_hours_2=self.units_received/int(self.stage["stage_2"])
                    self.S2_sumary=Label(pos_hint={"x":0.35,"y":0.45},size_hint=(0.25,0.30),color=(0,0,0,1))
                    self.scrap2=int(self.real_forcast-self.units_received)
                    self.S2_sumary.text=f"Units worked: {int(self.units_received)} \nScrap:{self.scrap2}\nProduction yeild {round((self.units_received/self.real_forcast)*100,2)}% \nTotal hours: {round(self.total_hours_2,2)} hours"
                    self.root.ids.pagina_principal.add_widget(self.S2_sumary)

                    self.Total_hours_list_s2.append(self.total_hours_2)
                    if self.Product_1==1:
                        self.scrap_list_p1.append(self.scrap2)
                    elif self.Product_2==1:
                        self.scrap_list_p2.append(self.scrap2)
                    elif self.Product_3==1:
                        self.scrap_list_p3.append(self.scrap2)
                except:
                    """Number of hours need it"""
                    self.units_received = self.real_forcast - self.real_forcast * rnd.uniform(0, 0.03)
                    self.total_hours_2 = self.real_forcast / int(self.stage["stage_2"])
                    self.S2_sumary = Label(pos_hint={"x": 0.35, "y": 0.45}, size_hint=(0.25, 0.30), color=(0, 0, 0, 1))
                    self.scrap2=int(self.real_forcast - self.units_received)
                    self.S2_sumary.text = f"Units worked: {int(self.units_received)} \nScrap:{self.scrap2}\nProduction yeild {round((self.units_received / self.real_forcast) * 100, 2)}% \nTotal hours: {round(self.total_hours_2, 2)} hours"
                    self.root.ids.pagina_principal.add_widget(self.S2_sumary)
                    self.Total_hours_list_s2.append(self.total_hours_2)
                    if self.Product_1==1:
                        self.scrap_list_p1.append(self.scrap2)
                    elif self.Product_2==1:
                        self.scrap_list_p2.append(self.scrap2)
                    elif self.Product_3==1:
                        self.scrap_list_p3.append(self.scrap2)
            except:
                """Process can't start without proper documentation"""
                self.S2_sumary = Label(pos_hint={"x": 0.40, "y": 0.45}, size_hint=(0.25, 0.30), color=(0, 0, 0, 1))
                self.S2_sumary.text = "Production order has not been released"
                self.root.ids.pagina_principal.add_widget(self.S2_sumary)

    def S3(self):
        if self.S2_sumary.text == "Check Raw material stock":
            self.root.ids.pagina_principal.remove_widget(self.S3_sumary)
            self.S3_sumary = Label(pos_hint={"x": 0.40, "y": 0.25}, size_hint=(0.25, 0.30), color=(0, 0, 0, 1))
            self.S3_sumary.text = "Check Raw material stock"
            self.root.ids.pagina_principal.add_widget(self.S3_sumary)
        else:
            try:
                try:
                    self.root.ids.pagina_principal.remove_widget(self.S3_sumary)
                    """These are the units you recieved from process 2"""
                    self.units_received_S2=self.units_received-self.units_received*rnd.uniform(0,0.03)
                    """Number of hours need it"""
                    self.total_hours_3=self.units_received/int(self.stage["stage_3"])
                    self.S3_sumary=Label(pos_hint={"x":0.35,"y":0.25},size_hint=(0.25,0.30),color=(0,0,0,1))
                    self.scrap3=int(self.units_received-self.units_received_S2)
                    self.S3_sumary.text=f"Units worked: {int(self.units_received_S2)}\nScrap:{self.scrap3}\nProduction yeild {round((self.units_received_S2/self.units_received) * 100, 2)}% \nTotal hours: {round(self.total_hours_3,2)} hours"
                    self.root.ids.pagina_principal.add_widget(self.S3_sumary)
                    self.Total_hours_list_s3.append(self.total_hours_3)
                    if self.Product_1==1:
                        self.Total_units_p1.append(self.units_received_S2)
                        self.scrap_list_p1.append(self.scrap3)
                    elif self.Product_2==1:
                        self.Total_units_p2.append(self.units_received_S2)
                        self.scrap_list_p2.append(self.scrap3)
                    elif self.Product_3==1:
                        self.Total_units_p3.append(self.units_received_S2)
                        self.scrap_list_p3.append(self.scrap3)
                except:
                    #These are the units you recieved from process 2
                    self.units_received_S2=self.units_received-self.units_received*rnd.uniform(0,0.03)
                    #Number of hours need it
                    self.total_hours_3=self.units_received/int(self.stage["stage_3"])
                    self.S3_sumary=Label(pos_hint={"x":0.35,"y":0.25},size_hint=(0.25,0.30),color=(0,0,0,1))
                    self.scrap3=int(self.units_received-self.units_received_S2)
                    self.S3_sumary.text=f"Units worked: {int(self.units_received_S2)}\nScrap:{self.scrap3}\nProduction yeild {round((self.units_received_S2/self.units_received) * 100, 2)}% \nTotal hours: {round(self.total_hours_3,2)} hours"
                    self.root.ids.pagina_principal.add_widget(self.S3_sumary)
                    self.Total_hours_list_s3.append(self.total_hours_3)
                    if self.Product_1==1:
                        self.Total_units_p1.append(self.units_received_S2)
                        self.scrap_list_p1.append(self.scrap3)
                    elif self.Product_2==1:
                        self.Total_units_p2.append(self.units_received_S2)
                        self.scrap_list_p2.append(self.scrap3)
                    elif self.Product_3==1:
                        self.Total_units_p3.append(self.units_received_S2)
                        self.scrap_list_p3.append(self.scrap3)

            except:
                #Process can't start without proper documentation
                self.S3_sumary = Label(pos_hint={"x": 0.40, "y": 0.25}, size_hint=(0.25, 0.30), color=(0, 0, 0, 1))
                self.S3_sumary.text = "Production order has not been released"
                self.root.ids.pagina_principal.add_widget(self.S3_sumary)


    """This method is going to define total noise of the process"""
    noice_type_list = []
    noice_time_list = []

    def Noice(self):
        """Define stops and types of unplanned stoppages"""
        try:
            self.root.ids.pagina_principal.remove_widget(self.noice_label)
            self.Unplanned_stoppages = {1: "Machine", 2: "Process", 3: "Standards"}
            self.noice_type = self.Unplanned_stoppages[rnd.randrange(1, 4)]
            self.noice_time = round(rnd.uniform(1, 3), 2)
            noice_label = Label(pos_hint={"x": 0.40, "y": 0.30}, size_hint=(0.15, 0.05), color=(0, 0, 0, 1))
            noice_label.text = f'Type of issue: {self.noice_type}\nTime to solve it: {self.noice_time} hours'
            self.root.ids.pagina_principal.add_widget(selfnoice_label)
            """Creating a list to store outcome"""
            self.noice_type_list.append(self.noice_type)
            self.noice_time_list.append(self.noice_time)
        except:
            self.Unplanned_stoppages = {1: "Machine", 2: "Process", 3: "Standards"}
            self.noice_type = self.Unplanned_stoppages[rnd.randrange(1, 4)]
            self.noice_time = round(rnd.uniform(1, 3), 2)
            self.noice_label = Label(pos_hint={"x": 0.40, "y": 0.20}, size_hint=(0.15, 0.05), color=(0, 0, 0, 1))
            self.noice_label.text = f'Type of issue: {self.noice_type}\nTime to solve it: {self.noice_time} hours'
            self.root.ids.pagina_principal.add_widget(self.noice_label)
            """Creating a list to store outcome"""
            self.noice_type_list.append(self.noice_type)
            self.noice_time_list.append(self.noice_time)

    """This is going to make a sumary of the process and tell how much stock you have, Total productive hours and unproductive hours"""
    """Create the lists to store process time"""
    Total_hours_list_s1 = []
    Total_hours_list_s2 = []
    Total_hours_list_s3 = []
    Total_units_p1 = []
    Total_units_p2 = []
    Total_units_p3 = []
    Total_unproductive_hours = []

    def Summary(self):
        try:
            self.root.ids.pagina_principal.remove_widget(self.Totals)
            self.Totals=Label(pos_hint={"x": 0.65, "y": 0.35}, size_hint=(0.30, 0.40), color=(0, 0, 0, 1))
            self.Totals.text = f'Total hours: {round((round(sum(self.Total_hours_list_s1), 2) + round(sum(self.Total_hours_list_s2), 2) + round(sum(self.Total_hours_list_s3), 2) + round(sum(self.noice_time_list), 2)), 2)} hours' \
                               f'\n  Stage 1: {round(sum(self.Total_hours_list_s1), 2)}\n  Stage 2: {round(sum(self.Total_hours_list_s2), 2)}' \
                               f'\n  Stage 3: {round(sum(self.Total_hours_list_s3), 2)}\nUnproductive_hours: {round(sum(self.noice_time_list), 2)}' \
                               f'\nType of stoppage:\n  Machine: {self.noice_type_list.count("Machine")}\n  Process: {self.noice_type_list.count("Process")}\n  Standars: {self.noice_type_list.count("Standards")}' \
                               f'\nUnits on stock\n  Lemon: {int(sum(self.Total_units_p1))}\n  Pineapple: {int(sum(self.Total_units_p2))}\n  Orange: {int(sum(self.Total_units_p3))}' \
                               f'\nTotal scrap\n  Lemon: {int(sum(self.scrap_list_p1))}\n  Pineapple: {int(sum(self.scrap_list_p2))}\n  Orange: {int(sum(self.scrap_list_p3))}'

            self.root.ids.pagina_principal.add_widget(self.Totals)
        except:
            self.Totals = Label(pos_hint={"x": 0.65, "y": 0.35}, size_hint=(0.30, 0.40), color=(0, 0, 0, 1))
            self.Totals.text = f'Total hours: {round((round(sum(self.Total_hours_list_s1), 2) + round(sum(self.Total_hours_list_s2), 2) + round(sum(self.Total_hours_list_s3), 2) + round(sum(self.noice_time_list), 2)),2)} hours' \
                               f'\n  Stage 1: {round(sum(self.Total_hours_list_s1), 2)}\n  Stage 2: {round(sum(self.Total_hours_list_s2), 2)}' \
                               f'\n  Stage 3: {round(sum(self.Total_hours_list_s3), 2)}\nUnproductive_hours: {round(sum(self.noice_time_list), 2)}' \
                               f'\nType of stoppage:\n  Machine: {self.noice_type_list.count("Machine")}\n  Process: {self.noice_type_list.count("Process")}\n  Standars: {self.noice_type_list.count("Standards")}' \
                               f'\nUnits on stock\n  Lemon: {int(sum(self.Total_units_p1))}\n  Pineapple: {int(sum(self.Total_units_p2))}\n  Orange: {int(sum(self.Total_units_p3))}' \
                               f'\nTotal scrap\n  Lemon: {int(sum(self.scrap_list_p1))}\n  Pineapple: {int(sum(self.scrap_list_p2))}\n  Orange: {int(sum(self.scrap_list_p3))}'

            self.root.ids.pagina_principal.add_widget(self.Totals)
    month_list=[]
    def real_demand(self):
        try:
            self.month=1
            print(self.month)
            """Product demand"""
            self.montly_Demand = {"product_1": rnd.randrange(15000, 19000), "product_2": rnd.randrange(20000, 23000),
                             "product_3": rnd.randrange(22000, 24000)}
            self.month_list.append(self.month)
            self.root.ids.pagina_principal.remove_widget(self.request)
            self.request=Label(pos_hint={"x":0.75,"y":0.15},size_hint=(0.1,0.1),color=(0,0,0,1))
            self.total_month = sum(self.month_list) - 1
            self.request.text = f"Month: {self.total_month}\nLemon: {self.montly_Demand['product_1']*self.total_month}\nPineapple: {self.montly_Demand['product_2']*self.total_month}\nOrange: {self.montly_Demand['product_3']*self.total_month}"
            self.root.ids.pagina_principal.add_widget(self.request)

        except:
            """Product demand"""
            self.month = 1
            self.montly_Demand = {"product_1": rnd.randrange(15000, 19000), "product_2": rnd.randrange(20000, 23000),
                             "product_3": rnd.randrange(22000, 24000)}
            self.month_list.append(self.month)
            self.request = Label(pos_hint={"x": 0.75, "y": 0.15}, size_hint=(0.1, 0.1), color=(0, 0, 0, 1))
            self.total_month=sum(self.month_list)-1
            self.request.text = f"Month: {self.total_month}\nLemon: {self.montly_Demand['product_1']*self.total_month}\nPineapple: {self.montly_Demand['product_2']*self.total_month}\nOrange: {self.montly_Demand['product_3']*self.total_month}"
            self.root.ids.pagina_principal.add_widget(self.request)

    """This is where we're going to define projected demand for product 1"""
    def projected_demand_p1(self,args):
        self.Product_1 = 1
        self.Product_2 = 0
        self.Product_3 = 0
        if self.Product_1 == 1:
            self.flavor="Lemon"
            self.RM_containers[self.flavor]
        elif self.Product_2 == 1:
            self.flavor = "Pineapple"
            self.RM_containers[self.flavor]
        elif self.Product_3 == 1:
            self.flavor = "Orange"
            self.RM_containers[self.flavor]
        try:
            try:

                data = self.DF["Product 1"]
                ses = SimpleExpSmoothing(data)
                alpha = 0.25
                model = ses.fit(smoothing_level=alpha, optimized=False)
                self.forcast = model.forecast(1)
                self.forcast=int(self.forcast.iloc[0])
                self.real_forcast=self.forcast
                self.root.ids.pagina_principal.add_widget(self.demand)
                self.demand.text = f"Projected demand \nfor this moth: {self.real_forcast}"
                return self.real_forcast
            except:

                data = self.DF["Product 1"]
                ses = SimpleExpSmoothing(data)
                alpha = 0.25
                model = ses.fit(smoothing_level=alpha, optimized=False)
                self.forcast = model.forecast(1)
                self.forcast = int(self.forcast.iloc[0])
                self.real_forcast = self.forcast
                self.demand.text = f"Projected demand \nfor this moth: {self.real_forcast}"
                return self.real_forcast
        except:
            data = self.DF["Product 1"]
            ses = SimpleExpSmoothing(data)
            alpha = 0.25
            model = ses.fit(smoothing_level=alpha, optimized=False)
            self.forcast = model.forecast(1)
            self.forcast = int(self.forcast.iloc[0])
            self.real_forcast=self.forcast
            return self.real_forcast

    def projected_demand_p2(self,args):
        self.Product_1 = 0
        self.Product_2 = 1
        self.Product_3 = 0
        if self.Product_1 == 1:
            self.flavor="Lemon"
            self.RM_containers[self.flavor]
        elif self.Product_2 == 1:
            self.flavor = "Pineapple"
            self.RM_containers[self.flavor]
        elif self.Product_3 == 1:
            self.flavor = "Orange"
            self.RM_containers[self.flavor]
        try:
            try:
                data2 = self.DF["Product 2"]
                ses = SimpleExpSmoothing(data2)
                alpha = 0.15
                model = ses.fit(smoothing_level=alpha, optimized=False)
                self.forcast2 = model.forecast(1)
                self.forcast2 = int(self.forcast2.iloc[0])
                self.real_forcast = self.forcast2
                self.root.ids.pagina_principal.remove_widget(self.demand)
                self.demand.text = f"Projected demand \nfor this moth: {self.real_forcast}"
                self.root.ids.pagina_principal.add_widget(self.demand)
                return self.real_forcast
            except:
                data2 = self.DF["Product 2"]
                ses = SimpleExpSmoothing(data2)
                alpha = 0.15
                model = ses.fit(smoothing_level=alpha, optimized=False)
                self.forcast2 = model.forecast(1)
                self.forcast2 = int(self.forcast2.iloc[0])
                self.real_forcast = self.forcast2
                self.demand.text = f"Projected demand \nfor this moth: {self.real_forcast}"
                return self.real_forcast
        except:
            data2 = self.DF["Product 2"]
            ses = SimpleExpSmoothing(data2)
            alpha = 0.15
            model = ses.fit(smoothing_level=alpha, optimized=False)
            self.forcast2 = model.forecast(1)
            self.forcast2 = int(self.forcast2.iloc[0])
            self.real_forcast = self.forcast2
            return self.real_forcast

    """This is where we're going to define projected demand for product 3"""
    def projected_demand_p3(self,args):
        self.Product_1 = 0
        self.Product_2 = 0
        self.Product_3 = 1
        if self.Product_1 == 1:
            self.flavor="Lemon"
            self.RM_containers[self.flavor]
        elif self.Product_2 == 1:
            self.flavor = "Pineapple"
            self.RM_containers[self.flavor]
        elif self.Product_3 == 1:
            self.flavor = "Orange"
            self.RM_containers[self.flavor]
        try:
            try:
                data3 = self.DF["Product 3"]
                ses = SimpleExpSmoothing(data3)
                alpha = 0.15
                model = ses.fit(smoothing_level=alpha, optimized=False)
                self.forcast3 = model.forecast(1)
                self.forcast3 = int(self.forcast3.iloc[0])
                self.real_forcast = self.forcast3
                self.root.ids.pagina_principal.remove_widget(self.demand)
                self.root.ids.pagina_principal.add_widget(self.demand)
                self.demand.text = f"Projected demand \nfor this moth: {self.real_forcast}"
                return self.real_forcast
            except:
                data3 = self.DF["Product 3"]
                ses = SimpleExpSmoothing(data3)
                alpha = 0.15
                model = ses.fit(smoothing_level=alpha, optimized=False)
                self.forcast3 = model.forecast(1)
                self.forcast3 = int(self.forcast3.iloc[0])
                self.real_forcast = self.forcast3
                self.demand.text = f"Projected demand \nfor this moth: {self.real_forcast}"
                return self.real_forcast
        except:
            data3 = self.DF["Product 3"]
            ses = SimpleExpSmoothing(data3)
            alpha = 0.15
            model = ses.fit(smoothing_level=alpha, optimized=False)
            self.forcast3 = model.forecast(1)
            self.forcast3 = int(self.forcast3.iloc[0])
            self.real_forcast = self.forcast3
            return self.real_forcast


    def get_demand(self):
        self.Product_1=Button(pos_hint={"x":0.15,"y":0.25},size_hint=(0.15,0.05),text="Lemon \n juice", on_release=self.projected_demand_p1)
        self.Product_2 = Button(pos_hint={"x": 0.15, "y": 0.30}, size_hint=(0.15, 0.05), text="Pineapple \n juice",on_release=self.projected_demand_p2)
        self.Product_3 = Button(pos_hint={"x": 0.15, "y": 0.35}, size_hint=(0.15, 0.05), text="Orange \n juice",on_release=self.projected_demand_p3)
        self.demand=Label(pos_hint={"x":0.15,"y":0.2},size_hint=(0.15,0.05),color=(0,0,0,1))
        self.root.ids.pagina_principal.add_widget(self.Product_1)
        self.root.ids.pagina_principal.add_widget(self.Product_2)
        self.root.ids.pagina_principal.add_widget(self.Product_3)
        self.root.ids.pagina_principal.add_widget(self.demand)

    def build(self):
        return self.kv

if __name__ == "__main__":
    Process().run()
