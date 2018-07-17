import datetime
import pexpect


username = 'user'
password = 'abc123'

routers = (['192.168.0.1', 'pe01'],)

commands = ('show version',
           'show chassis routing-engine')

now = datetime.datetime.now()
currentDateTime = now.strftime('%m-%d-%Y %H:%M:%S')

filename = "result.txt"


def main():
    print("This is main")
    for router in routers:
        prompt = username + "@" + router[1] + ">"
        print(prompt)
        exec_command(router[0], prompt)

def exec_command(router, prompt):

        child = pexpect.spawn('ssh {}@{}'.format(username, router) )
        child.expect("assword:")
        print(child.before)
        child.sendline(password)
        child.expect(prompt)
        child.sendline("set cli screen-length 0")
        child.expect(prompt)
        for command in commands:
            child.sendline(command)
            child.expect(prompt)
            write_to_file(child.before)
        child.sendline('quit')
        #
        # print("Unable to connect to {}".format(router))

def write_to_file(output):
    with open(filename, 'ab') as out:
        out.write(currentDateTime.center(80, "-").encode())
        out.write("\r\n".encode())
        out.write(output)


if __name__ == "__main__":
    main()