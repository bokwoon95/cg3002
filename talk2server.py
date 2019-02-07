
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Invalid number of arguments')
        print('python server.py [IP address] [Port] [groupID]')
        sys.exit()
    ip_addr = sys.argv[1]
    port_num = int(sys.argv[2])
    groupID = sys.argv[3]
