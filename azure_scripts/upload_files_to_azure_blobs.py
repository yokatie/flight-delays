from azure.storage.blob import BlockBlobService
import glob
import ConfigParser


def main():
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")

    # initialize constant variables
    STORAGE_NAME = Config.get('azure-blob', 'STORAGE_NAME')
    STORAGE_KEY = Config.get('azure-blob', 'STORAGE_KEY')
    TARGET_FOLDER_NAME = Config.get('azure-blob', 'TARGET_FOLDER_NAME')
    LOCAL_FILE_PATH = Config.get('azure-blob', 'LOCAL_FILE_PATH')
    CONTAINER_NAME = Config.get('azure-blob', 'CONTAINER_NAME')

    # initialize client for upload to azure
    block_blob_service = BlockBlobService(account_name=STORAGE_NAME, account_key=STORAGE_KEY)

    # get all folder containing months of flights data
    folders = glob.glob(LOCAL_FILE_PATH.format("*/"))
    for folder in folders:
        # get all the csv from current folder to upload
        files_to_upload = glob.glob(folder + "*.csv")
        for f in files_to_upload:
            # get the file name without extension
            file_name = f[f.rfind('/') + 1:].replace(".csv", '')
            block_blob_service.create_blob_from_path(
                CONTAINER_NAME,
                TARGET_FOLDER_NAME + file_name,
                f
            )

    return


if __name__ == "__main__":
    main()