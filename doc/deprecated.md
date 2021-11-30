# Deprecated

## enissue.py
### argparse
Why: making mutually exclusive arguments or subcommands optional
doesn't seem to work.
- Use the Poikilos argparsebetter module such as from
  <https://github.com/poikilos/argparsebetter> instead if such features
  are necessary.
```
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Process issues.')
    subparsers = parser.add_subparsers()
    # vParser = subparsers.add_parser('--verbose', aliases=['--debug'])
    # vParser.add_argument('foo')
    # qG = parser.add_mutually_exclusive_group(required=False)
    # qG.add_argument('open', action='store_true')
    # qG.add_argument('closed', action='store_false')
    # ^ They have to be required, so see
    #   <https://stackoverflow.com/questions/59773946/argparse-required-add-mutually-exclusive-group-parameters-list-as-optional>:
    state_help = {}
    for api_name, api in apis.items():
        default_query = api.get('default_query')
        default_query_state = default_query.get('state')
        state_help[api_name] = default_query_state
    '''
    parser.add_argument('state', choices=['open', 'closed'],
                        default="open",
                        help=('Show open or closed issues only'
                              ' (defaults are {}).'.format(state_help)))
    '''
    # ^ Makes it required so see
    #   <https://stackoverflow.com/a/40324928/4541104>
    #   on <https://stackoverflow.com/questions/40324356/python-argparse-choices-with-a-default-choice>

    parser_list = subparsers.add_parser('open')
    # parser_open.add_argument('open_type', default='all', const='all', nargs='?', choices=['all', 'servers', 'storage'])

    parser_closed = subparsers.add_parser('closed')
    # parser_closed.add_argument('closed_type', default='server', const='server', nargs='?', choices=['server', 'storage'])

    # parser.print_help()
    parser.parse_args(sys.argv)
    print("open: {}".format(parser.get("open")))
    sys.exit(0)
```
