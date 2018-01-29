import asyncio

from dispatcher import CommandDispatcher as cmd


@cmd.register
def iam(name):
    return f'hello {name}'


@cmd.register
def ping():
    return 'pong'


@cmd.register
def quit():
    return 'bye'


async def handle_client(reader, writer):
    while True:
        request = (await reader.read(255)).decode('utf8')
        if not request:
            return
        response = cmd.run(request)
        writer.write(response.encode('utf8'))


loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(handle_client, 'localhost', 15555))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
