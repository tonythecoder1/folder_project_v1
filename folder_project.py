import os
import hashlib
import shutil
import argparse
import logging
import time

def ensure_folder_exists(folder):
    if not os.path.exists(folder):
        print(f"The folder doesn't exists - Creating new Main folder!")
        os.makedirs(folder)
    else:
        print("-Folder Found!")


def list_files(folder):
    try:
        i = 0
        print(f"Showing {os.path.basename(folder)} \n")
        files = os.listdir(folder)

        if not files:
            print(f"The folder {os.path.basename(folder)} is empty")
            return []
        else:
            for file in files:
                i += 1
                print(f"File {i} - {file}")
            return files
    except Exception as e:
        print(f"Error while showing files in {folder} ")
        return []
        

def md5_calc(file_calc):
    if not os.path.isfile(file_calc):
        print("File not exists - MD5 CALC ERROR")
        return None
    try:
        with open(file_calc, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print("Error While calculating MD5: {e}" )
        return None
    
def compare_folders(main_folder, replica_folder):
    main_files = list_files(main_folder)
    replica_files = list_files(replica_folder)

    if(set(main_files) != set(replica_files)):
        logging.warning("Folders have different file sets")
        return False

    for file in main_files:

        main_file_p = os.path.join(main_folder, file)
        replica_files_p = os.path.join(replica_folder, file)

        if md5_calc(main_file_p) != md5_calc(replica_files_p):
            logging.warning("File '{file}' is different")
            return False

    logging.info("Folders are synch")   
    return True
    

def sync_files(main_folder, replica_folder):

    main_files = list_files(main_folder)
    replica_files = list_files(replica_folder)

    if compare_folders(main_folder, replica_folder):
        print("Folders are Already Sync!")

    for file in main_files:
        source_file_p = os.path.join(main_folder, file)
        replica_file_p = os.path.join(replica_folder, file)

        if file not in replica_files or md5_calc(source_file_p) != md5_calc(replica_file_p):
            try:
                source_file_p = os.path.join(main_folder, file)
                destination_file_p = os.path.join(replica_folder, file)
                if(os.path.exists(replica_file_p)):
                    os.remove(replica_file_p)
                    logging.info(f"File '{os.path.basename(replica_file_p)}' was removed from Replica folder")
               
                shutil.copy(source_file_p, destination_file_p)
                logging.info(f"File '{os.path.basename(source_file_p)}' was copied from Main Folder to Replica Folder")
                print("File copied with success")

            except Exception as e:
                    logging.error(f"Error while copying: {e}") 

    for file in replica_files:
        if file not in main_files:
            replica_file_p = os.path.join(replica_folder, file)
            try:
                os.remove(replica_file_p)
                print(f"The Obsolete file/s {os.path.basename(replica_file_p)} in the Replica folder was removed")
                logging.info(f"File {os.path.basename(replica_file_p)} was removed from Replica File ")
            except Exception as e:
                logging.error(f"Error while removing the file from Replica Folder")
            

def parse_args_command():
    parser = argparse.ArgumentParser(description="Sync Folder Project")
    parser.add_argument("source")
    parser.add_argument("replica")
    parser.add_argument("interval")
    parser.add_argument("logfile")

    args = parser.parse_args()

    try:
        args.interval = float(args.interval)
        if args.interval <= 0:
            raise ValueError("Interval must be a positive number")
    except ValueError as e:
        parser.error(f"Invalid interval number. It must be a positive number {e}")
    
    return args

def setup_logging(log_file):

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
    )

if __name__ == '__main__':

    args = parse_args_command()
    setup_logging(args.logfile)

    if (args.source == args.replica):
        logging.error("Error - The Main file can't be the same as the Replica file")
        exit(1)
   
    ensure_folder_exists(args.source)
    ensure_folder_exists(args.replica)

    list_files(args.replica)
    
    try:
        while True:
            logging.info("Starting sync")
            sync_files(args.source, args.replica)
            logging.info("Sync completed")
            time.sleep(float(args.interval))
    except KeyboardInterrupt:
        logging.info("Sync was stopped by the user")


    

    


