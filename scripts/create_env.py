import os
import boto3


def create_env_vars():
    client = boto3.client('ssm', region_name="eu-central-1")
    env_file_sample = open('./.env_sample', 'r')
    env_vars = list(map(lambda item: item.strip(
        "=\n"), env_file_sample.readlines()))
    env_file_sample.close()
    env_file = open('./.env', 'w')
    env_file.write("ENV=production\n")
    for var in env_vars:
        response = client.get_parameter(Name=f'/DiaryApp/production/{var}')
        env_file.write(f'{var}={response["Parameter"]["Value"]}\n')
    env_file.close()


if __name__ == "__main__":
    create_env_vars()
