from tempfile import NamedTemporaryFile


def parser(param):
    return {
        "app_name": param.get("name"),
        "server_name": param.get("app_server"),
        "user_name": param.get("name"),
        "user_pass": param.get("password"),
        "psql_pass": param.get("psql_password"),
        "python_version": param.get("python"),
    }


def write_hosts_inventory(appserver):
    hosts_file = NamedTemporaryFile(delete=False)
    hosts = "[appservers]\n{0}".format(appserver)

    hosts_file.write(hosts)
    hosts_file.close()
    return hosts_file.name
