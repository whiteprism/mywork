from models import ServerInfo

def get_servers():
    return ServerInfo.objects.all()

def delete_server(id):
    ServerInfo.objects.get(id=id).delete()

def insert_server(data):
    server = ServerInfo(id=data["int_code"], zone_id=data["zone_id"], zone_name=data["zone_name"], name=data["name"], url=data["url"], status_id=data["status"],\
        status_text=data["status_info"], open_at=data["open_at"],code=data["code"],gm_url=data["gm_url"])
    server.save()

def get_server_by_request(request):
    server_id = request.COOKIES.get("sid", 0)

    try:
        server = ServerInfo.objects.get(pk=int(server_id))
    except:
        server = get_servers()[0]

    return server
