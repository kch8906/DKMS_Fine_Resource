import subprocess
import json
from multiprocessing import Pool
import itertools
from datetime import datetime
import pandas as pd

def find_resource(resource) -> str:    
#     for item in tqdm(resource):
    proc = subprocess.Popen(
        ['aws', 'configservice', 'list-discovered-resources', '--resource-type', f'{resource}'],
    stdout = subprocess.PIPE
    )
    out, err = proc.communicate()
    
    if 'resourceType' in str(out):
        out = out.decode('utf-8')
        out = json.loads(out)
        resourceID = [out['resourceIdentifiers'][idx]['resourceId'] for idx in range(len(out['resourceIdentifiers']))]
        return [resource, resourceID]
    else:
        return 0

def multiprocessing(resource_lists) -> list:
    exist_resources = [] 
    pool = Pool(processes=4)
    resource = pool.map(find_resource, resource_lists)
    exist_resources.append(resource)
    print(resource)
    pool.close()
    pool.join()

def preprocessing_resource(exist_resources) -> list:
    exist_resources = list(itertools.chain(*exist_resources))
    exist_resources = [item for item in exist_resources if item != 0]
    exist_resources = dict(zip(range(1, len(exist_resources) + 1), exist_resources))
    result = json.dumps(exist_resources)
    
    return result

def convert_dataframe(resource_json) -> dict:
    df_resource = pd.DataFrame.from_dict(resource_json, orient='index', columns=['Resource_Type','ResourceID'])
    df_resource['date']=pd.datetime.now().date()
    df_resource.explode('ResourceID')
    
    return df_resource
    

if __name__ == 'main':    
    resources = "AWS::EC2::CustomerGateway | AWS::EC2::EIP | AWS::EC2::Host | AWS::EC2::Instance | AWS::EC2::InternetGateway | AWS::EC2::NetworkAcl | AWS::EC2::NetworkInterface | AWS::EC2::RouteTable | AWS::EC2::SecurityGroup | AWS::EC2::Subnet | AWS::CloudTrail::Trail | AWS::EC2::Volume | AWS::EC2::VPC | AWS::EC2::VPNConnection | AWS::EC2::VPNGateway | AWS::EC2::RegisteredHAInstance | AWS::EC2::NatGateway | AWS::EC2::EgressOnlyInternetGateway | AWS::EC2::VPCEndpoint | AWS::EC2::VPCEndpointService | AWS::EC2::VPCPeeringConnection | AWS::IAM::Group | AWS::IAM::Policy | AWS::IAM::Role | AWS::IAM::User |  AWS::ElasticLoadBalancingV2::LoadBalancer | AWS::ACM::Certificate | AWS::RDS::DBInstance | AWS::RDS::DBSubnetGroup | AWS::RDS::DBSecurityGroup | AWS::RDS::DBSnapshot | AWS::RDS::DBCluster | AWS::RDS::DBClusterSnapshot | AWS::RDS::EventSubscription | AWS::S3::Bucket | AWS::S3::AccountPublicAccessBlock | AWS::ElasticLoadBalancing::LoadBalancer | AWS::AutoScaling::ScalingPolicy | AWS::AutoScaling::ScheduledAction | AWS::DynamoDB::Table | AWS::Lambda::Function | AWS::NetworkFirewall::Firewall | AWS::NetworkFirewall::FirewallPolicy | AWS::NetworkFirewall::RuleGroup | AWS::ECR::Repository | AWS::EKS::Cluster | AWS::Route53::HostedZone"
    resource_lists = resources.split(" | ")    
    exist_resources = multiprocessing(resource_lists)
    resource_json = preprocessing_resource(exist_resources)
    df_resource = convert_dataframe(resource_json)
    date = datetime.today().strftime("%Y%m%d")
    df_resource.to_excel("f'{date}'_resource_list.xlsx")   
    