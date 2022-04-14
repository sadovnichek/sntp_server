from server import Server


def main():
    offset = 0
    with open("server.conf", encoding="utf-8") as file:
        for line in file.readlines():
            if "offset" in line:
                offset = int(line.split("=")[1])
    server = Server(offset)
    server.start()


if __name__ == "__main__":
    main()
