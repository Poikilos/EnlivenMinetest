import os
import sys
import traceback

class InstalledFile:
    source_dir_path = None
    dest_dir_path = None
    file_name = None

    def __init__(self, file_name, source_dir_path, dest_dir_path):
        self.file_name=file_name
        self.source_dir_path=source_dir_path
        self.dest_dir_path=dest_dir_path

class ConsoleInputConfigFile:
    #config_name = None
    _config_path = None
    _data = None
    _ao = None

    #DOES load variables if path exists
    def __init__(self, config_file_path, assignment_operator_string):
        self._data = {}
        self._config_path = config_file_path
        self._ao = assignment_operator_string
        self._data = get_dict_modified_by_conf_file(self._data, self._config_path, self._ao)

    #DOES ask for user input if does not exist
    def ask_for_value_if_not_loaded(name, default_value, description):
        if name not in self._data:
            if default_value is None:
                default_value = ""
            answer = raw_input("Please specify "+description+" [blank for "+default_value+"]: ")
            if answer is not None:
                answer = answer.strip()
                if len(answer)>0:
                    self_data[name] = answer
                else:
                    self_data[name] = default_value
        if not os.path.isfile(self._config_path):
            is_changed = True
            print("Creating '"+self._config_path+"'")
        if is_changed:
            self.save_yaml()


    #DOES autosave IF different val
    def set_val(name, val):
        is_changed = False
        if name not in self._data.keys():
            is_changed = True
        elif self._data[name] != val:
            is_changed = True
        if is_changed:
            self._data[name] = val
            self.save_yaml()

    def get_val(name):
        result = None
        if name in self._data:
            result = self._data[name]
        return result

    def save_yaml()
        save_conf_from_dict(self._config_path, self._data, self._ao, save_nulls_enable=False)

def get_dict_deepcopy(old_dict):
    new_dict = None
    if type(old_dict) is dict:
        new_dict = {}
        for this_key in old_dict.iterkeys():
            new_dict[this_key] = old_dict[this_key]
    return new_dict

def is_dict_subset(new_dict, old_dict, verbose_messages_enable, verbose_dest_description="unknown file"):
    is_changed = False
    try:
        if old_dict is not None:
            if new_dict is not None:
                old_dict_keys = old_dict.keys()
                for this_key in new_dict.iterkeys():
                    if (this_key not in old_dict_keys):
                        is_changed = True
                        if verbose_messages_enable:
                            print("SAVING '"+verbose_dest_description+"' since "+str(this_key)+" not in saved version.")
                        break
                    elif new_dict[this_key] != old_dict[this_key]:
                        is_changed = True
                        if verbose_messages_enable:
                            print("SAVING '"+verbose_dest_description+"' since "+str(this_key)+" not same as saved version.")
                        break
            #else new_dict is None so no change detected (no new information)
        else:
            if new_dict is not None:
                is_changed = True
    except:
        print("Could not finish is_dict_subset:")
        view_traceback()
    return is_changed

def ivec2_equals(pos1, pos2):
    return (int(pos1[0])==int(pos2[0])) and (int(pos1[1])==int(pos2[1]))

def get_dict_from_conf_file(path,assignment_operator="="):
    results = None
    results = get_dict_modified_by_conf_file(results, path, assignment_operator)
    return results

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def RepresentsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def view_traceback():
    ex_type, ex, tb = sys.exc_info()
    print(str(ex_type))
    print(str(ex))
    traceback.print_tb(tb)
    del tb

def print_file(path, min_indent=""):
    line_count = 0
    try:
        if path is not None:
            if os.path.isfile(path):

                if min_indent is None:
                    min_indent = ""
                ins = open(path, 'r')
                line = True
                while line:
                    line = ins.readline()
                    line_count += 1
                    if line:
                        print(min_indent+line)
                ins.close()
                #if line_count==0:
                    #print(min_indent+"print_file WARNING: "+str(line_count)+" line(s) in '"+path+"'")
                #else:
                    #print(min_indent+"# "+str(line_count)+" line(s) in '"+path+"'")
            else:
                print (min_indent+"print_file: file does not exist")
        else:
            print (min_indent+"print_file: path is None")
    except:
        print(min_indent+"print_file: could not finish")
        try:
            ins.close()
        except:
            pass
    return line_count

def get_dict_modified_by_conf_file(this_dict, path,assignment_operator="="):
    results = this_dict
    #print ("Checking "+str(path)+" for settings...")
    if (results is None) or (type(results) is not dict):
        results = {}
    if os.path.isfile(path):
        ins = open(path, 'r')
        line = True
        while line:
            line = ins.readline()
            if line and len(line)>0:
                line_strip=line.strip()
                if len(line_strip)>0 and not line_strip[0]=="#":  # if not comment
                    if not line_strip[0]=="-":  # ignore yaml arrays
                        ao_index = line_strip.find(assignment_operator)
                        if ao_index>=1:  # intentionally skip zero-length variable names
                            if ao_index<len(line_strip)-1:  # skip yaml implicit nulls or yaml objects
                                result_name = line_strip[:ao_index].strip()
                                result_value = line_strip[ao_index+1:].strip()
                                result_lower = result_value.lower()
                                if result_value=="None" or result_value=="null" or result_value=="~" or result_value=="NULL":
                                    result_value = None
                                elif result_lower=="true":
                                    result_value = True
                                elif result_lower=="false":
                                    result_value = False
                                elif RepresentsInt(result_value):
                                    result_value = int(result_value)
                                elif RepresentsFloat(result_value):
                                    result_value = float(result_value)
                                #print ("   CHECKING... "+result_name+":"+result_value)
                                results[result_name]=result_value
        ins.close()
    return results

def save_conf_from_dict(path, this_dict, assignment_operator="=", save_nulls_enable=True):
    try:
        outs = open(path, 'w')
        for this_key in this_dict.keys():
            if save_nulls_enable or (this_dict[this_key] is not None):
                if this_dict[this_key] is None:
                    outs.write(this_key+assignment_operator+"null\n")
                else:
                    outs.write(this_key+assignment_operator+str(this_dict[this_key])+"\n")
        outs.close()
    except:
        print("Could not finish saving chunk metadata to '"+str(path)+"': "+str(traceback.format_exc()))
        try:
            outs.close()
        except:
            pass

def get_tuple_from_notation(line, debug_src_name="<unknown object>"):
    result = None
    if line is not None:
        # mark chunk
        tuple_noparen_pos_string = line.strip("() \n\r")
        pos_strings = tuple_noparen_pos_string.split(",")
        if len(pos_strings) == 3:
            try:
                player_x = float(pos_strings[0])
                player_y = float(pos_strings[1])
                player_z = float(pos_strings[2])
            except:
                player_x = int(pos_strings[0])
                player_y = int(pos_strings[1])
                player_z = int(pos_strings[2])
            result = player_x, player_y, player_z
        else:
            print("'"+debug_src_name+"' has bad position data--should be 3-length (x,y,z) in position value: "+str(pos_strings))
    return result

def is_same_fvec3(list_a, list_b):
    result = False
    if list_a is not None and list_b is not None:
        if len(list_a)>=3 and len(list_b)>=3:
            result = (float(list_a[0]) == float(list_b[0])) and (float(list_a[1]) == float(list_b[1])) and (float(list_a[2]) == float(list_b[2]))
    return False
