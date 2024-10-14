from typing import Literal, Union, Any
from pathlib import Path
import pandas as pd

def filesize_in_folder(
        folder_path: Union[str, Path],
        unit: Literal["byte","KB","MB","GB","TB"] = "KB"
        ) -> pd.DataFrame:
    """
    Calculate the size of files in a folder and their proportion relative to the total size.

    Parameters:
    - folder_path (str or Path): Path to the folder.

    Returns:
    - pd.DataFrame: DataFrame with 'filesize' and 'filesize_prop' columns.
    """
    # solo from o1 seems pretty accurate medium tested, becareful when check with file system
    # this reconcile well with WinDirStat
    
    if unit in ["byte"]:
        unit_divider = 1
    elif unit in ["KB"]:
        unit_divider = 1000
    elif unit in ["MB"]:
        unit_divider = 1000**3
    elif unit in ["GB"]:
        unit_divider = 1000**6
    elif unit in ["TB"]:
        unit_divider = 1000**9

    folder_path = Path(folder_path)
    # Get all items in the folder (non-recursive)
    items = list(folder_path.iterdir())
    data = []
    for item in items:
        if item.is_file():
            size = item.stat().st_size  # File size in bytes
            size_scaled = size / unit_divider
            data.append({'item_name': item.name, 'filesize': size_scaled})
        elif item.is_dir():
            # Calculate total size of all files in the directory recursively
            size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
            size_scaled = size / unit_divider
            data.append({'item_name': item.name, 'filesize': size_scaled})
        else:
            # Handle other file types if necessary
            data.append({'item_name': item.name, 'filesize': 0})
    df = pd.DataFrame(data)
    total_size = df['filesize'].sum()
    df['filesize_prop'] = df['filesize'] / total_size if total_size > 0 else 0

    return df

def delete_files_in_folder(folder_path: Path|str,verbose = 1):
    # medium tested
    import os
    # Ensure the folder path is a Path object
    folder_path = Path(folder_path)
    
    # Check if the folder exists
    if not folder_path.exists():
        raise Exception(f"The path {folder_path} does not exist.")

    
    # Check if the path is a directory
    if not folder_path.is_dir():
        raise Exception(f"The path {folder_path} is not a directory.")
    
    # Iterate through files in the directory
    for filename in os.listdir(folder_path):
        file_path = folder_path / filename
        
        # Check if it's a file and remove it
        if file_path.is_file():
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

def extract_folder_structure(
        root_folder: Path |str) -> dict[Any]:
    """
    Extract the structure of a folder as dictionary representation.

    Parameters
    ----------
    root_folder : path-like
        The path to the root folder to extract the structure from.

    Returns
    -------
    structure : dict
        A dictionary with the subfolders as keys and their structures as values.
        If the subfolders do not have any subfolders, they are represented as a list.
    """
    # medium tested
    # solo from o1 as of Oct 14, 2024
    import os
    root_folder = os.path.abspath(root_folder)
    entries = os.listdir(root_folder)
    # Get the list of immediate subdirectories
    subdirs = [entry for entry in entries if os.path.isdir(os.path.join(root_folder, entry))]
    if not subdirs:
        # If there are no subdirectories, return None
        return None
    else:
        subdir_structures = {}
        all_subdirs_none = True
        for subdir in subdirs:
            subdir_path = os.path.join(root_folder, subdir)
            # Recursively extract the structure of each subdirectory
            subdir_structure = extract_folder_structure(subdir_path)
            subdir_structures[subdir] = subdir_structure
            if subdir_structure is not None:
                all_subdirs_none = False
        if all_subdirs_none:
            # If all subdirectories have no further subdirectories, represent them as a list
            return list(subdir_structures.keys())
        else:
            # Otherwise, represent them as a dictionary
            return subdir_structures


def create_folder_structure(
        root_folder: Path |str, 
        structure: dict[Any]) -> None:
    """
    create folder structure from dictionary
    allow final level to be a list

    structure_example = {
    "Portuguese": {
        "Westworld Portuguese": {
            "Westworld Portugues 01": None,
            "Westworld Portugues 02": ["folder1", "folder2"],
            "Westworld Portugues 03": None,
            "Westworld Portugues 04": None,
        },
        "BigBang Portuguese": [
            "BigBang PT Season 01",
            "BigBang PT Season 02",
            "BigBang PT Season 03",
            "BigBang PT Season 04",
            "BigBang PT Season 05",
            "BigBang PT Season 06",
            "BigBang PT Season 07",
            "BigBang PT Season 08",
            "BigBang PT Season 09",
            "BigBang PT Season 10",
            "BigBang PT Season 11",
        ],
        "The 100 PT": {
            "The 100 Season 01 Portuguese": None,
            "The 100 Season 02 Portuguese": None,
            "The 100 Season 03 Portuguese": None,
            "The 100 Season 04 Portuguese": None,
            "The 100 Season 05 Portuguese": None,
                        },
                    }
                }
    
    """
    import os
    # medium tested(pass 1 shot)
    if isinstance(structure, dict):
        for folder_name, subfolders in structure.items():
            # Construct the full path for the current folder
            current_folder = os.path.join(root_folder, folder_name)
            # Create the current folder if it doesn't exist
            os.makedirs(current_folder, exist_ok=True)
            # Recursively create subfolders
            create_folder_structure(current_folder, subfolders)
    elif isinstance(structure, list):
        for folder_name in structure:
            current_folder = os.path.join(root_folder, folder_name)
            os.makedirs(current_folder, exist_ok=True)
            # Since list items are considered final, you can decide whether to allow further nesting
            # For this example, we'll assume no further nesting
    elif structure is None:
        # No subfolders to create
        pass
    else:
        raise ValueError(f"Unsupported structure type: {type(structure)} for {root_folder}")


