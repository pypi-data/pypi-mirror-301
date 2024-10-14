import subprocess
import json
import csv
import commentjson
import os
import time
from ehdg_tools.ehdg_plotter import trial_plot, summary_plot, progress_plot
from ehdg_tools.ehdg_okn_checker import signal_checker, apply_okn_detection_rule, detect_with_okn_detector
from ehdg_tools.ehdg_updater import update_csv

color_dictionary = {
    'olive': (128, 128, 0),
    'crimson': (220, 20, 60),
    'mauve': (203, 78, 97),
    'indigo': (75, 0, 130),
    'snow': (255, 250, 250),
    'ghost white': (248, 248, 255),
    'white smoke': (245, 245, 245),
    'gainsboro': (220, 220, 220),
    'floral white': (255, 250, 240),
    'old lace': (253, 245, 230),
    'linen': (250, 240, 230),
    'antique white': (250, 235, 215),
    'papaya whip': (255, 239, 213),
    'blanched almond': (255, 235, 205),
    'bisque': (255, 228, 196),
    'peach puff': (255, 218, 185),
    'peachpuff': (255, 218, 185),
    'navajo white': (255, 222, 173),
    'moccasin': (255, 228, 181),
    'cornsilk': (255, 248, 220),
    'ivory': (255, 255, 240),
    'lemon chiffon': (255, 250, 205),
    'seashell': (255, 245, 238),
    'honeydew': (240, 255, 240),
    'mint cream': (245, 255, 250),
    'azure': (240, 255, 255),
    'alice blue': (240, 248, 255),
    'lavender': (230, 230, 250),
    'lavender blush': (255, 240, 245),
    'misty rose': (255, 228, 225),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'dark slate grey': (47, 79, 79),
    'dim grey': (105, 105, 105),
    'slate grey': (112, 128, 144),
    'light slate grey': (119, 136, 153),
    'grey': (190, 190, 190),
    'light grey': (211, 211, 211),
    'midnight blue': (25, 25, 112),
    'navy': (0, 0, 128),
    'navy blue': (0, 0, 128),
    'cornflower blue': (100, 149, 237),
    'dark slate blue': (72, 61, 139),
    'slate blue': (106, 90, 205),
    'medium slate blue': (123, 104, 238),
    'light slate blue': (132, 112, 255),
    'medium blue': (0, 0, 205),
    'royal blue': (65, 105, 225),
    'blue': (0, 0, 255),
    'dodger blue': (30, 144, 255),
    'deep sky blue': (0, 191, 255),
    'sky blue': (135, 206, 235),
    'light sky blue': (135, 206, 250),
    'steel blue': (70, 130, 180),
    'light steel blue': (176, 196, 222),
    'light blue': (173, 216, 230),
    'powder blue': (176, 224, 230),
    'pale turquoise': (175, 238, 238),
    'dark turquoise': (0, 206, 209),
    'medium turquoise': (72, 209, 204),
    'turquoise': (64, 224, 208),
    'cyan': (0, 255, 255),
    'light cyan': (224, 255, 255),
    'cadet blue': (95, 158, 160),
    'medium aquamarine': (102, 205, 170),
    'aquamarine': (127, 255, 212),
    'dark green': (0, 100, 0),
    'dark olive green': (85, 107, 47),
    'dark sea green': (143, 188, 143),
    'sea green': (46, 139, 87),
    'medium sea green': (60, 179, 113),
    'light sea green': (32, 178, 170),
    'pale green': (152, 251, 152),
    'spring green': (0, 255, 127),
    'lawn green': (124, 252, 0),
    'green': (0, 255, 0),
    'chartreuse': (127, 255, 0),
    'medium spring green': (0, 250, 154),
    'green yellow': (173, 255, 47),
    'lime green': (50, 205, 50),
    'yellow green': (154, 205, 50),
    'forest green': (34, 139, 34),
    'olive drab': (107, 142, 35),
    'dark khaki': (189, 183, 107),
    'khaki': (240, 230, 140),
    'pale goldenrod': (238, 232, 170),
    'light goldenrod yellow': (250, 250, 210),
    'light yellow': (255, 255, 224),
    'yellow': (255, 255, 0),
    'gold': (255, 215, 0),
    'light goldenrod': (238, 221, 130),
    'goldenrod': (218, 165, 32),
    'dark goldenrod': (184, 134, 11),
    'rosy brown': (188, 143, 143),
    'indian red': (205, 92, 92),
    'saddle brown': (139, 69, 19),
    'sienna': (160, 82, 45),
    'peru': (205, 133, 63),
    'burlywood': (222, 184, 135),
    'beige': (245, 245, 220),
    'wheat': (245, 222, 179),
    'sandy brown': (244, 164, 96),
    'tan': (210, 180, 140),
    'chocolate': (210, 105, 30),
    'fire brick': (178, 34, 34),
    'brown': (165, 42, 42),
    'dark salmon': (233, 150, 122),
    'salmon': (250, 128, 114),
    'light salmon': (255, 160, 122),
    'orange': (255, 165, 0),
    'dark orange': (255, 140, 0),
    'coral': (255, 127, 80),
    'light coral': (240, 128, 128),
    'tomato': (255, 99, 71),
    'orange red': (255, 69, 0),
    'red': (255, 0, 0),
    'hot pink': (255, 105, 180),
    'deep pink': (255, 20, 147),
    'pink': (255, 192, 203),
    'light pink': (255, 182, 193),
    'pale violet red': (219, 112, 147),
    'maroon': (176, 48, 96),
    'medium violet red': (199, 21, 133),
    'violet red': (208, 32, 144),
    'magenta': (255, 0, 255),
    'violet': (238, 130, 238),
    'plum': (221, 160, 221),
    'orchid': (218, 112, 214),
    'medium orchid': (186, 85, 211),
    'dark orchid': (153, 50, 204),
    'dark violet': (148, 0, 211),
    'blue violet': (138, 43, 226),
    'purple': (160, 32, 240),
    'medium purple': (147, 112, 219),
    'thistle': (216, 191, 216),
    'dark grey': (169, 169, 169),
    'dark blue': (0, 0, 139),
    'dark cyan': (0, 139, 139),
    'dark magenta': (139, 0, 139),
    'dark red': (139, 0, 0),
    'light green': (144, 238, 144),
}


