import flet as ft

from components import Message, ChatMessage
from n8n import get_ai_response

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Flet IA com n8n"
    page.window.width = 420
    page.window.height = 740
    page.window.resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()
    
    
    ### Comandos/Ações
    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Nome é obrigatório!"
            join_user_name.update()
        else:
            page.session.set('user_name', join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            #new_message.update()
            page.update()

    
    def add_message_on_history(message: Message):
        m = ChatMessage(message)
        chat.controls.append(m)
        page.update()

    
    async def send_message_click(e):
        if new_message.value != "":
            user_message = new_message.value
           
            add_message_on_history(
               Message(
                    user_name=page.session.get('user_name'),
                    text=user_message,
                    user_type="user"
                )
            )
           
            new_message.value = ""
            page.update()

            ai_response = await get_ai_response(user_message, page)

            add_message_on_history(
               Message(
                    user_name='IA',
                    text=ai_response,
                    user_type="ia"
                )
            )

            new_message.focus()
            page.update()


    join_user_name = ft.TextField(
        label='Informe seu nome',
        autofocus=True,
        on_submit=join_chat_click,
    )


    app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.ASSISTANT),
        leading_width=40,
        title=ft.Text("Flet IA com n8n"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE,
    )

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Bem-vindo(a)", size=20, color=ft.Colors.WHITE),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text='Começar', on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="No que posso ajudar ?",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=3,
        filled=True,
        bgcolor="#273c75",
        border_radius=10,
        color="#FFFFFF",
        border_color="#273c75",
        # focused_border_color="#FFFFFF",
        on_submit=send_message_click,
    )

    container = ft.Container(
        width=page.window.width,
        height=page.window.height,
        expand=True,
        bgcolor="#192a56",
        border_radius=30,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Container(
                    content=
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.Text('PyFlet IA com n8n', size=24, color=ft.Colors.WHITE),
                            ],
                        ),
                    border_radius=5,
                    height=40,
                    margin=ft.margin.only(left=20, top=10, right=20, bottom=0),
                ),
                ft.Container(
                    content=chat,
                    border_radius=10,
                    padding=ft.padding.all(10),
                    expand=True,
                    margin=ft.margin.only(left=20, top=5, right=20, bottom=0),
                    bgcolor="#273c75",
                ),
                ft.Container(
                    margin=ft.margin.only(left=20, top=5, right=20, bottom=20),
                    content=ft.Row(
                        controls=[
                            new_message,
                            ft.IconButton(
                                icon=ft.Icons.SEND_ROUNDED,
                                tooltip="Enviar",
                                icon_color=ft.Colors.WHITE,
                                on_click=send_message_click,
                            )
                        ]
                    )
                ),
            ]
        )
    )

    def update_size(e):
        container.width = page.window.width
        container.height = page.window.height
        page.update()

    page.on_window_resize = update_size

    page.add(page.dialog, container)
    page.update()

ft.app(main)