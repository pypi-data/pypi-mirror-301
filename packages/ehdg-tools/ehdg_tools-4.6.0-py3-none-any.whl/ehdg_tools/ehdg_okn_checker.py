import os
import csv
import time


# This function is to get header position from the given array
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


# This function is to retrieve the value from dictionary
# If it is invalid, then it will return None
def try_and_get_value(dict_input, key_input, print_string=True):
    try:
        output_value = dict_input[key_input]
    except Exception as error:
        output_value = None
        error_string = f"{type(error).__name__}"
        if print_string:
            print(f"//WARNING:Key:\"{key_input}\" could not retrieve from config: {dict_input} due to {error_string}.")

    return output_value


def read_signal_csv(input_file_dir, print_string=True):
    file = open(input_file_dir)
    csv_reader = csv.reader(file)
    header_array = []
    rows = []
    count_one = 0

    for row in csv_reader:
        if count_one <= 0:
            header_array = row
            count_one += 1
        else:
            rows.append(row)

    dict_array = []
    for row in rows:
        temp_dict = {}
        for header in header_array:
            header_position = get_index(header, header_array, print_string)
            temp_dict[header] = row[header_position]
        dict_array.append(temp_dict)

    return dict_array


def read_signal_csv_old_way(input_file_dir1, print_string=True):
    file1 = open(input_file_dir1)
    csv_reader = csv.reader(file1)
    header_array = []
    rows = []
    data_table_dict = {}
    count_one = 0

    for row in csv_reader:
        if count_one <= 0:
            header_array = row
            count_one += 1
        else:
            rows.append(row)

    for header in header_array:
        header_position = get_index(header, header_array, print_string)
        value_array = []
        for row in rows:
            value_array.append(row[header_position])
        data_table_dict[header] = value_array

    return data_table_dict


