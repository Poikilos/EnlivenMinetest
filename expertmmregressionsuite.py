import os
import sys
import keyword
#import types
import inspect
import traceback

module_list = list()
module_list.append("os")
module_list.append("sys")
module_list.append("keyword")
module_list.append("inspect")
module_list.append("traceback")

def view_traceback():
    ex_type, ex, tb = sys.exc_info()
    print(str(ex_type))
    print(str(ex))
    traceback.print_tb(tb)
    del tb

class RegressionMismatch:
    side_a_string = None
    side_b_string = None
    endswith_enable = None
    startswith_enable = None
    
    def __init__(self, side_a_string, side_b_string, startswith_enable, endswith_enable):
        self.side_a_string = side_a_string
        self.side_b_string = side_b_string
        self.endswith_enable = endswith_enable
        self.startswith_enable = startswith_enable

global_case_sensitive_enable = None
y_enable = False
print("Initializing...")
regression_mismatches = list()
independent_list = ["index","suffix","prefix","decachunk_x_path"]
print("  (Ignoring the following independent variables:")
print(','.join(independent_list)+")")
#NOTE: "for decachunk_z_name in os.listdir(decachunk_x_path):" is ok since z folders are in x folder
independent_endswith_list = list()
for word in independent_list:
    independent_endswith_list.append("_"+word)
regression_mismatches.append(RegressionMismatch("_x","_z",False,True))

if y_enable:
    regression_mismatches.append(RegressionMismatch("_x","_y",False,True))
    regression_mismatches.append(RegressionMismatch("_y","_z",False,True))

regression_mismatches.append(RegressionMismatch("_x_","_z_",False,False))
if y_enable:
    regression_mismatches.append(RegressionMismatch("_x_","_y_",False,False))
    regression_mismatches.append(RegressionMismatch("_y_","_z_",False,False))

regression_mismatches.append(RegressionMismatch("x","z",False,True))
if y_enable:
    regression_mismatches.append(RegressionMismatch("x","y",False,True))
    regression_mismatches.append(RegressionMismatch("y","z",False,True))

regression_mismatches.append(RegressionMismatch("x_","z_",True,False))
if y_enable:
    regression_mismatches.append(RegressionMismatch("x_","y_",True,False))
    regression_mismatches.append(RegressionMismatch("y_","z_",True,False))

if global_case_sensitive_enable is True:
    regression_mismatches.append(RegressionMismatch("_X_","_Z_",False,False))
    if y_enable:
        regression_mismatches.append(RegressionMismatch("_X_","_Y_",False,False))
        regression_mismatches.append(RegressionMismatch("_Y_","_Z_",False,False))

    regression_mismatches.append(RegressionMismatch("_X","_Z",False,True))
    if y_enable:
        regression_mismatches.append(RegressionMismatch("_X","_Y",False,True))
        regression_mismatches.append(RegressionMismatch("_Y","_Z",False,True))

    regression_mismatches.append(RegressionMismatch("X","Z",False,True))
    if y_enable:
        regression_mismatches.append(RegressionMismatch("X","Y",False,True))
        regression_mismatches.append(RegressionMismatch("Y","Z",False,True))

    regression_mismatches.append(RegressionMismatch("X_","Z_",True,False))
    if y_enable:
        regression_mismatches.append(RegressionMismatch("X_","Y_",True,False))
        regression_mismatches.append(RegressionMismatch("Y_","Z_",True,False))

#splits by any non-alphanumeric characters
#print(keyword.kwlist)
# DOESN'T WORK (from linuxbochs on http://stackoverflow.com/questions/6315496/display-a-list-of-user-defined-functions-in-the-python-idle-session ):
#function_list = [f for f in globals().values() if type(f) == types.FunctionType]
# DOESN'T WORK
#def dummy(): pass
#function_list = [f.__name__ for f in globals().values() if type(f) == type(dummy)]
function_list = list()
for module_string in module_list:
    exec ("function_list += inspect.getmembers("+module_string+", inspect.isroutine)")
  # NOTE: isfunction does NOT include c-defined functions such as those in math
function_names = list()
for function_tuple in function_list:
    function_names.append(function_tuple[0])
