# Deprecated


## Forks
- https://gitlab.com/poikilos/ilights
  - Poikilos' copy: ~/metaprojects/deprecated
  - Revert to 5a4cc589434de2e24b9f2b128cfb5f5ccef7f385 (CC BY-SA version of code before change to LGPL v3.0)
    - The revert doesn't seem complete, because newer commits are present (up to "fix the 'fix'" 51a4625).
    - For the details of how the fork was constructed, see the modified ilights readme link discussed under the "Merge branch..." point below.
    - The fork still had the "LICENSE" file with the separate licenses for code and media.
  - `lighten "off" bulb a bit (way too dark) + update license` (manually cherry pick commit 6398d89 by VanessaE but change the commit to add a copy of the license)
  - "Merge branch 'old-license-branch' into 'master'":
    - Change readme (See [deprecated/ilights/readme.md](deprecated/ilights/readme.md). The upstream version only says "Repo for ilights mod.")
    - Add license.txt (Attribution-ShareAlike 4.0 International).
- https://gitlab.com/poikilos/moretrees
  - Poikilos' copy: ~/metaprojects/deprecated
  - only adds depends.txt
- https://gitlab.com/poikilos/plantlife_modpack
  - Poikilos' copy: ~/metaprojects/deprecated
  - only adds depends.txt files


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