# check whether there is input commandline program or not
def check_commandline_program(program_name):
    check_cmd = f"{program_name} --version"
    try:
        check_output = subprocess.check_output(check_cmd, shell=True)
        check_output = check_output.decode('utf-8')
        print(check_output)
        is_there_program = True
        print(f"{program_name} is found.")
    except Exception as error:
        print(error)
        is_there_program = False
    return is_there_program


# This function is to change color string to color bgr tuple value
def string_to_bgr_tuple(input_string):
    input_string = str(input_string).lower()
    try:
        rgb_tuple = color_dictionary[input_string]
        red_index = rgb_tuple[0]
        green_index = rgb_tuple[1]
        blue_index = rgb_tuple[2]
        return blue_index, green_index, red_index
    except IndexError:
        print(f"Input string {input_string} is not a valid color string input.")
        print("It can be red, green, blue, black, white or magenta.")
        print("It also can be hex color code.")
        raise ValueError(f"Input string {input_string} is not a valid color string input.")


# This function is to change hex color string to color bgr tuple value
def hex_string_to_bgr_tuple(input_string):
    input_string = str(input_string).lower()
    if "#" in input_string:
        value = input_string.lstrip('#')
        lv = len(value)
        if lv == 6:
            try:
                tem_arr = tuple(int(value[xx:xx + lv // 3], 16) for xx in range(0, lv, lv // 3))
                return tem_arr[::-1]
            except ValueError as e:
                print(e)
                raise
        else:
            print(f"The length of input hex string must be 6 character. But it is {lv}.")
            raise ValueError(f"Input string {input_string} is not a valid hex string.")
    else:
        raise ValueError(f"Input string {input_string} must contain #.")


# This function is to translate disk condition string to logmar value
def convert_disk_to_logmar(disk_string_input):
    disk_logmar_equivalent = {"disk-condition-1-1": 1.0, "disk-condition-1-2": 1.0, "disk-condition-2-1": 0.9,
                              "disk-condition-2-2": 0.9, "disk-condition-3-1": 0.8, "disk-condition-3-2": 0.8,
                              "disk-condition-4-1": 0.7, "disk-condition-4-2": 0.7, "disk-condition-5-1": 0.6,
                              "disk-condition-5-2": 0.6, "disk-condition-6-1": 0.5, "disk-condition-6-2": 0.5,
                              "disk-condition-7-1": 0.4, "disk-condition-7-2": 0.4, "disk-condition-8-1": 0.3,
                              "disk-condition-8-2": 0.3, "disk-condition-9-1": 0.2, "disk-condition-9-2": 0.2,
                              "disk-condition-10-1": 0.1, "disk-condition-10-2": 0.1, "disk-condition-11-1": 0.0,
                              "disk-condition-11-2": 0.0, "disk-condition-12-1": -0.1, "disk-condition-12-2": -0.1,
                              "disk-condition-13-1": -0.2, "disk-condition-13-2": -0.2}

    try:
        out_string = disk_logmar_equivalent[disk_string_input]
        convertable = True
    except KeyError:
        out_string = disk_string_input
        convertable = False

    return convertable, out_string


# This function is to write the json as a file with given indent to read easily
def write_json_with_ident(jason_input, output_dir, indent_input=4):
    # Serializing json
    json_object = json.dumps(jason_input, indent=indent_input)

    # Writing to sample.json
    with open(output_dir, "w") as outfile:
        outfile.write(json_object)


def get_info_from_csv(csv_dir_input):
    header_array_out = []
    rows_out = []
    try:
        file_to_open = open(csv_dir_input)
        csv_reader = csv.reader(file_to_open)

        count_one = 0
        for row_data in csv_reader:
            if count_one <= 0:
                header_array_out = row_data
                count_one += 1
            else:
                rows_out.append(row_data)
    except FileNotFoundError:
        print(f"{csv_dir_input} could not be found.")

    return header_array_out, rows_out


def get_index(search_input, array_in, print_string=True):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(array_in):
        if val == search_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        if print_string:
            print(f"//{search_input} can not be found!")

    return return_idx


def load_commented_json(config_input):
    with open(config_input, 'r') as handle:
        protocol = commentjson.load(handle)
    return protocol


# This function is to retrieve the value from dictionary
# If it is invalid, then it will return None
def try_and_get_value(dict_input, key_input, print_string=True, accept_exception=False):
    try:
        output_value = dict_input[key_input]
    except Exception as error:
        output_value = None
        error_string = f"{type(error).__name__}"
        if print_string:
            if accept_exception:
                pass
            else:
                print(f"//WARNING:Key:\"{key_input}\" could not retrieve from given dictionary due to {error_string}.")

    return output_value


def get_dict_from_csv(csv_input):
    header_array, rows = get_info_from_csv(csv_input)

    dict_array = []
    for row in rows:
        temp_dict = {}
        for header in header_array:
            header_position = get_index(header, header_array)
            temp_dict[header] = row[header_position]
        dict_array.append(temp_dict)

    return dict_array


def fix_direction_in_dict_array(dict_array_in, reverse_direction=False):
    for record_data in dict_array_in:
        try:
            record_direction = int(record_data["direction"])
        except ValueError:
            record_direction = 1
        except KeyError:
            record_direction = 1
        except TypeError:
            record_direction = 1
        if record_direction == 1 or record_direction == -1:
            pass
        else:
            record_direction = 1
        if reverse_direction:
            rev_d = int(record_direction * -1)
            record_data["direction"] = rev_d
        else:
            record_data["direction"] = record_direction

    return dict_array_in


def get_start_end_info(gaze_csv_input, reverse_direction=False):
    recording_data_dict_array = get_dict_from_csv(gaze_csv_input)
    recording_data_dict_array = fix_direction_in_dict_array(recording_data_dict_array,
                                                            reverse_direction=reverse_direction)
    trials_start_end_raw_info_array = []
    start_info = None
    start_index = None
    trial_id = None
    disk_condition = None
    trial_event_id = None
    temp_info_dict = None
    temp_event_id = 0
    for ind, record_data in enumerate(recording_data_dict_array):
        event_string = record_data["event_string"]
        if event_string != " ":
            temp_event_id += 1
            try:
                temp_dict = json.loads(event_string)
            except json.decoder.JSONDecodeError:
                temp_dict = None
            if temp_dict:
                try:
                    trial_type = temp_dict["trial_type"]
                except KeyError:
                    trial_type = None
                if trial_type is not None and trial_type != "animation":
                    if temp_dict["type"] == "start_marker":
                        start_info = record_data
                        start_index = ind
                        trial_id = temp_dict["trial_id"]
                        disk_condition = temp_dict["trial_index"]
                        temp_info_dict = temp_dict
                        try:
                            trial_event_id = temp_dict["event_id"]
                        except KeyError:
                            trial_event_id = temp_event_id
                    else:
                        end_info = record_data
                        end_index = ind
                        if start_info is not None and start_index is not None \
                                and trial_id is not None and disk_condition is not None \
                                and trial_event_id is not None and temp_info_dict is not None:
                            t_dict = {}
                            t_dict["start_info"] = start_info
                            t_dict["start_index"] = start_index
                            t_dict["end_info"] = end_info
                            t_dict["end_index"] = end_index
                            t_dict["info_dict"] = temp_info_dict
                            t_dict["trial_id"] = trial_id
                            t_dict["disk_condition"] = disk_condition
                            t_dict["event_id"] = trial_event_id
                            trials_start_end_raw_info_array.append(t_dict)
                        else:
                            raise ValueError(f"Incorrect order of event marker in from gaze csv : {gaze_csv_input}.")

    return trials_start_end_raw_info_array, recording_data_dict_array


def create_trial_csv(out_dir_input, start_end_info_input, record_data_array_input, header_array):
    trial_id = start_end_info_input["trial_id"]
    disk_condition = start_end_info_input["disk_condition"]
    start_index = start_end_info_input["start_index"]
    end_index = start_end_info_input["end_index"]
    event_id = start_end_info_input["event_id"]
    array_to_be_used = record_data_array_input[start_index:end_index + 1]
    trial_name = f"{trial_id}_{disk_condition}"
    trial_folder_dir = os.path.join(out_dir_input, trial_name)
    if not os.path.isdir(trial_folder_dir):
        os.mkdir(trial_folder_dir)
    trial_csv_dir = os.path.join(trial_folder_dir, f"{trial_name}.csv")

    first_record_timestamp = None
    with open(trial_csv_dir, mode='w', newline="") as destination_file:
        csv_writer = csv.DictWriter(destination_file, fieldnames=header_array)
        csv_writer.writeheader()
        for data_dict in array_to_be_used:
            is_event = data_dict["is_event"]
            if str(is_event).lower() == "true":
                is_event = 1
            else:
                is_event = 0
            data_dict["is_event"] = is_event
            data_dict["event_id"] = event_id
            del data_dict["event_string"]
            record_timestamp = data_dict["record_timestamp"]
            if first_record_timestamp is None:
                first_record_timestamp = record_timestamp
            record_timestamp = float(record_timestamp) - float(first_record_timestamp)
            data_dict["record_timestamp"] = record_timestamp
            csv_writer.writerow(data_dict)
        destination_file.close()
    return trial_csv_dir, trial_folder_dir


# This function is to record trial info into the given csv file
def record_result(dir_input, signal_data_input,
                  sptrack_input, sp_long_limit_input,
                  min_chain_length_input, min_unchained_okn_input,
                  okn_boolean_input, trial_id_input, disk_condition_input,
                  logmar_level_input, description_input,
                  event_id, direction):
    start_time = time.time()
    max_chain_length_signal_data = signal_data_input["max_chain_length"]
    unchained_okn_total_signal_data = signal_data_input["unchained_okn_total"]
    try:
        max_sp_duration = signal_data_input["max_sp_duration"]
    except KeyError:
        max_sp_duration = "None"
    except TypeError:
        max_sp_duration = "None"

    if sp_long_limit_input is None:
        sp_long_limit_input = "None"

    if okn_boolean_input:
        okn_matlab = 1
    else:
        okn_matlab = 0
    header_names = ["trial_id", "disk_condition", "event_id", "logmar_level", "description",
                    "direction", "sptrack", "sp_long_limit", "min_chain_length_rule", "min_unchained_okn_rule",
                    "max_chain_length_signal_data", "unchained_okn_total_signal_data", "max_sp_duration",
                    "okn", "okn_matlab", "final_va"]
    print(f"OKN detector summary csv directory: {dir_input}")
    file_exists = os.path.exists(dir_input)
    if file_exists:
        with open(dir_input, mode='a+', newline="") as destination_file:
            csv_writer = csv.writer(destination_file)
            csv_writer.writerow(
                [trial_id_input, disk_condition_input, event_id, logmar_level_input,
                 description_input, direction, sptrack_input, sp_long_limit_input,
                 min_chain_length_input, min_unchained_okn_input, max_chain_length_signal_data,
                 unchained_okn_total_signal_data, max_sp_duration, okn_boolean_input,
                 okn_matlab, " "])
            destination_file.close()
    else:
        with open(dir_input, mode='w', newline="") as new_destination_file:
            csv_writer = csv.DictWriter(new_destination_file, fieldnames=header_names)
            csv_writer.writeheader()
            csv_writer.writerow({"trial_id": trial_id_input, "disk_condition": disk_condition_input,
                                 "event_id": event_id, "logmar_level": logmar_level_input,
                                 "description": description_input, "direction": direction,
                                 "sptrack": sptrack_input, "sp_long_limit": sp_long_limit_input,
                                 "min_chain_length_rule": min_chain_length_input,
                                 "min_unchained_okn_rule": min_unchained_okn_input,
                                 "max_chain_length_signal_data": max_chain_length_signal_data,
                                 "unchained_okn_total_signal_data": unchained_okn_total_signal_data,
                                 "max_sp_duration": max_sp_duration, "okn": okn_boolean_input,
                                 "okn_matlab": okn_matlab, "final_va": " "})
            new_destination_file.close()

    print(f"Result is recorded in this directory: {dir_input}")
    print(f"It took {time.time() - start_time} sec.")
    print("--------------------------------------------------------------------------------------")


# This function is to record final in the okn detector summary csv
def record_final_va(summary_csv_dir, logmar_level_header_input, final_va_header_input):
    file_exists = os.path.exists(summary_csv_dir)
    error_string = None
    if file_exists:
        try:
            file_to_open = open(summary_csv_dir)
            csv_reader = csv.reader(file_to_open)
            header_array = []
            rows = []
            count_one = 0
            for row in csv_reader:
                if count_one <= 0:
                    header_array = row
                    count_one += 1
                else:
                    rows.append(row)
        except FileNotFoundError:
            error_string = f"{summary_csv_dir} could not be found."
            rows = []
            header_array = None

        if len(rows) > 0:
            last_row_index = len(rows) - 1
            last_row = rows[last_row_index]
            logmar_level_position = get_index(logmar_level_header_input, header_array)
            final_va_position = get_index(final_va_header_input, header_array)
            final_va_logmar = last_row[logmar_level_position]
            rows[last_row_index][final_va_position] = final_va_logmar
            with open(summary_csv_dir, mode='w', newline="") as destination_file:
                csv_writer = csv.DictWriter(destination_file, fieldnames=header_array)
                csv_writer.writeheader()
                for row in rows:
                    row_dict = {}
                    for ind, value in enumerate(row):
                        row_dict[header_array[ind]] = value
                    csv_writer.writerow(row_dict)
                destination_file.close()
        else:
            error_string = f"There is no data in {summary_csv_dir} or it does not exist."
            print(error_string)
    else:
        error_string = f"File:{summary_csv_dir} does not exist."
        print(error_string)

    return error_string


# This function is to convert gaze.csv to trials folder with all the data inside
# tpi = trial plot info
# spi = summary plot info, ppi = progress plot info
# ucl = updater config location, dcl = detector config location
# mcl = min_chain_length, muo = min_unchained_okn,
# tha = trial header array
# esfuc = extra_string_for_updated_csv
def convert_gaze_csv_to_trials(gaze_csv_input, output_folder_name,
                               tpi, spi, ppi, ucl, dcl,
                               mcl, muo, sll, esfuc, tha,
                               use_disk_to_logmar=False,
                               reverse_direction=False,
                               output_folder_dir=None):
    if output_folder_dir is None:
        gaze_base_name = os.path.basename(gaze_csv_input)
        output_folder_dir = str(gaze_csv_input).replace(gaze_base_name, output_folder_name)

    if not os.path.isdir(output_folder_dir):
        os.mkdir(output_folder_dir)
    print(f"Output folder : {output_folder_dir} will be used in convert_gaze_csv_to_trials.")

    summary_csv_name_for_final_va = spi["summary_csv_name"]
    summary_csv_dir = os.path.join(output_folder_dir, summary_csv_name_for_final_va)
    summary_csv_exists = os.path.isfile(summary_csv_dir)
    if summary_csv_exists:
        os.remove(summary_csv_dir)

    start_end_info_array, record_data_array = get_start_end_info(gaze_csv_input,
                                                                 reverse_direction=reverse_direction)
    # for rr in start_end_info_array:
    #     print(rr["info_dict"])

    for start_end_info in start_end_info_array:
        trial_id = start_end_info["trial_id"]
        disk_condition = start_end_info["disk_condition"]
        info_dict = start_end_info["info_dict"]
        try:
            logmar_level = info_dict["logmar_level"]
        except KeyError:
            if use_disk_to_logmar:
                cv, ll = convert_disk_to_logmar(disk_condition)
                logmar_level = ll
            else:
                logmar_level = "undefined"
        except TypeError:
            if use_disk_to_logmar:
                cv, ll = convert_disk_to_logmar(disk_condition)
                logmar_level = ll
            else:
                logmar_level = "undefined"
        try:
            description = info_dict["description"]
        except KeyError:
            description = logmar_level
        except TypeError:
            description = logmar_level
        event_id = start_end_info["event_id"]
        try:
            direction = int(info_dict["trial_direction"])
        except ValueError:
            direction = "undefined"
        except KeyError:
            direction = "undefined"
        except TypeError:
            direction = "undefined"
        trial_csv_dir, trial_folder_dir = create_trial_csv(output_folder_dir, start_end_info, record_data_array, tha)
        updated_csv_dir = update_csv(trial_csv_dir, esfuc, ucl)
        updated_csv_exists = os.path.isfile(updated_csv_dir)
        if updated_csv_exists:
            is_there_detector = check_commandline_program("okndetector")
            if is_there_detector:
                output_signal_dir = detect_with_okn_detector(updated_csv_dir, dcl)
            else:
                raise FileNotFoundError("OKN detector cannot be found.")
        else:
            raise FileNotFoundError("Updated trial csv does not exist.")

        if sll is None:
            signal_data = signal_checker(output_signal_dir, sp_track_column_name=None)
        else:
            signal_data = signal_checker(output_signal_dir)

        is_there_okn = apply_okn_detection_rule(signal_data, mcl, muo, min_sp_duration=sll)
        signal_csv_name = tpi["signal_csv_name"]
        signal_csv_dir = os.path.join(output_signal_dir, signal_csv_name)
        trial_plot(tpi, signal_csv_dir)
        sum_csv_name = spi["summary_csv_name"]
        sum_csv_dir = os.path.join(output_folder_dir, sum_csv_name)

        if sll is None:
            sptrack = False
        else:
            sptrack = True

        record_result(sum_csv_dir, signal_data, sptrack, sll, mcl, muo, is_there_okn, trial_id,
                      disk_condition, logmar_level, description, event_id, direction)

    progress_plot_trial_summary_csv_name = ppi["trial_summary_csv_name"]
    trial_data_csv_dir = os.path.join(output_folder_dir, progress_plot_trial_summary_csv_name)

    is_sweep = True if "sweep" in str(output_folder_dir) else False
    if is_sweep:
        max_row = 2
    else:
        max_row = None
    summary_plot(output_folder_dir, spi, max_graph_in_a_row_input=max_row, is_sweep=is_sweep)
    trial_data_csv_exists = os.path.isfile(trial_data_csv_dir)
    if trial_data_csv_exists:
        progress_plot(output_folder_dir, ppi)
        summary_csv_exists = os.path.isfile(summary_csv_dir)
        if summary_csv_exists:
            error_str = record_final_va(summary_csv_dir,
                                        "logmar_level",
                                        "final_va")
            if error_str is not None:
                print(str(error_str))
        else:
            print("Summary csv could not be found.")
