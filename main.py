import argparse
import _queue
import os.path
import re
import tempfile
from multiprocessing import Manager, Process

def wrapper_hard(queue, *args):
    queue.put(FlipperNested.calculate_keys_hard(*args))

class FlipperNested:
    VERSION = 3
    FILE_TYPES = ["Flipper Nested Nonce Manifest File", "Flipper Nested Nonces File"]
    DEPTH_VALUES = {1: 25, 2: 50, 3: 100}
    FLIPPER_PATH = "/ext/nfc/.nested/"
    LEGACY_PATH = "/ext/nfc/nested/"

    def __init__(self):
        self.connection = None
        self.filename = None
        self.nonces = None
        self.found_keys = None
        self.bruteforce_distance = [0, 0]
        self.progress_bar = False
        self.save = False
        self.preserve = False
        self.uid = ""

    def run(self, args=None):
        if args:
            self.progress_bar = args.progress
            self.save = args.save
            self.preserve = args.preserve
            self.uid = args.uid
        self.extract_nonces_from_file(args.file)

    def parse_file(self, contents):
        # TODO: Designed for one target key
        self.nonces = {"A": {}, "B": {}}
        self.found_keys = {"A": {}, "B": {}}
        lines = contents.splitlines()
        for line in lines:
            values = self.parse_line(line)
            sec, key_type = values[-2:]
            if sec not in self.nonces[key_type].keys():
                self.nonces[key_type][sec] = []
            file = tempfile.NamedTemporaryFile(delete=False)
            nonces_filename = values[1].rsplit("/", 1)[1]
            if self.connection:
                value = self.connection.file_read(values[1])
            elif os.path.dirname(self.filename) and os.path.isfile(
                    os.path.dirname(self.filename) + "/" + nonces_filename):
                # file in same directory as input file
                value = open(os.path.dirname(self.filename) + "/" + nonces_filename, "rb").read()
            elif os.path.dirname(self.filename) and os.path.isfile(
                    os.path.dirname(self.filename) + "/" + self.filename.rsplit(".", 1)[
                        0] + "/" + nonces_filename):
                # copied from .nested directory with UID
                value = open(os.path.dirname(self.filename) + "/" + self.filename.rsplit(".", 1)[
                    0] + "/" + nonces_filename, "rb").read()
            elif os.path.isfile(self.filename.rsplit(".", 1)[
                        0] + "/" + nonces_filename):
                # copied from .nested directory with UID, from current directory
                value = open(self.filename.rsplit(".", 1)[
                    0] + "/" + nonces_filename, "rb").read()
            elif os.path.isfile(nonces_filename):
                # file in current directory (--save)
                value = open(nonces_filename, "rb").read()
            else:
                print("[!] Missing {} file and Flipper Zero isn't connected".format(nonces_filename))
                print("[?] If you are trying to recover from Hard Nested offline, you should copy this file")
                return False
            open(file.name, "wb+").write(b"\n".join(value.split(b"\n")[4:]))
            if self.save:
                open(nonces_filename, "wb+").write(value)
            values[1] = file.name
            self.nonces[key_type][sec].append(values)
        return len(self.nonces["A"]) + len(self.nonces["B"]) > 0

    def extract_nonces_from_file(self, file):
        self.filename = file.name
        if not self.parse_file(file.read()):
            print("[!] Failed to parse", self.filename)
            return
        self.recover_keys()
        self.save_keys_to_file()

    def recover_keys(self):
        for key_type in self.nonces.keys():
            for sector in self.nonces[key_type].keys():
                for info in self.nonces[key_type][sector]:
                    print("Recovering key type", key_type + ", sector", sector)
                    m = Manager()
                    q = m.Queue()
                    value = info[:-2]
                    value.insert(0, q)

                    p = Process(target=wrapper_hard, args=value)
                    p.start()

                    try:
                        p.join()
                    except KeyboardInterrupt:
                        print("Stopping...")
                        p.kill()
                        return True

                    try:
                        keys = q.get(timeout=1).split(";")
                    except _queue.Empty:
                        print("[!!!] Something went VERY wrong in key recovery.\nYou MUST report this to developer!")
                        return
                    keys.pop()

                    print(f"Found {str(len(keys))} key(s):", keys)

                    if keys:
                        self.found_keys[key_type][sector] = keys
                        break
                    elif info == self.nonces[key_type][sector][-1]:
                        print("[!] Failed to find keys for this sector, try running Nested attack again")

    def save_keys_to_string(self):
        output = ""
        for key_type in self.found_keys.keys():
            for sector in self.found_keys[key_type].keys():
                for key in self.found_keys[key_type][sector]:
                    output += f"Key {key_type} sector {str(sector).zfill(2)}: " + " ".join(
                        [key.upper()[i:i + 2] for i in range(0, len(key), 2)]) + "\n"

        keys = output.count("Key")
        if keys:
            print("[+] Found potential {} keys, use \"Check found keys\" in app".format(keys))
        return output.strip()

    def save_keys_to_file(self):
        output = self.save_keys_to_string()
        if not output:
            print("[-] No keys found!")
            return
        filename = self.filename + ".keys"
        open(filename, "w+").write(output)
        print("[?] Saved keys to", filename)

    def save_keys_to_flipper(self):
        output = self.save_keys_to_string()
        if not output:
            print("[-] No keys found!")
            return
        filename = self.filename.replace("nonces", "keys")
        if self.save:
            open(filename, "w+").write(output)
            print("[?] Saved keys to", filename)
        try:
            self.connection.file_write(self.FLIPPER_PATH + filename, output.encode())
            if not self.preserve:
                self.connection.file_delete(self.FLIPPER_PATH + self.filename)
        except:
            if not self.save:
                open(filename, "w+").write(output)
                print("[!] Lost connection to Flipper!")
                print("[?] Saved keys to", filename)

    @staticmethod
    def parse_line(line):
        result = re.search(
            r"Key ([A-B]) cuid (0x[0-9a-f]*) nt0 (0x[0-9a-f]*) ks0 (0x[0-9a-f]*) par0 ([0-9a-f]*) nt1 (0x[0-9a-f]*) ks1 (0x[0-9a-f]*) par1 ([0-9a-f]*) sec (\d{1,2})",
            line.strip())
        groups = result.groups()

        key_type, sec = groups[0], int(groups[-1])
        values = list(
            map(lambda x: x if x.startswith("/") else (int(x, 16) if x.startswith("0x") else int(x)), groups[1:-1]))
        values.append(sec)
        values.append(key_type)
        return values

    @staticmethod
    def calculate_keys_hard(uid, filename):
        import faulthandler
        faulthandler.enable()
        import hardnested
        run = hardnested.run_hardnested(uid, filename)
        return run

def main():
    parser = argparse.ArgumentParser(description="Recover keys after Nested attack")
    parser.add_argument("--uid", type=str, help="Recover only for this UID", default="")
    parser.add_argument("--port", type=str, help="Port to connect", default="")
    parser.add_argument("--progress", action="store_true", help="Show key recovery progress bar")
    parser.add_argument("--save", action="store_true", help="Debug: Save nonces/keys from Flipper")
    parser.add_argument("--preserve", action="store_true", help="Debug: Don't remove nonces after recovery")
    parser.add_argument("--file", type=argparse.FileType("r"), help="Debug: Recover keys from local .nonces file")
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    flipper = FlipperNested()
    flipper.run(args)

if __name__ == "__main__":
    main()
