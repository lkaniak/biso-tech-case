class UserNotFound(Exception):
    def __init__(self):
        self.message = "Usuário não encontrado."


class EmailAlreadyExists(Exception):
    def __init__(self):
        self.message = "Já existe um usuário cadastrado com esse email."
