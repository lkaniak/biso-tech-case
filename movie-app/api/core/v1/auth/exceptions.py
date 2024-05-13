class InvalidCredentials(Exception):
    def __init__(self):
        self.message = "Credenciais inválidas."


class InactiveUser(Exception):
    def __init__(self):
        self.message = "Usuário inativo."
