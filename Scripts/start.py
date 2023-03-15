from allresource import start_searching
from uploadgcs import gcs_upload_file
import pandas as pd




if __name__ == '__main__':
    # start_searching()
    # gcs_upload_file()
    
    get_resource_csv = pd.read_csv('../resource_data/resource_list.csv')
    extract_resource = get_resource_csv.groupby('Resource_Type', axis=1)
    print(extract_resource)
    
    
    
    