# This function is to read the signal.csv and retrieve max chain length and unchained okn total
# If the signal csv name is None, dir_input will be used as main signal csv dir
def signal_checker(dir_input, signal_csv_name="signal.csv",
                   print_string=True, sp_track_column_name="is_sptrack"):
    if sp_track_column_name is None:
        if print_string:
            print(f"//Warning: sp_track_column_name is None!")
            print(f"//Therefore using retrieve signal data with old way.")
        if print_string:
            print(f"//Sending the following directory: {dir_input} to signal checker!")
        start_time = time.time()

        if signal_csv_name is None:
            # using direct directory
            csv_input = dir_input
        else:
            # Add signal.csv to directory
            csv_input = os.path.join(dir_input, signal_csv_name)

        data_table = read_signal_csv_old_way(csv_input, print_string)
        result_id_array = data_table["result_id"]
        result_chain_id_array = data_table["result_chain_id"]
        signal_data = {}
        result_data = []
        temp_max_chain_length = 0
        temp_unchained_okn_total = 0

        # Looking for result id and result chain id.
        # When they are found, they are added into result data array
        for r_id, r_c_id in zip(result_id_array, result_chain_id_array):
            if int(r_id) != -1 and int(r_c_id) != -1:
                result_data.append((int(r_c_id), int(r_id)))

        # remove duplicate number from result data array
        unique_result_data = list(dict.fromkeys(result_data))
        # print(unique_result_data)

        # taking only result id
        raw_unique_result_id_array = []
        for ri in unique_result_data:
            raw_unique_result_id_array.append(ri[0])

        # remove duplicate result id from raw unique result id array
        unique_result_id_array = list(dict.fromkeys(raw_unique_result_id_array))

        final_data_array = []

        # looping unique result id array to get all result chain id which are
        # related to their individual result id into temp array
        # after that, add result id and its related result chain id into final data array as a tuple
        for rid in unique_result_id_array:
            temp_array = []
            for data in unique_result_data:
                if rid == data[0]:
                    temp_array.append(data[1])
            final_data_array.append((rid, temp_array))

        # determine the max chain length and unchained okn total from final data array
        if len(final_data_array) > 0:
            if print_string:
                print(f"//Raw result: {final_data_array}")
            for tuple_item in final_data_array:
                chain_length = len(tuple_item[1])
                if chain_length > temp_max_chain_length:
                    temp_max_chain_length = chain_length
                if chain_length == 1:
                    temp_unchained_okn_total += 1
            signal_data["max_chain_length"] = temp_max_chain_length
            signal_data["unchained_okn_total"] = temp_unchained_okn_total
        else:
            if print_string:
                print("//There is no chain or okn")
            signal_data["max_chain_length"] = 0
            signal_data["unchained_okn_total"] = 0

        if print_string:
            print(f"//Signal data: {signal_data} is collected and it took {time.time() - start_time} sec.")
            print("//--------------------------------------------------------------------------------------")

        return signal_data
    else:
        if print_string:
            print(f"//Sending the following directory: {dir_input} to signal checker!")
        start_time = time.time()

        if signal_csv_name is None:
            # using direct directory
            csv_input = dir_input
        else:
            # Add signal.csv to directory
            csv_input = os.path.join(dir_input, signal_csv_name)

        data_dict_array = read_signal_csv(csv_input, print_string)
        # reverse_data_dict_array = list(reversed(data_dict_array))
        # result_id_array = data_table["result_id"]
        # result_chain_id_array = data_table["result_chain_id"]
        signal_data = {}
        result_data_array = []
        unique_id = None
        previous_dict = None
        sp_track_start = False

        for data_index, data_dict in enumerate(data_dict_array):
            result_id = data_dict["result_id"]
            result_chain_id = data_dict["result_chain_id"]
            state = data_dict["state"]
            sp_duration = data_dict["sp_duration"]
            is_sptrack = try_and_get_value(data_dict, sp_track_column_name)
            row_id = data_dict["id"]
            temp_dict = {}
            unique_id_to_check = f"{result_chain_id}_{result_id}_{state}"
            if unique_id_to_check != unique_id:
                unique_id = unique_id_to_check
                if previous_dict is not None:
                    result_data_array.append(previous_dict)
            temp_dict["id"] = unique_id
            temp_dict["result_chain_id"] = result_chain_id
            temp_dict["result_id"] = result_id
            temp_dict["state"] = state
            temp_dict["sp_duration"] = sp_duration
            temp_dict["is_sptrack"] = is_sptrack
            temp_dict["row_id"] = row_id
            if str(is_sptrack).lower() == "true":
                if not sp_track_start:
                    sp_track_start = True
                    sptrack_dict = {**temp_dict}
                    sptrack_dict["id"] = f"{unique_id}_sptrack_start"
                    result_data_array.append(sptrack_dict)
                else:
                    if data_index == (len(data_dict_array) - 1):
                        sptrack_dict = {**temp_dict}
                        sptrack_dict["id"] = f"{unique_id}_sptrack_end"
                        result_data_array.append(sptrack_dict)
            else:
                if sp_track_start:
                    sp_track_start = False
                    sptrack_dict = {**previous_dict}
                    temp_result_id = sptrack_dict["result_id"]
                    temp_result_chain_id = sptrack_dict["result_chain_id"]
                    temp_state = sptrack_dict["state"]
                    temp_unique_id = f"{temp_result_chain_id}_{temp_result_id}_{temp_state}"
                    sptrack_dict["id"] = f"{temp_unique_id}_sptrack_end"
                    result_data_array.append(sptrack_dict)
            previous_dict = temp_dict
            if data_index == (len(data_dict_array) - 1):
                result_data_array.append(previous_dict)

        # For testing
        # for dd in result_data_array:
        #     print(dd)
        # print("-----------------------------------------------------------------------")

        final_info_dict = {}
        isolated_sptrack_num = 0
        for dd in result_data_array:
            result_chain_id = dd["result_chain_id"]
            result_id = dd["result_id"]
            sp_duration = dd["sp_duration"]
            is_sptrack = dd["is_sptrack"]
            data_id = dd["id"]
            if result_chain_id == "-1":
                if str(is_sptrack).lower() == "true":
                    if "sptrack_end" in str(data_id):
                        # print(f"====>{dd}")
                        isolated_sptrack_num += 1
                        info_id = f"isolated_sptrack_{isolated_sptrack_num}"
                        temp_dict = {}
                        temp_dict["id"] = info_id
                        temp_dict["result_chain_id"] = f"iso_{isolated_sptrack_num}"
                        temp_dict["result_id"] = result_id
                        temp_dict["sp_duration"] = sp_duration
                        final_info_dict[info_id] = temp_dict
            else:
                check_id = f"{result_chain_id}_{result_id}_IN_SP"
                if data_id == check_id:
                    temp_dict = {}
                    info_id = f"{result_chain_id}_{result_id}"
                    temp_dict["id"] = info_id
                    temp_dict["result_chain_id"] = result_chain_id
                    temp_dict["result_id"] = result_id
                    temp_dict["sp_duration"] = sp_duration
                    final_info_dict[info_id] = temp_dict

        max_sp_duration = 0
        raw_unique_chain_id_array = []

        for id_string in final_info_dict:
            d_dict = final_info_dict[id_string]
            # print(d_dict)
            result_chain_id = d_dict["result_chain_id"]
            sp_duration = float(d_dict["sp_duration"])
            raw_unique_chain_id_array.append(result_chain_id)
            if sp_duration >= max_sp_duration:
                max_sp_duration = sp_duration

        unique_chain_id_array = list(dict.fromkeys(raw_unique_chain_id_array))

        # print(unique_chain_id_array)

        final_data_array = []

        # looping unique result id array to get all result chain id which are
        # related to their individual result id into temp array
        # after that, add result id and its related result chain id into final data array as a tuple
        for chain_id in unique_chain_id_array:
            t_array = []
            for key_string in final_info_dict:
                i_dict = final_info_dict[key_string]
                rci = i_dict["result_chain_id"]
                ri = i_dict["result_id"]
                if chain_id == rci:
                    t_array.append(ri)
            final_data_array.append((chain_id, t_array))

        # print(final_data_array)

        temp_max_chain_length = 0
        temp_unchained_okn_total = 0

        # determine the max chain length and unchained okn total from final data array
        if len(final_data_array) > 0:
            if print_string:
                print(f"//Raw result: {final_data_array}")
            for tuple_item in final_data_array:
                chain_length = len(tuple_item[1])
                if chain_length > temp_max_chain_length:
                    temp_max_chain_length = chain_length
                if chain_length == 1:
                    temp_unchained_okn_total += 1
            signal_data["max_chain_length"] = temp_max_chain_length
            signal_data["unchained_okn_total"] = temp_unchained_okn_total
        else:
            if print_string:
                print("//There is no chain or okn")
            signal_data["max_chain_length"] = 0
            signal_data["unchained_okn_total"] = 0

        signal_data["max_sp_duration"] = float(max_sp_duration)

        if print_string:
            print("//Checking whether there is slow phase track column or not.")

        if print_string:
            print(f"//Signal data: {signal_data} is collected and it took {time.time() - start_time} sec.")
            print("//--------------------------------------------------------------------------------------")

        return signal_data


