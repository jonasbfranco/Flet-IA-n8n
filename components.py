import flet as ft

class Message:
    def __init__(self, user_name: str, text: str, user_type: str):
        self.user_name = user_name
        self.text = text
        self.user_type = user_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.alignment = ft.MainAxisAlignment.START 
        self.vertical_alignment = ft.CrossAxisAlignment.START # eixovertical
        self.spacing = 8

        if message.user_type == "ia":
            avatar = ft.Icon(ft.Icons.ASSISTANT, size=20, color=ft.Colors.WHITE)
        else:
            avatar = ft.Text(self.__get_initials(message.user_name), size=20, color=ft.Colors.WHITE)

        
        # Criar os controles
        self.controls = [
            ft.CircleAvatar(
                content=avatar,
                color=ft.Colors.WHITE,
                bgcolor=self.__get_avatar_color(message.user_name, message.user_type),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, size=12, weight="bold", color=ft.Colors.WHITE),
                    ft.Markdown(message.text, selectable=True, width=300),
                ],
                tight=True,
                spacing=5,
            )
        ]

    def __get_initials(self, user_name: str):
        parts = user_name.split()
        if len(parts) == 0:
            return ""
        elif len(parts) == 1:
            return parts[0][0].upper() + parts[0][1].upper()
        else:
            return parts[0][0].upper() + parts[1][0].upper()
            

        
    def __get_avatar_color(self, user_name: str, user_type: str):
        if user_name == "IA":
            return ft.Colors.PURPLE
        
        color_lookup = [
            
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ]

        # Map user names to colors
        user_name_hash = hash(user_name)
        return color_lookup[user_name_hash % len(color_lookup)]