print("  (Ignoring known routines:")
print(','.join(function_names)+")")
print("")
print("")
def split_non_alnum(haystack, strip_enable=True, skip_keywords_enable=True):
    results = list()
    index = 0
    start_index = 0
    while index <= len(haystack):
        if index==len(haystack) or not haystack[index].isalnum():
            word = haystack[start_index:index]
            if (not skip_keywords_enable) or (word not in keyword.kwlist and word not in function_names):
                if strip_enable:
                    results.append(word.strip())
                else:
                    results.append(word)
            start_index = index+1
        index += 1
    return results

alpha_upper_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpha_lower_chars = alpha_upper_chars.lower()
alpha_chars = alpha_upper_chars+alpha_lower_chars
numeric_chars = "1234567890"
alnum_chars = alpha_chars+numeric_chars
identifier_chars = alnum_chars+"_"
issue_count = 0
file_list = list()
def is_identifier(needle):
    result = True
    for index in range(0,len(needle)):
        if needle[index] not in identifier_chars:
            result = False
            break
    return result
    
def split_non_identifier(haystack, strip_enable=True, skip_keywords_enable=True, skip_disoriented_enable=True):
    results = list()
    index = 0
    start_index = 0
    while index <= len(haystack):
        if index==len(haystack) or not is_identifier(haystack[index]):
            word = haystack[start_index:index]
            if (not skip_keywords_enable) or word not in keyword.kwlist:
                if (not skip_disoriented_enable) or (word not in independent_list and not endswith_any(word, independent_endswith_list)):
                    if strip_enable:
                        results.append(word.strip())
                    else:
                        results.append(word)
            start_index = index+1
        index += 1
    return results

def endswith(haystack, needle, case_sensitive_enable=False):
    if global_case_sensitive_enable is not None:
        case_sensitive_enable = global_case_sensitive_enable
    result = False
    if haystack is not None and needle is not None and len(needle)>0 and len(haystack)>=len(needle):
        if case_sensitive_enable:
            if haystack[-len(needle):] == needle:
                #print("haystack[-len(needle):] = "+haystack[-len(needle):]+" in "+haystack)
                result = True
        else:
            if haystack[-len(needle):].lower() == needle.lower():
                #print("haystack[-len(needle):].lower() = "+haystack[-len(needle):].lower()+" in "+haystack)
                result = True
    return result

def startswith(haystack, needle, case_sensitive_enable=False):
    if global_case_sensitive_enable is not None:
        case_sensitive_enable = global_case_sensitive_enable
    result = False
    if haystack is not None and needle is not None and len(needle)>0 and len(haystack)>=len(needle):
        if case_sensitive_enable:
            if haystack[:len(needle)] == needle:
                result = True
        else:
            if haystack[:len(needle)].lower() == needle.lower():
                result = True
    return result

def any_endswith(haystacks, needle, case_sensitive_enable=False):
    if global_case_sensitive_enable is not None:
        case_sensitive_enable = global_case_sensitive_enable
    result = False
    for haystack in haystacks:
        if endswith(haystack, needle, case_sensitive_enable):
            result = True
            break
    return result

def endswith_any(haystack, needles, case_sensitive_enable=False):
    if global_case_sensitive_enable is not None:
        case_sensitive_enable = global_case_sensitive_enable
    result = False
    for needle in needles:
        if endswith(haystack, needle, case_sensitive_enable):
            result = True
            break
    return result

def any_startswith(haystacks, needle, case_sensitive_enable=False):
    if global_case_sensitive_enable is not None:
        case_sensitive_enable = global_case_sensitive_enable
    result = False
    for haystack in haystacks:
        if startswith(haystack, needle, case_sensitive_enable):
            result = True
            break
    return result

#only works on strings IF case_sensitive_enable, since then would do lower() on each element of haystacks 
def in_any_string(needle, haystacks, case_sensitive_enable=False):
    if global_case_sensitive_enable is not None:
        case_sensitive_enable = global_case_sensitive_enable
    result = False
    if needle is not None and len(needle)>0:
        for haystack in haystacks:
            if haystack is not None and len(haystack)>0:
                if case_sensitive_enable:
                    if needle in haystack:
                        result = True
                        break
                else:
                    if needle.lower() in haystack.lower():
                        result = True
                        break
    return result

    
min_indent = ""

def increase_indent():
    global min_indent
    min_indent+="  "
    
def decrease_indent():
    global min_indent
    if len(min_indent)>=2:
        min_indent = min_indent[:-2]