def print_folder_structure(startpath: Path | str, indent='│   ', verbose=1, include_only_folder=False):
    # by ChatGPT 4o as of Oct, 14, 2024(2-3 attempts)
    import os
    result = []  # To store the folder structure as text

    # Convert to Path object if it's a string
    startpath = Path(startpath) if isinstance(startpath, str) else startpath
    
    for root, dirs, files in os.walk(startpath):
        level = root.replace(str(startpath), '').count(os.sep)
        indent_space = indent * level  # Now using the custom `indent` value for spacing
        
        # Sort folder names
        dirs.sort()
        folder_name = os.path.basename(root)
        folder_line = f'{indent_space}├── {folder_name}/'
        
        # Add folder line to result
        result.append(folder_line)

        # Print if verbose >= 1
        if verbose >= 1:
            print(folder_line)

        if not include_only_folder:
            # Sort files and print them in sorted order
            files.sort()
            subindent = indent * (level + 1)
            for f in files:
                file_line = f'{subindent}├── {f}'
                result.append(file_line)

                # Print if verbose >= 1
                if verbose >= 1:
                    print(file_line)

    # Return the folder structure as text
    return "\n".join(result)

def add_suffix_to_name(
        filepath: Path | str
        ,suffix:str | float | int
        ,seperator:str = "_"
        ):
    """
    Add a suffix to a file name before its extension.

    Parameters
    ----------
    filepath : Path or str
        The original file path.
    suffix : str, float, or int
        The suffix to add to the file name.
    separator : str, optional
        The separator to use between the original file name and the suffix. Default is "_".

    Returns
    -------
    Path or str
        The new file path with the suffix added. Returns a `str` if `filepath` is a `str`, or a `Path` if `filepath` is a `Path`.

    Notes
    -----
    - Converts the `filepath` to a string for processing.
    - Preserves the original file extension.
    - If `filepath` is a `Path` object, the returned value will also be a `Path` object.

    Examples
    --------
    >>> add_suffix_to_name("BigBang FR S02E01.ass", 1)
    'BigBang FR S02E01_1.ass'
    >>> from pathlib import Path
    >>> add_suffix_to_name(Path("video.mp4"), "edited")
    PosixPath('video_edited.mp4')
    """

    # tested via extract_sub_1_video
    from pathlib import Path
    filepath_str = str(filepath)
    name, ext = os.path.splitext(filepath_str)
    new_filename_str = f"{name}{seperator}{str(suffix)}{ext}"
    new_filename_Path = Path(new_filename_str)

    if isinstance(filepath,str):
        return new_filename_str
    else:
        return new_filename_Path


def clean_filename(ori_name):
    # update01: deal with '\n' case
    replace_with_empty = [".","?",":",'"' , "\\" ] 
    replace_with_space = ["\n", "/" ]
    
    new_name = ori_name
    for delimiter in replace_with_empty:
        new_name = new_name.replace(delimiter, "")
        
    for delimiter in replace_with_space:
        new_name = new_name.replace(delimiter, " ")

    return new_name

def rename_files_replace_text(folder_path, old_text, new_text, extension=None, case_sensitive=False) -> None:
    import os
    # not tested
    """
    Renames files in a folder by replacing a portion of the filename with new text.

    Args:
        folder_path (str): The path to the folder containing the files to rename.
        old_text (str): The text to be replaced in the filenames.
        new_text (str): The new text to replace the old text.
        extension (str or list, optional): If provided, only files with this extension (or extensions) will be renamed. Default is None.
        case_sensitive (bool, optional): If True, the text replacement will be case-sensitive. Default is False.

    Returns:
        None
    """
    renamed_count = 0

    if isinstance(extension, str):
        extension = [extension]

    for filename in os.listdir(folder_path):
        if extension is None or any(filename.endswith(ext) for ext in extension):
            if case_sensitive:
                new_filename = filename.replace(old_text, new_text)
            else:
                new_filename = filename.lower().replace(old_text.lower(), new_text.lower())

            if new_filename != filename:
                src_path = os.path.join(folder_path, filename)
                dest_path = os.path.join(folder_path, new_filename)
                os.rename(src_path, dest_path)
                renamed_count += 1

    


