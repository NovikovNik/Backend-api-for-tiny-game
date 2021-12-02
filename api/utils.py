def config_parser(config_path):
    with open('/Users/novikovnikolay/Documents/GitHub/BackendForRFL/api/config.txt', 'r') as config_file:
        config = dict()
        lines = config_file.readlines()
        for line in lines:
            k, v = line.split(' = ')
            config[k] = v.split('\n')[0]
        return config