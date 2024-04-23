from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol.selectioncontrol import MDSwitch

from kivy.core.window import Window

import requests, json

server = 'http://127.0.0.1:8000'

class LoginApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        
        self.screen = Screen()
        
        # Создание вертикального бокс-лейаута
        self.layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
        
        # Надпись "вход"
        label = MDLabel(text="Вход", halign="center", font_style="H5")
        self.layout.add_widget(label)
        
        # Поле Логин
        self.login_field = MDTextField(
            hint_text="Логин",
            helper_text_mode="on_focus",
            mode="rectangle"
        )
        self.layout.add_widget(self.login_field)
        
        # Поле Пароль
        self.password_field = MDTextField(
            hint_text="Пароль",
            helper_text_mode="on_focus",
            mode="rectangle",
            password=True
        )
        self.layout.add_widget(self.password_field)
        
        # Кнопка Вход
        button = MDRaisedButton(text="Вход", size_hint=(1, 0.2))
        button.bind(on_release=self.login_request)
        self.layout.add_widget(button)

        button2 = MDRaisedButton(text="Зарегистрироваться", size_hint=(1, 0.2))
        button2.bind(on_release=self.register)
        self.layout.add_widget(button2)
        
        self.screen.add_widget(self.layout)
        
        return self.screen
    
    def dialog_error_close(self, *args):
        self.dialog.dismiss(force=True)

    def checkErr(self, data):
        try: 
            self.dialog = MDDialog(title=data['error'], buttons=[MDFlatButton(text="ОК", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color,)])
            self.dialog.open()
            return True
        except:
            return False

    def showDialog(self, text):
        self.dialog = MDDialog(title=text, buttons=[MDFlatButton(text="ОК", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color,)])
        self.dialog.open()


    #SETTINGS
    def change_theme(self, instance_switch, theme_switch):
        if theme_switch:
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"
        print(self.theme_cls.theme_style)

    def settingsMenu(self, instance):
        self.theme_switch = MDSwitch()
        self.theme_switch.bind(active=self.change_theme)
        self.dialog = MDDialog(
            title="Настройки",
            type='custom',
            buttons=[
                MDFlatButton(text="Закрыть", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color)
            ],
            content_cls=MDBoxLayout(
                orientation="vertical",
                size_hint_y=None,
                spacing="12dp"
            )
        )
        self.dialog.content_cls.add_widget(MDLabel(text="Светлая тема", halign="left", font_style="H6"))
        self.dialog.content_cls.add_widget(self.theme_switch)
        self.dialog.open()
    


    #ABOUT
    def getAbout(self, instance):
        response = requests.post(f"{server}/getAbout")
        error = self.checkErr(response.json())
        if error: return 0
        self.dialog = MDDialog(title='Справка', text=response.json()['about'], buttons=[MDFlatButton(text="ОК", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color,)])
        self.dialog.open()
    #CONTACTS
    def getContacts(self, instance):
        response = requests.post(f"{server}/getContacts")
        error = self.checkErr(response.json())
        if error: return 0
        self.dialog = MDDialog(title='Контакты', text=response.json()['contacts'], buttons=[MDFlatButton(text="ОК", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color,)])
        self.dialog.open()


    #PORTFOLIO
    def getPortfolio(self):
        data=self.data
        response = requests.post(f"{server}/getPortfolio", params=self.data)
        error = self.checkErr(response.json())
        if error: return 0

        return response.json()['portfolio']

    def changePortfolio(self):
        self.dialog_error_close()
        data=self.data
        data['portfolio']=self.comment_field.text
        response = requests.post(f"{server}/changePortfolio", params=self.data)
        error = self.checkErr(response.json())
        if error: return 0
        self.showDialog('Сохранено')

    def showPortfolio(self, instance):
        self.comment_field = MDTextField(hint_text="Ваше резюме", text=self.getPortfolio(), multiline=True)
        self.dialog = MDDialog(title='Резюме', type='custom',
            buttons=[
                MDFlatButton(text="Отмена",
                         on_release=lambda x: self.dialog_error_close(),
                         theme_text_color="Custom",
                         text_color=self.theme_cls.primary_color),
                MDFlatButton(text="Сохранить",
                             on_release=lambda x: self.changePortfolio(),
                             theme_text_color="Custom",
                             text_color=self.theme_cls.primary_color)
            ],
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="200dp",
            )
        )
        self.dialog.content_cls.add_widget(self.comment_field)
        self.dialog.open()

    #CASTING
    def ticketCasting(self, casting):
        self.dialog_error_close()

        data=self.data
        data['casting']=str(casting)

        response = requests.post(f"{server}/ticketCasting", params=data)
        casting=response.json()

        error = self.checkErr(casting)
        if error: return 0

        self.showDialog('Заявка подана')

    def viewCasting(self, instance):
        castingid=instance.secondary_text
        data=self.data
        data['casting']=str(castingid)

        response = requests.post(f"{server}/getCasting", params=data)
        casting=response.json()

        error = self.checkErr(casting)
        if error: return 0

        text=f"""\
    {casting['title']}

{casting['text']}
"""
        if str(self.mainMenu.__name__)=='openUserMenu':
            buttons=[
                        MDFlatButton(text="Отмена", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                        MDFlatButton(text="Подать заявку", on_release=lambda x: self.ticketCasting(casting['id']), theme_text_color="Custom", text_color=self.theme_cls.primary_color)
                    ]
        else:
            print(str(self.mainMenu))
            buttons=[
                        MDFlatButton(text="Отмена", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    ]
        self.dialog = MDDialog(
            title=text,
                buttons=buttons
            )
        self.dialog.open()

    def previewCasting(self, instance):
        castingid=instance.secondary_text
        data=self.data
        data['casting']=str(castingid)

        response = requests.post(f"{server}/getCasting", params=data)
        casting=response.json()

        error = self.checkErr(casting)
        if error: return 0

        text=f"""\
    {casting['title']}

{casting['text']}
"""
        self.dialog = MDDialog(
            title=text,
                buttons=[
                    MDFlatButton(text="Закрыть", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                ]
            )
        self.dialog.open()

    def updatefilters(self, instance):
        self.filters=self.search_field.text
        self.openCastingsMenu(instance)

    def openCastingsMenu(self, *args):
        try:
            self.screen.clear_widgets()
        except Exception as ex:
            print(ex)
            
        data = self.data
        data['filters'] = self.filters
        response = requests.post(f"{server}/getOpenCastings", params=data)
        castings = response.json()
        self.layout.clear_widgets()
        
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
    
        label = MDLabel(text="Открытые кастинги", halign="center", font_style="H5", size_hint_y=1.8)
        self.screen.add_widget(label)
    
        self.search_field = MDTextField(hint_text="Введите запрос", size_hint=(1, None), height=50, text=self.filters)
        user_layout.add_widget(self.search_field)
        search_button = MDRaisedButton(text="Искать", size_hint=(None, None), width=100, height=50, on_release=self.updatefilters)
        user_layout.add_widget(search_button)
        
        
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.casting_list = MDList()
        
        for casting in castings:
            text = f"{casting['title']}"
            self.casting_list.add_widget(OneLineListItem(text=text, on_release=self.viewCasting, secondary_text=str(casting['id'])))
        
        
        scroll_view.add_widget(self.casting_list)
        user_layout.add_widget(scroll_view)
    
        reload_button = MDFloatingActionButton(icon="refresh", type="standard", on_release=self.openCastingsMenu)
        back_button = MDFloatingActionButton(icon="arrow-left", type="standard", on_release=self.mainMenu)
        ###user_layout.add_widget(reload_button)
        user_layout.add_widget(back_button)
        
        self.screen.add_widget(user_layout)


    def openMyTicketsMenu(self, *args):
        try: self.screen.clear_widgets()
        except Exception as ex: print(ex)
            
        data = self.data
        response = requests.post(f"{server}/getMyTickets", params=data)
        castings = response.json()
        self.layout.clear_widgets()
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
        label = MDLabel(text="Мои заявки", halign="center", font_style="H5", size_hint_y=1.8)
        self.screen.add_widget(label)
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.casting_list = MDList()
        status = {0: 'На рассмотрении - ', 1: 'Принято - ', 2: 'Отклонено - '}
        for casting in castings:
            text = f'{status[int(casting["ticket_status"])]} {casting["title"]}'
            self.casting_list.add_widget(OneLineListItem(text=text, on_release=self.previewCasting, secondary_text=str(casting["id"])))

        scroll_view.add_widget(self.casting_list)
        user_layout.add_widget(scroll_view)
        reload_button = MDFloatingActionButton(icon="refresh", type="standard", on_release=self.openCastingsMenu)
        back_button = MDFloatingActionButton(icon="arrow-left", type="standard", on_release=self.mainMenu)
        ###user_layout.add_widget(reload_button)
        user_layout.add_widget(back_button)
    
        self.screen.add_widget(user_layout)

    #INVITES
    def acceptInvite(self, invite):
        self.dialog_error_close()

        data=self.data
        data['invite']=str(invite)

        response = requests.post(f"{server}/acceptInvite", params=data)
        invite=response.json()

        error = self.checkErr(invite)
        if error: return 0

        self.showDialog('Приглашение принято')
        
    def rejectInvite(self, invite):
        self.dialog_error_close()

        data=self.data
        data['invite']=str(invite)

        response = requests.post(f"{server}/rejectInvite", params=data)
        invite=response.json()

        error = self.checkErr(invite)
        if error: return 0

        self.showDialog('Приглашение удалено')

    def viewInvite(self, instance):
        castingid=instance.secondary_text.split(':')[0]
        data=self.data
        data['casting']=str(castingid)
        data['invite']=str(instance.secondary_text.split(':')[1])

        print(data)
        response = requests.post(f"{server}/getCastingInvite", params=data)
        casting=response.json()
        print(casting)

        error = self.checkErr(casting)
        if error: return 0

        text=f"""\
    {casting['title']}

{casting['comment']}

{casting['text']}
"""
        self.dialog = MDDialog(
            title=text,
                buttons=[
                    MDFlatButton(text="Отмена", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Отклонить", on_release=lambda x: self.rejectInvite(instance.secondary_text.split(':')[1]), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Принять", on_release=lambda x: self.acceptInvite(instance.secondary_text.split(':')[1]), theme_text_color="Custom", text_color=self.theme_cls.primary_color)
                ]
            )
        self.dialog.open()

    def invitesMenu(self, *args):
        try:self.screen.clear_widgets()
        except Exception as ex:print(ex)

        data = self.data
        response = requests.post(f"{server}/getMyInvites", params=data)
        castings = response.json()
        self.layout.clear_widgets()
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
        label = MDLabel(text="Приглашения", halign="center", font_style="H5", size_hint_y=1.8)
        self.screen.add_widget(label)
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.casting_list = MDList()
    
        for casting in castings:
            text = f'{casting["title"]}'
            self.casting_list.add_widget(OneLineListItem(text=text, on_release=self.viewInvite, secondary_text=f'{casting["casting_id"]}:{casting["id"]}'))
    
        scroll_view.add_widget(self.casting_list)
        user_layout.add_widget(scroll_view)
        reload_button = MDFloatingActionButton(icon="refresh", type="standard", on_release=self.openCastingsMenu)
        back_button = MDFloatingActionButton(icon="arrow-left", type="standard", on_release=self.mainMenu)
        ###user_layout.add_widget(reload_button)
        user_layout.add_widget(back_button)
        self.screen.add_widget(user_layout)

    #USER MENU
    def openUserMenu(self, *args):
        try:self.screen.clear_widgets()
        except Exception as ex:print(ex)

        # Создание вертикального бокс-лейаута
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)

        # Надпись "Меню актера"
        label = MDLabel(text="Меню актера", halign="center", font_style="H5")
        user_layout.add_widget(label)

        # Кнопка Профиль
        profile_button = MDRaisedButton(text="Резюме", size_hint=(1, None), height="48dp", on_release=self.showPortfolio)
        user_layout.add_widget(profile_button)

        # Кнопка Заявки
        applications_button = MDRaisedButton(text="Заявки", size_hint=(1, None), height="48dp", on_release=self.openMyTicketsMenu)
        user_layout.add_widget(applications_button)

        # Кнопка Приглашения
        invitations_button = MDRaisedButton(text="Приглашения", size_hint=(1, None), height="48dp", on_release=self.invitesMenu)
        user_layout.add_widget(invitations_button)

        # Кнопка Кастинги
        castings_button = MDRaisedButton(text="Кастинги", size_hint=(1, None), height="48dp", on_release=self.openCastingsMenu)
        user_layout.add_widget(castings_button)

        # Кнопка Настройки
        settings_button = MDRaisedButton(text="Настройки", size_hint=(1, None), height="48dp", on_release=self.settingsMenu)
        user_layout.add_widget(settings_button)

        # Кнопка Контакты
        contacts_button = MDRaisedButton(text="Контакты", size_hint=(1, None), height="48dp", on_release=self.getContacts)
        user_layout.add_widget(contacts_button)

        # Кнопка Справка
        help_button = MDRaisedButton(text="Справка", size_hint=(1, None), height="48dp", on_release=self.getAbout)
        user_layout.add_widget(help_button)

        self.screen.add_widget(user_layout)

    #GET CLIENTS
    def reviews(self, client):
        data = self.data
        data['client']=str(client)
        response = requests.post(f"{server}/getReviews", params=data)
        clients = response.json()
        error = self.checkErr(clients)
        if error: return 0
        text=''
        for line in clients:
            text+=f'{line['text']}\n________________________\n\n'
        reviewslist=requests.post
        scrollview = ScrollView(size_hint_y=None, height="400dp")
        label = MDLabel(text=text, size_hint_y=None, font_size=20, halign="left")
        label.bind(width=lambda instance, value: setattr(label, 'text_size', (value, None)))
        label.bind(texture_size=label.setter('size'))
        scrollview.add_widget(label)
    
        self.dialog = MDDialog(title="Отзывы", type="custom", content_cls=scrollview,
                           buttons=[MDFlatButton(text="ОК", on_release=lambda x: self.dialog_error_close(),
                                                 theme_text_color="Custom", text_color=self.theme_cls.primary_color,)])
        self.dialog.open()

    def addReview(self, client):
        self.dialog_error_close()
        comment=self.comment_field.text

        data=self.data
        data['client']=str(client)
        data['text']=str(comment)

        response = requests.post(f"{server}/addReview", params=data)
        review=response.json()

        error = self.checkErr(review)
        if error: return 0

        self.showDialog('Отзыв оставлен')

    def addReviewMenu(self, client):
        self.dialog_error_close()
        self.comment_field = MDTextField(hint_text="Отзыв", text=self.getPortfolio(), multiline=True)
        self.dialog = MDDialog(title='Оставить отзыв', type='custom',
            buttons=[
                MDFlatButton(text="Отмена",
                         on_release=lambda x: self.dialog_error_close(),
                         theme_text_color="Custom",
                         text_color=self.theme_cls.primary_color),
                MDFlatButton(text="Сохранить",
                             on_release=lambda x: self.addReview(client),
                             theme_text_color="Custom",
                             text_color=self.theme_cls.primary_color)
            ],
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="200dp",
            )
        )
        self.dialog.content_cls.add_widget(self.comment_field)
        self.dialog.open()

    def viewClient(self, client):
        data=self.data
        if str(type(client))=="<class 'str'>":
            data['client']=client
        else:
            data['client']=str(client.secondary_text)

        response = requests.post(f"{server}/getUser", params=data)
        user=response.json()

        error = self.checkErr(user)
        if error: return 0

        text=f"""\
{user['login']}

Резюме:
{user['portfolio']}
"""
        self.dialog = MDDialog(
            title=text,
                buttons=[
                    MDFlatButton(text="Отмена", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Отзывы", on_release=lambda x: self.reviews(user['id']), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Оставить отзыв", on_release=lambda x: self.addReviewMenu(user['id']), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                ]
            )
        self.dialog.open()

    def getClientsMenu(self, *args):
        try:self.screen.clear_widgets()
        except Exception as ex:print(ex)

        data = self.data
        response = requests.post(f"{server}/getClients", params=data)
        clients = response.json()
        self.layout.clear_widgets()
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
        label = MDLabel(text="Клиенты", halign="center", font_style="H5", size_hint_y=1.8)
        self.screen.add_widget(label)
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.client_list = MDList()
    
        for client in clients:
            text = f'{client["login"]}'
            self.client_list.add_widget(OneLineListItem(text=text, on_release=self.viewClient, secondary_text=f'{client["id"]}'))
    
        scroll_view.add_widget(self.client_list)
        user_layout.add_widget(scroll_view)
        reload_button = MDFloatingActionButton(icon="refresh", type="standard", on_release=self.openCastingsMenu)
        back_button = MDFloatingActionButton(icon="arrow-left", type="standard", on_release=self.mainMenu)
        ###user_layout.add_widget(reload_button)
        user_layout.add_widget(back_button)
        self.screen.add_widget(user_layout)

    #TICKETS MENU
    def acceptTicket(self, casting):
        self.dialog_error_close()
        data=self.data
        data['casting']=str(casting)
        response = requests.post(f"{server}/acceptTicket", params=data)
        review=response.json()
        error = self.checkErr(review)
        if error: return 0
        self.showDialog('Принято')

    def rejectTicket(self, casting):
        self.dialog_error_close()
        data=self.data
        data['casting']=str(casting)
        response = requests.post(f"{server}/rejectTicket", params=data)
        review=response.json()
        error = self.checkErr(review)
        if error: return 0
        self.showDialog('Отклонено')

    def viewTicket(self, instance):
        castingid=instance.secondary_text.split(':')[0]
        data=self.data
        data['casting']=str(castingid)

        response = requests.post(f"{server}/getCasting", params=data)
        casting=response.json()

        error = self.checkErr(casting)
        if error: return 0

        text=f"""\
    {casting['title']}

{casting['text']}
"""
        self.dialog = MDDialog(
            title=text,
                buttons=[
                    MDFlatButton(text="Закрыть", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Принять", on_release=lambda x: self.acceptTicket(instance.secondary_text.split(':')[1]), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Отклонить", on_release=lambda x: self.rejectTicket(instance.secondary_text.split(':')[1]), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Профиль", on_release=lambda x: self.viewClient(instance.secondary_text.split(':')[2]), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                ]
            )
        self.dialog.open()

    def openTicketsMenu(self, *args):
        try: self.screen.clear_widgets()
        except Exception as ex: print(ex)
            
        data = self.data
        response = requests.post(f"{server}/getTickets", params=data)
        castings = response.json()
        self.layout.clear_widgets()
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
        label = MDLabel(text="Заявки", halign="center", font_style="H5", size_hint_y=1.8)
        self.screen.add_widget(label)
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.casting_list = MDList()
        status = {0: 'На рассмотрении - ', 1: 'Принято - ', 2: 'Отклонено - '}
        for casting in castings:
            text = f'{status[int(casting["ticket_status"])]} {casting["title"]}'
            self.casting_list.add_widget(OneLineListItem(text=text, on_release=self.viewTicket, secondary_text=f'{casting["id"]}:{casting['ticket_id']}:{casting['user']}'))

        scroll_view.add_widget(self.casting_list)
        user_layout.add_widget(scroll_view)
        reload_button = MDFloatingActionButton(icon="refresh", type="standard", on_release=self.openCastingsMenu)
        back_button = MDFloatingActionButton(icon="arrow-left", type="standard", on_release=self.mainMenu)
        ###user_layout.add_widget(reload_button)
        user_layout.add_widget(back_button)
    
        self.screen.add_widget(user_layout)


    #CASTINGS-ADMIN
    def changeCasting(self, casting):
        self.dialog_error_close()
        data=self.data
        data['casting']=str(casting)
        data['title']=str(self.comment_field1.text)
        data['text']=str(self.comment_field2.text)
        response = requests.post(f"{server}/changeCasting", params=data)
        review=response.json()
        error = self.checkErr(review)
        if error: return 0
        self.showDialog('Изменено')

    def editCasting(self, casting, title, text):
        self.dialog_error_close()
        self.comment_field1 = MDTextField(hint_text="Заголовок", text=title)
        self.comment_field2 = MDTextField(hint_text="Текст", multiline=True, text=text)
        self.dialog = MDDialog(title='Создать заявку', type='custom',
            buttons=[
                MDFlatButton(text="Отмена",
                         on_release=lambda x: self.dialog_error_close(),
                         theme_text_color="Custom",
                         text_color=self.theme_cls.primary_color),
                MDFlatButton(text="Изменить",
                             on_release=lambda x: self.changeCasting(casting),
                             theme_text_color="Custom",
                             text_color=self.theme_cls.primary_color)
            ],
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="200dp",
            )
        )
        self.dialog.content_cls.add_widget(self.comment_field1)
        self.dialog.content_cls.add_widget(self.comment_field2)
        self.dialog.open()

    def addCasting(self):
        self.dialog_error_close()
        data=self.data
        data['title']=str(self.comment_field1.text)
        data['text']=str(self.comment_field2.text)
        response = requests.post(f"{server}/addCasting", params=data)
        review=response.json()
        error = self.checkErr(review)
        if error: return 0
        self.showDialog('Создано')

    def createCasting(self, instance):
        self.comment_field1 = MDTextField(hint_text="Заголовок")
        self.comment_field2 = MDTextField(hint_text="Текст", multiline=True)
        self.dialog = MDDialog(title='Создать заявку', type='custom',
            buttons=[
                MDFlatButton(text="Отмена",
                         on_release=lambda x: self.dialog_error_close(),
                         theme_text_color="Custom",
                         text_color=self.theme_cls.primary_color),
                MDFlatButton(text="Cоздать",
                             on_release=lambda x: self.addCasting(),
                             theme_text_color="Custom",
                             text_color=self.theme_cls.primary_color)
            ],
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="200dp",
            )
        )
        self.dialog.content_cls.add_widget(self.comment_field1)
        self.dialog.content_cls.add_widget(self.comment_field2)
        self.dialog.open()

    def deleteCasting(self, casting):
        self.dialog_error_close()
        data=self.data
        data['casting']=str(casting)
        response = requests.post(f"{server}/deleteCasting", params=data)
        review=response.json()
        error = self.checkErr(review)
        if error: return 0
        self.showDialog('Удалено')

    def viewCastingD(self, instance):
        castingid=instance.secondary_text
        data=self.data
        data['casting']=str(castingid)

        response = requests.post(f"{server}/getCasting", params=data)
        casting=response.json()

        error = self.checkErr(casting)
        if error: return 0

        text=f"""\
    {casting['title']}

{casting['text']}
"""
        buttons=[
                    MDFlatButton(text="Отмена", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Завершить", on_release=lambda x: self.deleteCasting(casting['id']), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Редактировать", on_release=lambda x: self.editCasting(casting['id'], casting['title'], casting['text']), theme_text_color="Custom", text_color=self.theme_cls.primary_color)
                ]
        self.dialog = MDDialog(
            title=text,
                buttons=buttons
            )
        self.dialog.open()

    def openCastingsMenuD(self, *args):
        try:
            self.screen.clear_widgets()
        except Exception as ex:
            print(ex)
            
        data = self.data
        data['filters'] = self.filtersс
        response = requests.post(f"{server}/getMyCastings", params=data)
        castings = response.json()
        self.layout.clear_widgets()
        
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
    
        label = MDLabel(text="Кастинги", halign="center", font_style="H5", size_hint_y=1.8)
        self.screen.add_widget(label)
        
        # Добавляем кнопки фильтрации
        filter_buttons = MDBoxLayout(spacing=10, size_hint_y=None, height=50)
        
        # Функция для обновления фильтра и перезагрузки меню
        def update_and_reload(filter_value):
            self.filtersс = filter_value
            self.openCastingsMenuD()
            
        create_button = MDRaisedButton(text="Создать кастинг", on_release=self.createCasting, size_hint=(1, None), height=self.layout.height * 0.2)
        user_layout.add_widget(create_button)

        all_button = MDRaisedButton(text="Все", on_release=lambda x: update_and_reload(3))
        active_button = MDRaisedButton(text="Активные", on_release=lambda x: update_and_reload(0))
        inactive_button = MDRaisedButton(text="Неактивные", on_release=lambda x: update_and_reload(1))
        
        filter_buttons.add_widget(all_button)
        filter_buttons.add_widget(active_button)
        filter_buttons.add_widget(inactive_button)
        
        user_layout.add_widget(filter_buttons)
        
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.casting_list = MDList()
        
        for casting in castings:
            text = f"{casting['title']}"
            self.casting_list.add_widget(OneLineListItem(text=text, on_release=self.viewCastingD, secondary_text=str(casting['id'])))
        
        scroll_view.add_widget(self.casting_list)
        user_layout.add_widget(scroll_view)
    
        back_button = MDFloatingActionButton(icon="arrow-left", type="standard", on_release=self.mainMenu)
        user_layout.add_widget(back_button)
        
        self.screen.add_widget(user_layout)

    #AGENT MENU
    def openAgentMenu(self, *args):
        try:self.screen.clear_widgets()
        except Exception as ex:print(ex)
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)

        # Надпись
        label = MDLabel(text="Меню агента", halign="center", font_style="H5")
        user_layout.add_widget(label)

        # Кнопка 
        profile_button = MDRaisedButton(text="Резюме", size_hint=(1, None), height="48dp", on_release=self.showPortfolio)
        user_layout.add_widget(profile_button)

        # Кнопка 
        applications_button = MDRaisedButton(text="Актёры", size_hint=(1, None), height="48dp", on_release=self.openActersMenu)
        user_layout.add_widget(applications_button)

        # Кнопка 
        invitations_button = MDRaisedButton(text="Приглашения", size_hint=(1, None), height="48dp", on_release=self.SentInvitesMenu)
        user_layout.add_widget(invitations_button)

        # Кнопка 
        castings_button = MDRaisedButton(text="Кастинги", size_hint=(1, None), height="48dp", on_release=self.openCastingsMenu)
        user_layout.add_widget(castings_button)

        # Кнопка 
        clients_button = MDRaisedButton(text="Клиенты", size_hint=(1, None), height="48dp", on_release=self.getClientsMenu)
        user_layout.add_widget(clients_button)

        # Кнопка Настройки
        settings_button = MDRaisedButton(text="Настройки", size_hint=(1, None), height="48dp", on_release=self.settingsMenu)
        user_layout.add_widget(settings_button)

        # Кнопка Контакты
        contacts_button = MDRaisedButton(text="Контакты", size_hint=(1, None), height="48dp", on_release=self.getContacts)
        user_layout.add_widget(contacts_button)

        # Кнопка Справка
        help_button = MDRaisedButton(text="Справка", size_hint=(1, None), height="48dp", on_release=self.getAbout)
        user_layout.add_widget(help_button)

        self.screen.add_widget(user_layout)

    #INVITE ACTER
    def inviteActerInCasting(self, casting):
        self.dialog_error_close()

        data=self.data
        data['actor']=str(self.selectedActer)
        data['casting']=str(casting.secondary_text)
        data['comment']=str(self.comment_field.text)

        response = requests.post(f"{server}/inviteActor", params=data)
        invite=response.json()

        error = self.checkErr(invite)
        if error: return 0
        self.showDialog('Актер приглашен')
        self.mainMenu()

    def updatefiltersInviteActerMenu(self, instance):
        self.filters=self.search_field.text
        self.openInviteActerMenu()

    def openInviteActerMenu(self):
        try: self.screen.clear_widgets()
        except Exception as ex: print(ex)
            
        data = self.data
        data['filters'] = self.filters
        response = requests.post(f"{server}/getAllCastings", params=data)
        castings = response.json()
        self.layout.clear_widgets()
        
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
    
        label = MDLabel(text="Выберите кастинг", halign="center", font_style="H5", size_hint_y=1.8)
        self.screen.add_widget(label)
    
        self.search_field = MDTextField(hint_text="Введите запрос", size_hint=(1, None), height=50, text=self.filters)
        user_layout.add_widget(self.search_field)
        search_button = MDRaisedButton(text="Искать", size_hint=(None, None), width=100, height=50, on_release=self.updatefiltersInviteActerMenu)
        user_layout.add_widget(search_button)
        
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.casting_list = MDList()
        
        for casting in castings:
            text = f"{casting['title']}"
            self.casting_list.add_widget(OneLineListItem(text=text, on_release=self.inviteActerInCasting, secondary_text=str(casting['id'])))
        
        scroll_view.add_widget(self.casting_list)
        user_layout.add_widget(scroll_view)
        reload_button = MDFloatingActionButton(icon="refresh", type="standard", on_release=self.openCastingsMenu)
        back_button = MDFloatingActionButton(icon="arrow-left", type="standard", on_release=self.mainMenu)
        ###user_layout.add_widget(reload_button)
        user_layout.add_widget(back_button)
        
        self.screen.add_widget(user_layout)

    def inviteActer(self, acter):
        self.selectedActer=acter
        self.dialog_error_close()
        self.openInviteActerMenu()

    def viewInvite(self, instance):
        castingid=instance.secondary_text.split(':')[0]
        data=self.data
        data['casting']=str(castingid)
        data['invite']=str(instance.secondary_text.split(':')[1])

        print(data)
        response = requests.post(f"{server}/getCastingInvite", params=data)
        casting=response.json()
        print(casting)

        error = self.checkErr(casting)
        if error: return 0

        text=f"""\
Кастинг: {casting['title']}

Комментарий:{casting['comment']}

Получатель:{casting['comment']}

{casting['text']}
"""
        self.dialog = MDDialog(
            title=text,
                buttons=[
                    MDFlatButton(text="Отмена", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Отменить приглашение", on_release=lambda x: self.rejectInvite(instance.secondary_text.split(':')[1]), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                ]
            )
        self.dialog.open()

    def SentInvitesMenu(self, *args):
        try:self.screen.clear_widgets()
        except Exception as ex:print(ex)

        data = self.data
        response = requests.post(f"{server}/getSentInvites", params=data)
        invites = response.json()
        self.layout.clear_widgets()
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
        label = MDLabel(text="Отправленные приглашения", halign="center", font_style="H5", size_hint_y=1.8)
        self.screen.add_widget(label)
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.casting_list = MDList()
    
        for invite in invites:
            text = f'{invite["login"]} | {invite["title"]}'
            self.casting_list.add_widget(OneLineListItem(text=text, on_release=self.viewInvite, secondary_text=f'{invite["casting_id"]}:{invite["id"]}'))
    
        scroll_view.add_widget(self.casting_list)
        user_layout.add_widget(scroll_view)
        reload_button = MDFloatingActionButton(icon="refresh", type="standard", on_release=self.openCastingsMenu)
        back_button = MDFloatingActionButton(icon="arrow-left", type="standard", on_release=self.mainMenu)
        ###user_layout.add_widget(reload_button)
        user_layout.add_widget(back_button)
        self.screen.add_widget(user_layout)

    #VIEW ACTERS
    def viewActer(self, instance):
        acterid=instance.secondary_text
        data=self.data
        data['acter']=str(acterid)

        response = requests.post(f"{server}/getActer", params=data)
        acter=response.json()

        error = self.checkErr(acter)
        if error: return 0

        text=f"""\
   {acter['login']}

{acter['portfolio']}
"""
        self.comment_field = MDTextField(hint_text="Комментарий к приглашению")
        self.dialog = MDDialog(
            title=text,
                buttons=[
                    MDFlatButton(text="Закрыть", on_release=lambda x: self.dialog_error_close(), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                    MDFlatButton(text="Пригласить", on_release=lambda x: self.inviteActer(acter['id']), theme_text_color="Custom", text_color=self.theme_cls.primary_color),
                ],
                type='custom',
                content_cls=MDBoxLayout(
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="200dp",
                )
            )
        self.dialog.content_cls.add_widget(self.comment_field)
        self.dialog.open()

    def updateFiltersActersMenu(self, instance):
        self.filters=self.search_field.text
        self.openActersMenu(instance)

    def openActersMenu(self, *args):
        try:
            self.screen.clear_widgets()
        except Exception as ex:
            print(ex)
            
        data = self.data
        data['filters'] = self.filters
        response = requests.post(f"{server}/getActers", params=data)
        acters = response.json()
        self.layout.clear_widgets()
        
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)
    
        label = MDLabel(text="Актёры", halign="center", font_style="H5", size_hint_y=1.8)
        self.screen.add_widget(label)
    
        self.search_field = MDTextField(hint_text="Введите запрос", size_hint=(1, None), height=50, text=self.filters)
        user_layout.add_widget(self.search_field)
        search_button = MDRaisedButton(text="Искать", size_hint=(None, None), width=100, height=50, on_release=self.updateFiltersActersMenu)
        user_layout.add_widget(search_button)
        
        
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.casting_list = MDList()
        
        for acter in acters:
            text = f"{acter['login']}"
            self.casting_list.add_widget(OneLineListItem(text=text, on_release=self.viewActer, secondary_text=str(acter['id'])))
        
        
        scroll_view.add_widget(self.casting_list)
        user_layout.add_widget(scroll_view)
    
        reload_button = MDFloatingActionButton(icon="refresh", type="standard", on_release=self.openCastingsMenu)
        back_button = MDFloatingActionButton(icon="arrow-left", type="standard", on_release=self.mainMenu)
        ###user_layout.add_widget(reload_button)
        user_layout.add_widget(back_button)
        
        self.screen.add_widget(user_layout)

    #CASTING-D MENU
    def openCastingDMenu(self, *args):
        self.filtersс=3

        try:self.screen.clear_widgets()
        except Exception as ex:print(ex)

        # Создание вертикального бокс-лейаута
        user_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=30)

        # Надпись "Меню актера"
        label = MDLabel(text="Меню кастинг-директора", halign="center", font_style="H5")
        user_layout.add_widget(label)

        # Кнопка Профиль
        profile_button = MDRaisedButton(text="Резюме", size_hint=(1, None), height="48dp", on_release=self.showPortfolio)
        user_layout.add_widget(profile_button)

        # Кнопка Заявки
        applications_button = MDRaisedButton(text="Мои кастинги", size_hint=(1, None), height="48dp", on_release=self.openCastingsMenuD)
        user_layout.add_widget(applications_button)

        # Кнопка Приглашения
        invitations_button2 = MDRaisedButton(text="Заявки на кастинги", size_hint=(1, None), height="48dp", on_release=self.openTicketsMenu)
        user_layout.add_widget(invitations_button2)

        # Кнопка Кастинги
        castings_button = MDRaisedButton(text="Актёры", size_hint=(1, None), height="48dp", on_release=self.openActersMenu)
        user_layout.add_widget(castings_button)

        # Кнопка Кастинги
        invitations_button = MDRaisedButton(text="Приглашения", size_hint=(1, None), height="48dp", on_release=self.SentInvitesMenu)
        user_layout.add_widget(invitations_button)

        # Кнопка Настройки
        settings_button = MDRaisedButton(text="Настройки", size_hint=(1, None), height="48dp", on_release=self.settingsMenu)
        user_layout.add_widget(settings_button)

        # Кнопка Контакты
        contacts_button = MDRaisedButton(text="Контакты", size_hint=(1, None), height="48dp", on_release=self.getContacts)
        user_layout.add_widget(contacts_button)

        # Кнопка Справка
        help_button = MDRaisedButton(text="Справка", size_hint=(1, None), height="48dp", on_release=self.getAbout)
        user_layout.add_widget(help_button)

        self.screen.add_widget(user_layout)

    def login_request(self, instance):
        self.filters=''
        self.selectedActer=None
        self.login = str(self.login_field.text)
        self.password = str(self.password_field.text)
        
        self.data = {
            "login": self.login,
            "password": self.password,
        }
        
        response = requests.post(f"{server}/login", params=self.data)
        
        if response.status_code == 200:
            error = self.checkErr(response.json())
            if error: return 0
            role = response.json()['role']
            if role == 0:
                self.mainMenu=self.openUserMenu
            elif role == 1:
                self.mainMenu=self.openAgentMenu
            elif role == 2:
                self.mainMenu=self.openCastingDMenu
            self.mainMenu()

    def register(self, instance):
        self.login = str(self.login_field.text)
        self.password = str(self.password_field.text)
        
        self.data = {
            "login": self.login,
            "password": self.password,
        }
        
        response = requests.post(f"{server}/register", params=self.data)
        
        if response.status_code == 200:
            error = self.checkErr(response.json())
            if error: return 0
            self.login_request(instance)

if __name__ == '__main__':
    LoginApp().run()