def check_coord_mismatch(file_path):
    global file_list
    global issue_count
    global module_list
    print("Running check_coord_mismatch on "+file_path+"...")
    global function_list
    if (file_path not in file_list):
        file_list.append(file_path)
    line_counting_number = 1
    ins = open(file_path, 'r')
    line = True
    global min_indent
    while line:
        line = ins.readline()
        if line:
            line_strip = line.strip()
            if (len(line_strip)>0) and (line_strip[0]!="#"):
                ao_index = line_strip.find("=")
                import_string = "import "
                from_string = "from "
                import_index = -1
                if line_strip[:len(import_string)]==import_string:
                    import_index = 0
                elif line_strip[:len(from_string)]==from_string:
                    import_string = from_string
                    import_index = line_strip.find(import_string)
                if import_index>=0:
                    module_string = line_strip[import_index+len(import_string):].strip()
                    space_index = module_string.find(" ")
                    if space_index>-1:
                        module_string = module_string[:space_index]
                    if module_string not in module_list:
                        module_list.append(module_string)
                        try:
                            #tmp_tuples = list()
                            import_string = "import "+module_string
                            exec_string = "tmp_tuples = inspect.getmembers("+module_string+", inspect.isroutine)"
                            #exec exec_string
                            try_enable = False
                            outs = open('expertmmregressiontmp.py','w')
                            outs.write("def get_module_contents():"+"\n")
                            outs_indent = "    "
                            outs.write(outs_indent+"results = None"+"\n")
                            if try_enable:
                                outs.write(outs_indent+"try:"+"\n")
                                outs_indent = "        "
                            outs.write(outs_indent+"import inspect"+"\n")
                            outs.write(outs_indent+import_string+"\n")
                            outs.write(outs_indent+exec_string+"\n")
                            outs.write(outs_indent+"results = list()"+"\n")
                            outs.write(outs_indent+"for function_tuple in tmp_tuples:"+"\n")
                            outs.write(outs_indent+"    results.append(function_tuple[0])"+"\n")
                            
                            outs_indent = "    "
                            if try_enable:
                                outs.write(outs_indent+"except:"+"\n")
                                outs_indent = "        "
                                outs.write(outs_indent+"print(\"Could not finish get_module_contents\")"+"\n")
                            outs_indent = "    "
                            outs.write(outs_indent+"return results"+"\n")
                            outs.write("\n")
                            outs.close()
                            import expertmmregressiontmp
                            tmp_list = expertmmregressiontmp.get_module_contents()
                            new_list = None
                            if tmp_list is not None:
                                new_list = list()
                                for routine_string in tmp_list:
                                    if routine_string not in function_list:
                                        new_list.append(routine_string)
                            if new_list is not None:
                                function_list += new_list
                                print("Found "+str(len(new_list))+" new method(s) from '"+module_string+"' to ignore: "+','.join(new_list))
                            else:
                                print("unable to import module named '"+module_string+"', so some routines may not be successfully ignored:")
                        except:
                            print("Could not finish importing module named '"+module_string+"', so some routines may not be successfully ignored:")
                            view_traceback()
                if ao_index<0:
                    ao_index = line_strip.find(">")
                if ao_index<0:
                    ao_index = line_strip.find("<")
                if ao_index<0:
                    ao_index = line_strip.find(" in ")
                if ao_index>0:  # intentionally >0 instead of =
                    increase_indent()
                    names_string = line_strip[:ao_index].strip()
                    values_string = line_strip[ao_index+1:].strip()
                    name_list = split_non_identifier(names_string)
                    value_list = split_non_identifier(values_string)
                    message = None
                    is_line_problematic = False
                    for regression_mismatch in regression_mismatches:
                        both_present = False
                        message_prefix = " WARNING: "
                        only_mismatched_coord_is_present_string = " ERROR (only has mismatch): "
                        if regression_mismatch.startswith_enable:
                            if (any_startswith(name_list,regression_mismatch.side_a_string) and not any_startswith(name_list,regression_mismatch.side_b_string)) and any_startswith(value_list,regression_mismatch.side_b_string):
                                name_index = line.find(regression_mismatch.side_a_string) + 1
                                if not both_present:
                                    both_present = any_startswith(value_list,regression_mismatch.side_a_string)
                                    message_prefix = only_mismatched_coord_is_present_string
                                if message is None:
                                    message = (file_path+" ("+str(line_counting_number)+","+str(name_index)+")"+message_prefix+"name starts with "+regression_mismatch.side_a_string+", but "+regression_mismatch.side_b_string+" on right in check/assignment")
                                is_line_problematic = True
                                break
                                
                            elif (any_startswith(name_list,regression_mismatch.side_b_string) and not any_startswith(name_list,regression_mismatch.side_a_string)) and any_startswith(value_list,regression_mismatch.side_a_string):
                                name_index = line.find(regression_mismatch.side_b_string) + 1
                                if not both_present:
                                    both_present = any_startswith(value_list,regression_mismatch.side_b_string)
                                    message_prefix = only_mismatched_coord_is_present_string
                                if message is None:
                                    message = (file_path+" ("+str(line_counting_number)+","+str(name_index)+")"+message_prefix+"name starts with "+regression_mismatch.side_b_string+", but "+regression_mismatch.side_a_string+" on right in check/assignment")
                                is_line_problematic = True
                                break
                        elif regression_mismatch.endswith_enable:
                            if (any_endswith(name_list,regression_mismatch.side_a_string) and not any_endswith(name_list,regression_mismatch.side_b_string)) and any_endswith(value_list,regression_mismatch.side_b_string):
                                name_index = line.find(regression_mismatch.side_a_string) + 1
                                if not both_present:
                                    both_present = any_endswith(value_list,regression_mismatch.side_a_string)
                                    message_prefix = only_mismatched_coord_is_present_string
                                if message is None:
                                    message = (file_path+" ("+str(line_counting_number)+","+str(name_index)+")"+message_prefix+"name ends with "+regression_mismatch.side_a_string+", but "+regression_mismatch.side_b_string+" on right in check/assignment")
                                is_line_problematic = True
                                break
                                
                            elif (any_endswith(name_list,regression_mismatch.side_b_string) and not any_endswith(name_list,regression_mismatch.side_a_string)) and any_endswith(value_list,regression_mismatch.side_a_string):
                                name_index = line.find(regression_mismatch.side_b_string) + 1
                                if not both_present:
                                    both_present = any_endswith(value_list,regression_mismatch.side_b_string)
                                    message_prefix = only_mismatched_coord_is_present_string
                                if message is None:
                                    message = (file_path+" ("+str(line_counting_number)+","+str(name_index)+")"+message_prefix+"name ends with "+regression_mismatch.side_b_string+", but "+regression_mismatch.side_a_string+" on right in check/assignment")
                                is_line_problematic = True
                                break
                                
                        else:
                            if (in_any_string(regression_mismatch.side_a_string, name_list) and not in_any_string(regression_mismatch.side_b_string, name_list)) and in_any_string(regression_mismatch.side_b_string, value_list):
                                value_index = line.find(regression_mismatch.side_a_string) + 1
                                if not both_present:
                                    both_present = in_any_string(regression_mismatch.side_a_string, value_list)
                                    message_prefix = only_mismatched_coord_is_present_string
                                if message is None:
                                    message = (file_path+" ("+str(line_counting_number)+","+str(value_index)+")"+message_prefix+"name contains "+regression_mismatch.side_a_string+", but "+regression_mismatch.side_b_string+" on right in check/assignment")
                                is_line_problematic = True
                                break
                            elif (in_any_string(regression_mismatch.side_b_string, name_list) and not in_any_string(regression_mismatch.side_a_string, name_list)) and in_any_string(regression_mismatch.side_a_string, value_list):
                                value_index = line.find(regression_mismatch.side_b_string) + 1
                                if not both_present:
                                    both_present = in_any_string(regression_mismatch.side_b_string, value_list)
                                    message_prefix = only_mismatched_coord_is_present_string
                                if message is None:
                                    message = (file_path+" ("+str(line_counting_number)+","+str(value_index)+")"+message_prefix+"name contains "+regression_mismatch.side_b_string+", but "+regression_mismatch.side_a_string+" on right side of check/assignment")
                                is_line_problematic = True
                                break
                    if message is not None:
                        print("")
                        print(message)
                        print(line_strip)
                    if is_line_problematic:
                        issue_count += 1
        line_counting_number += 1
    ins.close()


check_coord_mismatch("chunkymap-regen.py")
check_coord_mismatch(os.path.join("web","chunkymap.php"))
print("Found "+str(issue_count)+" issue(s) in "+str(len(file_list))+" file(s)")
raw_input("Press enter to exit...")
