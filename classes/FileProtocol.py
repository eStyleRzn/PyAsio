import asyncio

# ======================================================================================================================
# @asyncio.coroutine
def send_data(proto, transport):
    for i in range(0, 20):
        #  print(datetime.datetime.now())

        transport.write(proto.message.encode())
        print('Data sent: {!r}'.format(proto.message))

        yield from asyncio.sleep(1.0)