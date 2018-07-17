import datetime
import pexpect
import yaml
from pprint import pprint as pp


now = datetime.datetime.now()
currentDateTime = now.strftime('%m-%d-%Y %H:%M:%S')
config_file = 'config.yaml'

def main():
    print("This is main")
    load_config(config_file)
    for router in config['routers']:
        prompt = router[0] + ">"
        print(prompt)
        exec_command(router[0], router[1], prompt)


def load_config(config_file):
    global config
    config = yaml.load(open(config_file))


def exec_command(hostname ,ip_address, prompt):
    try:
        child = pexpect.spawn('ssh {}@{}'.format(config['username'], ip_address) )
        child.expect("assword:")
        print(child.before)
        child.sendline(config['password'])
        child.expect(prompt)

    except:
        print("Unable to connect to {}".format(hostname))

    else:
        child.sendline("set cli screen-length 0")
        child.expect(prompt)
        for command in config['commands']:
            child.sendline(command)
            child.expect(prompt)
            write_to_file(child.before, hostname)
        print("host completed, exiting..")
        child.sendline('quit')



def write_to_file(output, hostname):
    with open(config['output'], 'ab') as out:
        title = "-".join([hostname,currentDateTime])
        out.write(title.center(80, "-").encode())
        out.write("\r\n".encode())
        out.write(output)

if __name__ == "__main__":
    main()