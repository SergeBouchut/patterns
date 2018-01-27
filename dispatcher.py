class CommandDispatcher:
    _commands = {}

    @classmethod
    def run(cls, command):
        name, *args = command.split()
        try:
            return str(cls._commands[name](*args))
        except KeyError:
            return 'Invalid command.'
        except (TypeError, ValueError):
            return 'Invalid parameters.'

    @classmethod
    def register(cls, function):
        cls._commands[function.__name__] = function
        return function


cmd = CommandDispatcher
assert(cmd.run('bye') == 'Invalid command.')


@cmd.register
def hello(to='world'):
    """Say hello to anyone."""
    return f'Hello {to}!'

assert(cmd.run('hello jane') == 'Hello jane!')
assert(cmd.run('hello') == 'Hello world!')
assert(cmd.run('hello jane john') == 'Invalid parameters.')


@cmd.register
def add(*numbers):
    """Add numbers, as much as you want."""
    return sum((int(number) for number in numbers))

assert(cmd.run('add 1 2 3') == '6')
assert(cmd.run('add 1 2 trois') == 'Invalid parameters.')


@cmd.register
def help(command=None):
    """Return available commands or command description."""
    if command is None:
        return ' '.join(cmd._commands.keys())
    return cmd._commands[command].__doc__

assert(cmd.run('help hello') == 'Say hello to anyone.')
assert(cmd.run('help bye') == 'Invalid command.')
assert(cmd.run('help') == 'hello add help')
assert(cmd.run('help help') == 'Return available commands or command description.')
assert(cmd.run('help help hello') == 'Invalid parameters.')
