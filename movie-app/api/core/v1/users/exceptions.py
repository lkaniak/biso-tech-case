class UserNotFound(Exception):
    def __init__(self):
        self.message = "Usuário não encontrado."


class EmailAlreadyExists(Exception):
    def __init__(self):
        self.message = "Já existe um usuário cadastrado com esse email."


class InvalidPassword(Exception):
    def __init__(self):
        self.message = "Senha incorreta."


class InvalidNewPassword(Exception):
    def __init__(self, errors: list[str]):
        nl = "\n"
        self.message = f"Senha inválida. Erros encontrados: {nl.join(errors)}"


class RegistrationNotSupported(Exception):
    def __init__(self):
        self.message = "Servidor não suporta autenticação sem login."


class SelfDeleteError(Exception):
    def __init__(self):
        self.message = "Usuário tentou se deletar."
