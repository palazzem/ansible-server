from tempfile import NamedTemporaryFile


def parser(param):
    return {
        "app_name": param.get("app_name"),
        "server_name": param.get("server_name"),
        "user_name": param.get("app_name"),
        "user_pass": param.get("password"),
        "python_version": param.get("python"),
        "createdb": param.get("createdb"),
    }


def write_hosts_inventory(appserver):
    hosts_file = NamedTemporaryFile(delete=False)
    hosts = "[appservers]\n{0}".format(appserver)

    hosts_file.write(hosts)
    hosts_file.close()
    return hosts_file.name
