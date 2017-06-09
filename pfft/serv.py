import asyncio, logging, os, socket

os.environ['PYTHONASYNCIODEBUG'] = '1'
FORMAT = '... %(message)s'
logging.basicConfig(format=FORMAT)
logging.getLogger('asyncio').setLevel(logging.DEBUG)

log = logging.getLogger('asyncio').debug

def protocol_factory():
    log("protocol_factory!")
    return None

async def hello_world():
    log("hello hello")

async def client_connected_cb(client_reader, client_writer):
    log("************** client_connected_cb!  %s %s" % (client_reader,client_writer))
    stuffs = await client_reader.read()
    print("yay read %s" % stuffs)
    client_writer.write(b'YAH WHATEVER KTHXBYE\n\n\n\n')

def pfftserv(path):
    log("SERV!")
    log("pfftserv starting")
    loop = asyncio.get_event_loop()

    if (os.path.exists(path)):
        os.unlink(path)

    loop.run_until_complete(asyncio.start_unix_server(client_connected_cb, path=path))
    loop.run_forever()
    loop.close()

def pfftclient(path):
    log("CLIENT!")
    log("pfftclient connecting")
    loop = asyncio.get_event_loop()
    [reader, writer] = loop.run_until_complete(asyncio.open_unix_connection(path))
    log("wrote stuffs")
    writer.write(b'GEEEETT SOME')
    reply = reader.readline()
    asyncio.ensure_future(reply)
    log("reply is %s" % reply)
    #r = await reply
    #log("r is %s" % r)
    # loop.run_until_complete(cli)
    # loop.call_later(2.5, hello_world)
    # loop.run_forever()
    # loop.close()
