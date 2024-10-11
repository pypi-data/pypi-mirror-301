


import configparser


def ini_to_dict(config_path):
    parser = configparser.ConfigParser()
    parser.read(config_path)
    
    config_dict={key:parser.get('DEFAULT', key) for key in parser['DEFAULT']}
    
    init_dict={}
    for section in parser.sections():
        section_tree_headers=section.split('.')

        
        value_config={}
        value_config[section] = dict(parser.items(section))
        for key in config_dict:
            value_config[section].pop(key)
        
        # Handles the case where there is only one section tag
        if len(section_tree_headers)==1:
            init_dict.update(value_config)
            continue
        
        section_tree_dict=None
        for i,section_tree_header in enumerate(section_tree_headers):
            # Handles the first section section tag
            if i==0:
                if section_tree_header in config_dict:
                    raise ValueError(f"Section {section} already exists in the default dictionary.\n"
                                        "Please rename the section such that it is not in conflict with the default keys."
                                        )
                if section_tree_header not in init_dict:
                    init_dict[section_tree_header]={}
                section_tree_dict=init_dict[section_tree_header]
                
            # Handles the last section tag
            elif i==len(section_tree_headers)-1:
                
                if section_tree_header not in section_tree_dict:
                    section_tree_dict[section_tree_header]=value_config[section]
                else:
                    section_tree_dict[section_tree_header].update(value_config[section])
                
            # Handles the intermediate section tags
            else:
                if section_tree_header not in section_tree_dict:
                    section_tree_dict[section_tree_header]={}
                section_tree_dict=section_tree_dict[section_tree_header]

    config_dict.update(init_dict)
    
    return config_dict

    