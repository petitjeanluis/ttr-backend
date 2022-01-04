class StateMachineException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f'StateMachineException: {msg}')

class StateMachineValidationException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f'StateMachineValidationException: {msg}')