def auto_rename_series(folder_path,prefix, suffix = "", pattern = r'[sS]\d\d[eE]\d\d'):
    # medium tested
    # about 30 min(including testing)

    # function that will help rename series assuming the filename has SxxExx pattern in the filename
    # for automatically rename series files
    
    # it would additional space to prefix if it hasn't already had on
    prefix_in = prefix if prefix[-1] in [" ","_"] else prefix + " "

    import re
    import os
    
    video_path_list = get_full_filename(folder_path,[".mp4",".mkv"])
    video_name_list = get_filename(folder_path,[".mp4",".mkv"])
    subtitle_path_list = get_full_filename(folder_path,[".srt",".ass"])
    subtitle_name_list = get_filename(folder_path,[".srt",".ass"])
    
    for i, filename in enumerate(video_name_list):
        episode = re.findall(pattern, filename)
        extension = filename.split('.')[-1]
        # episode will be empty list when SxxExx is not found
        if len(episode) > 0:
            new_name = prefix_in + episode[0] + suffix + "." +  extension
            new_path = str(folder_path) + "/" + new_name
            os.rename(video_path_list[i],new_path)
    
    for i, filename in enumerate(subtitle_name_list):
        episode = re.findall(pattern, filename)
        # episode will be empty list when SxxExx is not found
        if len(episode) > 0:
            extension = filename.split('.')[-1]
            new_name = prefix_in + episode[0] + suffix + "." +  extension
            new_path = str(folder_path) + "/" + new_name
            os.rename(subtitle_path_list[i],new_path)

    
    
def is_folder_path(path:Union[str,Path]):
    # not tested
    import os
    """ 
    check if this path is folder or normal file(document, Excel, audio, video)

    """
    ans = os.path.isdir(str(path))

    return ans



def extract_filename(file_path: Union[list[str], list[Path] ,str, Path], 
                     with_extension = True) -> Union[list[str], str]:
    # high tested
    from pathlib import Path

    if not isinstance(file_path, list):
        file_path_in = [file_path]
    else:
        file_path_in = list(file_path)
    
    name_with_ext_list = []
    name_no_ext_list = []

    for curr_filepath in file_path_in:
        name_with_ext = Path(curr_filepath).name
        extension = '.' + name_with_ext.split(".")[-1]

        name_no_ext = name_with_ext.replace(extension,'')

        name_with_ext_list.append(name_with_ext)
        name_no_ext_list.append(name_no_ext)
    
    if len(name_with_ext_list) == 1:
        # del name_with_ext_list
        name_with_ext_list = name_with_ext_list[0]
    
    if len(name_no_ext_list) == 1:
        # del name_no_ext_list
        name_no_ext_list = name_no_ext_list[0]

    if with_extension:
        return name_with_ext_list
    else:
        return name_no_ext_list


def get_filename(folder_path,extension = "all"):
    import os
    """ 
    get all of filename that has 
    """
    # also include "folder"  case
# tested small
# new feature1: include subfolders
    if extension == "all":
        out_list = [ file for file in os.listdir(folder_path) ]

    elif isinstance(extension,str):
        extension_temp = [extension]

        out_list = []

        for file in os.listdir(folder_path):
            if "." in file:
                file_extension = file.split('.')[-1]
                for each_extention in extension_temp:
                    # support when it's ".csv" or only "csv"
                    if file_extension in each_extention:
                        out_list.append(file)
            elif extension == "folder":
                out_list.append(file)


    elif isinstance(extension,list):
        out_list = []
        for file in os.listdir(folder_path):

            if "." in file:
                file_extension = file.split('.')[-1]
                for each_extention in extension:
                    # support when it's ".csv" or only "csv"
                    if file_extension in each_extention:
                        out_list.append(file)

            elif "folder" in extension:
                out_list.append(file)

        return out_list

    else:
        print("Don't support this dataype for extension: please input only string or list")
        return False

    return out_list

def get_full_filename(folder_path,extension = "all"):
    import os
    # tested small
    short_names = get_filename(folder_path,extension)
    out_list = []
    for short_name in short_names:
        full_name = os.path.join(folder_path,short_name)
        out_list.append(full_name)
    return out_list



def os_add_extension(ori_path, added_extension, inplace = True):
    # still doesn't work
    # still can't modify the text direclty
    # imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 05_UsefulSenLabel\sen_useful_GPT01.py"
    ori_path_in = [ori_path] if isinstance(ori_path, str) else ori_path
    
    # for now I only write added_extension to support only string
    
    outpath = []

    
    if isinstance(added_extension, str):
        added_extension_in = added_extension if "." in added_extension else "." + added_extension
        
        for i,curr_path in enumerate(ori_path):
            if inplace:
                curr_path = curr_path if added_extension in curr_path else curr_path + added_extension_in
                ori_path[i] = curr_path

                
            else:
                curr_path_temp = curr_path if added_extension in curr_path else curr_path + added_extension_in
                outpath.append(curr_path_temp)
    
    if inplace:
        return ori_path
    else:
        # return the string if outpath has only 1 element, otherwise return the whole list
        if len(outpath) == 1:
            return outpath[0]
        else:
            return outpath
        