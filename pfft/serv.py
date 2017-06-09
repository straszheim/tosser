import asyncio, logging, os, socket

os.environ['PYTHONASYNCIODEBUG'] = '1'
FORMAT = '... %(module)s:%(lineno)d] %(message)s'
logging.basicConfig(format=FORMAT)
logging.getLogger('').setLevel(logging.DEBUG)

log = logging.getLogger('asyncio').debug

def protocol_factory():
    log("protocol_factory!")
    return None

def hello_world():
    log("hello hello")
    return 42

clients = {}

def accept_client(client_reader, client_writer):
    task = asyncio.Task(handle_client(client_reader, client_writer))
    clients[task] = (client_reader, client_writer)
    def client_done(task):
        del clients[task]
        client_writer.close()
        log("done connection")

    log("new connection")
    task.add_done_callback(client_done)

async def handle_client(client_reader, client_writer):
    log("************** client_connected_cb!  %s %s" % (client_reader,client_writer))
    stuffs = await client_reader.readline()
    if stuffs is None:
        return
    log("yay read %s" % stuffs.decode())
    res = eval(stuffs.decode())
    log("evalled to %s", repr(res))
    client_writer.write(repr(res).encode())

def pfftserv(path):
    log("pfftserv on %s" % path)
    loop = asyncio.get_event_loop()

    if (os.path.exists(path)):
        os.unlink(path)

    f = asyncio.start_unix_server(accept_client, path=path)
    loop.run_until_complete(f)
    loop.run_forever()
    loop.close()

def pfftclient(path):
    log("CLIENT!")
    log("pfftclient connecting")
    loop = asyncio.get_event_loop()
    [reader, writer] = loop.run_until_complete(asyncio.open_unix_connection(path))
    log("wrote stuffs")
    writer.write(b'17*999.1\n')
    reply = loop.run_until_complete(reader.readline())
    # asyncio.ensure_future(reply)
    log("reply is %s" % reply)
    rslt = eval(reply.decode())
    log("result is %s (%s)" % (repr(rslt), type(rslt)))
    #r = await reply
    #log("r is %s" % r)
    # loop.run_until_complete(cli)
    # loop.call_later(2.5, hello_world)
    # loop.run_forever()
    # loop.close()
