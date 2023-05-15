from get_uart import get_uart


def get_nvram(voltage, start_pin, stop_pin):
    jtagulator_object = get_uart(voltage, start_pin, stop_pin)
    if jtagulator_object.rx and jtagulator_object.tx and jtagulator_object.baud:
        passthru = jtagulator_object.use_passthru()
        passthru.interact("\r\n")
        passthru.interact("\r\n")
        passthru.write("nvram show")
        console_output = passthru.read()
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
