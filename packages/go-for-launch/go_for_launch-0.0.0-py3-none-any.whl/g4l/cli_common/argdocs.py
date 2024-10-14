import os
import sys
import subprocess
import re
import json

DOCSTR = ''

def main():

    out_helps = {}
    help_node(['python3', '-m', sys.argv[1]], out_helps, 0)

    print('{}'.format(json.dumps(out_helps, indent=4)))

    build_help_md_string('avrs', out_helps, 0)

    with open('out.md', 'w', encoding='utf-8') as f:
        f.write(DOCSTR)

def build_help_md_string(node_name, node, depth):
    global DOCSTR
    DOCSTR += '{} {}\n'.format('#' * (depth + 1), node_name)
    if not 'usage' in node:
        print('no usage in node {}'.format(node_name))
        return
    DOCSTR += '`{}`\n\n'.format(node['usage'])
    DOCSTR += '{}\n'.format(node['options'].replace('\n', '<br /><br />'))
    if 'subs' in node:
        for s in node['subs']:
            build_help_md_string(s, node['subs'][s], depth + 1)


def help_node(cmd_chain, out_helps, depth):

    print('RUNNING: {}'.format(cmd_chain + ['-h']))
    result = subprocess.run(cmd_chain + ['-h'], stdout=subprocess.PIPE)
    result_output = result.stdout.decode('utf-8')
    print('result: {}'.format(result_output))

    usage_match = re.search(r'usage: (.*)\s', result_output)
    if usage_match: 
        out_helps['usage'] = usage_match.group(1)

    options_match = re.search(r'options:\s((?s).*\s*)', result_output)
    if options_match:
        out_helps['options'] = options_match.group(1)

        # parse out options

    #posargs_match = re.search(r'positional arguments:\s')

    out_helps['subs'] = {}

    m = re.search(r'arguments:\s*{(.*)}', result_output)

    if m:
        subs = m.group(1).split(',')
        print('subs: {}'.format(subs))
        for s in subs:
            out_helps['subs'][s] = {}
            help_node(cmd_chain + [s], out_helps['subs'][s], depth + 1)


if __name__ == '__main__':
    main()