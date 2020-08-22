import os
import glob
import re
import json
import time

rules = []
regex = r'^\|\s*([^\s|\|]+)\s*\|([^\|]+)\|\s*$'
output_filename = 'rules.json'
rule_dir = os.path.join('rules', '*.md')
valid_causes = ['extension', 'browser', 'malware', 'other']
required_fields = ['cause', 'title', 'short_description']

for filename in glob.glob(rule_dir):
    temp_required_fields = required_fields.copy()
    print('[i] Processing {}...'.format(filename), end='')
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        rule = {}
        directives = {}
        markdown = f.read()
        matches = re.findall(regex, markdown, re.MULTILINE)
        for (field, value) in matches:
            value = value.strip()
            if field in temp_required_fields:
                rule[field] = value
                temp_required_fields.remove(field)
            elif field.startswith('url'):
                url_no = 1 if field == 'url' else field.split('_')[1]
                directives[url_no] = {
                    'url': value,
                    'directive': ''
                }
            elif field.startswith('directive'):
                directive_no = 1 if field == 'directive_no' else field.split('_')[1]
                if directive_no in directives:
                    directives[directive_no]['directive'] = value
        
        ld_start = markdown.find('## [Description]')
        ld_end = markdown.find('## [Comments]')

        is_valid = True
        errors = []
        if len(temp_required_fields) > 0:
            errors.append('[!] Invalid Rule. Required field missing: {}'.format(temp_required_fields))
            is_valid = False
        if len(directives) == 0:
            errors.append('[!] Invalid Rule. No directives specified.')
            is_valid = False
        if 'cause' in rule and not rule['cause'] in valid_causes:
            errors.append('[!] Invalid Rule. Cause is "{}" must be one of: {}'.format(rule['cause'], valid_causes))
            is_valid = False
        if ld_start == -1 or ld_end == -1:
            errors.append('[!] Invalid Rule. Could not find [Description] and [Comments] markers')
            is_valid = False
        
        if not is_valid:
            print(' FAILED')
            for err in errors:
                print(err)
            continue
        
        rule['id'] = os.path.basename(filename).replace('.md', '')
        rule['directives'] = list(directives.values())
        long_description = markdown[ld_start+16:ld_end].strip()
        rule['long_description'] = long_description
        rules.append(rule)
        print(' OK')
            
with open(output_filename, 'w') as f_out:
    out_dict = {
        'last_updated': time.time(),
        'rules': rules
    }
    json_str = json.dumps(out_dict)
    f_out.write(json_str)
    print('\n=> Compiled {} rules to {}'.format(len(rules), output_filename))