# This function is to decide whether there is okn or not by the given rules
def apply_okn_detection_rule(data, min_chain_length_input, min_unchained_okn_input,
                             min_sp_duration=None, print_string=True):
    if print_string:
        print(f"//Start applying the okn detection rule.")
        print(f"//Minimum chain length must be greater than equal {min_chain_length_input}.")
        print(f"//Minimum unchained okn must be greater than equal {min_unchained_okn_input}.")
        if min_sp_duration is not None:
            print(f"//Slow phase duration must be greater than equal {min_sp_duration}.")
    start_time = time.time()

    if min_sp_duration is not None:
        top_rule = (data["max_sp_duration"] >= min_sp_duration)
    else:
        top_rule = False

    if top_rule:
        if print_string:
            print("//There is an valid okn because it has long slow phase!")
        valid_okn = True
    else:
        # Rule 1
        is_chained = (data["max_chain_length"] >= min_chain_length_input)

        # Rule 2
        is_unchained = (data["unchained_okn_total"] >= min_unchained_okn_input)

        valid_okn = is_chained | is_unchained
        if print_string:
            print(f"//Data:{data} has been measured by okn detection rules!")
        if valid_okn:
            if print_string:
                print("//There is an valid okn according to the rules!")
        else:
            if print_string:
                print("//There is no valid okn!")
    if print_string:
        print(f"//The process took {time.time() - start_time} sec.")
        print("//--------------------------------------------------------------------------------------")

    return valid_okn


# This function is to detect okn from the given preprocessed csv and produce result folder which includes signal.csv
def detect_with_okn_detector(csv_to_b_detected, odc):
    start_time = time.time()
    print(f"Sending the following directory to okn detector: {csv_to_b_detected}!")
    updated_filename = os.path.basename(csv_to_b_detected)
    out_put_dir = csv_to_b_detected.replace(updated_filename, "result")

    if not os.path.isfile(odc):
        raise FileNotFoundError("OKN detector config file cannot be found.")

    commandline = f"okndetector -c \"{odc}\" -i \"{csv_to_b_detected}\" -o \"{out_put_dir}\""
    os.system(commandline)
    print(f"The result has been produced in the directory {out_put_dir}.")
    print(f"The process took {time.time() - start_time} sec.")
    print("--------------------------------------------------------------------------------------")

    return out_put_dir
