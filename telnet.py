import telnetlib

tn = telnetlib.Telnet('10.56.33.31')
tn.read_until(b'# ')

def traf_gen():
    cmd = 'traf-gen 1.1.1.1 250 250 101'
    tn.write(cmd.encode("ascii") + b"\r\n")

traf_gen()



