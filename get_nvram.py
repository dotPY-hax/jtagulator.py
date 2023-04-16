from get_uart import get_uart


def get_nvram():
    jtagulator_object = get_uart(3.3, 0, 1)
    if jtagulator_object.rx and jtagulator_object.tx and jtagulator_object.baud:
        jtagulator_object.use_passthru()
        jtagulator_object._connection.write_read("\r\n")
        jtagulator_object._connection.write_read("\r\n")
        jtagulator_object._connection.write("nvram show")
        console_output = jtagulator_object._connection.read()
        return parse_nvram(console_output)
    return {}


def parse_nvram(console_output):
    if not console_output.startswith(b"nvram show\r\n"):
        print("NOT NVRAM!!")
        print(console_output)
    command, *nvram, size, next_prompt = console_output.split(b"\r\n")
    nvram_dict = {}
    for entry in nvram:
        try:
            key, value = entry.split(b"=", 1)
            nvram_dict[key.decode()] = value.decode()
        except ValueError:
            print("Got weird stuff in nvram")
            print(entry)

    return nvram_dict
