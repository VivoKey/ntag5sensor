import argparse


def parse():
    parser = argparse.ArgumentParser(description = "Read and configure sensors connected to NTAG 5 Link")

    parser.add_argument("-hd", "--help-documentation", action="store_true", dest="documentation", 
        help="Print the complete help documentation")
    parser.add_argument("-l", "--list-readers", action="store_true", dest="listreaders", 
        help="list available ACR1552 readers")

    actions = parser.add_subparsers(help="desired action to perform", dest="action") 

    # Interfacing options
    parser_handle_interface = argparse.ArgumentParser(add_help=False)
    parser_handle_interface.add_argument("-r", "--reader", nargs="?", dest="reader", type=int, 
        const=0, default=0, required=False, 
        help="index of the available ACR1552 readers to use (default: 0)")
    
    # Persistent configuration options
    parser_handle_config = argparse.ArgumentParser(add_help=False)
    parser_handle_config.add_argument("-c", "--current", nargs="?", dest="current", type=str, 
        const="0.4", default="0.4", choices=["0.4", "0.6", "1.4", "2.7", "4.0", "6.5", "9.0", "12.5"], 
        help="minimum available current for energy harvesting to trigger, in mA (default: 0.4)")
    parser_handle_config.add_argument("-v", "--voltage", nargs="?", dest="voltage", type=str, 
        const="1.8", default="1.8", choices=["1.8", "2.4", "3.0"], 
        help="regulated voltage output of active energy harvesting, in V (default: 1.8)")

    # Sensor interfacing
    parser_handle_sensor_interface = argparse.ArgumentParser(add_help=False)
    parser_handle_sensor_interface.add_argument("-a", "--address", nargs="?", dest="address", type=int, 
        const=72, default=72, choices=[72, 73, 74, 75], 
        help="I2C address of the connected sensor chip (default: 72)")

    # Sensor reading options
    parser_handle_sensor_read = argparse.ArgumentParser(add_help=False)
    parser_handle_sensor_read.add_argument("-m", "--mode", nargs="?", dest="mode", type=str, 
        const="oneshot", default="oneshot", choices=["oneshot", "continuous"], 
        help="Mode to read the connected sensor chip in (default: oneshot)")

    # Sensor configuration options
    parser_handle_sensor_settings = argparse.ArgumentParser(add_help=False)
    parser_handle_sensor_settings.add_argument("-sm", "--startup-mode", nargs="?", dest="startupmode", type=str, 
        const="oneshot", default="oneshot", choices=["oneshot", "continuous"], 
        help="Startup mode to configure the connected sensor chip with (default: oneshot)")


    # INFO action
    parser_info = actions.add_parser("info", 
        parents=[parser_handle_interface],
        help="read information and configuration data of the NTAG5 Link")

    # SETUP action
    parser_info = actions.add_parser("setup", 
        parents=[parser_handle_interface, parser_handle_config],
        help="write persistent configuration settings into the NTAG5 Link EEPROM")


    # TMP117 action
    parser_tmp117 = actions.add_parser('tmp117', help='manage connected TMP117 sensor')
    subparsers_tmp117 = parser_tmp117.add_subparsers(
        help='desired action to perform on the connected TMP117 sensor', 
        dest='verb', required=True) 

    # TMP117 INFO action
    parser_tmp117_info = subparsers_tmp117.add_parser('info', 
        parents=[parser_handle_interface, parser_handle_sensor_interface], 
        help='read information and configuration of the connected TMP117 sensor')

    # TMP117 SETUP action
    parser_tmp117_info = subparsers_tmp117.add_parser('setup', 
        parents=[parser_handle_interface, parser_handle_sensor_interface, parser_handle_sensor_settings], 
        help='write persistent configuration to the connected TMP117 sensor')

    # TMP117 READ action
    parser_tmp117_info = subparsers_tmp117.add_parser('read', 
        parents=[parser_handle_interface, parser_handle_sensor_interface, parser_handle_sensor_read], 
        help='read measurement data from the connected TMP117 sensor')

    args = parser.parse_args()
    return (parser, args)


def validate(parser, args):
    if(args.documentation):
        print(parser.format_help())
        subparsers_actions = [
            action for action in parser._actions 
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for _, action in subparsers_action.choices.items():
                subparsers_verbs = [
                    action for action in action._actions 
                    if isinstance(action, argparse._SubParsersAction)]
                for subparsers_verb in subparsers_verbs:
                    for _, verb in subparsers_verb.choices.items():
                        print(verb.format_help())
        exit(0)

    if(args.listreaders):
        return

    if(args.action is None):
        parser.print_help()
        exit(1)
