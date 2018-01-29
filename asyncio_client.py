import asyncio


async def handle_input():
    while True:
        value = input('>> ')
        return value


async def handle_server(loop):
    reader, writer = await asyncio.open_connection('localhost', 15555, loop=loop)
    request = None
    while request != 'quit':
        request = await handle_input()
        if not request:
            continue
        writer.write(request.encode('utf8'))
        response = (await reader.read(255)).decode('utf8')
        print(response)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(handle_server(loop))
except KeyboardInterrupt:
    loop.close()
