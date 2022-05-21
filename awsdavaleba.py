import boto3
import argparse





def create_my_instance(subnet, group, client):
    response = client.run_instances(
        BlockDeviceMappings=[{'DeviceName': '/dev/sdh',
                              'Ebs': {
                                      'VolumeSize': 9,
                                      'VolumeType': 'gp2',
                                      'DeleteOnTermination': True,
                                      'Encrypted': False}
                              }],
        ImageId='ami-0022f774911c1d690',
        InstanceType='t2.micro', 
        KeyName='my-quiz-key-1',
        InstanceINetworkInterfacestiatedShutdownBehavior='terminate',
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': False,  
                'DeleteOnTermination': True,
                'Description': 'string',
                'Groups': [
                    group
                ],
                'DeviceIndex':0,
                'SubnetId':subnet
            },
        ])

    for inst in response.get("Instances"):

        inst_id = inst.get("InstanceId")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', "--subnet")
    parser.add_argument('-g', "--vpc")
    parser.add_argument('-v', "--vpc")

    return parser.parse_args()

def key_pair(client, name):
    response = client.create_key_pair(
        KeyName=name,
        KeyType='rsa',
        KeyFormat='pem',    
    )

    pair_id = response.get('KeyPairId')

    with open(f'{key_name}.pem', 'w') as file:

        file.write(response.get('KeyMaterial'))

    return pair_id


def runner():
    parser = init_argparse()
    client = boto3.client('ec2', region_name='us-east-1')
    create_key_pair(client, 'my-quiz-key-1')
    create_instance(client, parser.group, parser.subnet)



runner()
