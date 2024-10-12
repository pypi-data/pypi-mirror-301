"""Core module for defining partitions related operations."""
import subprocess
from shutil import copyfile
from textwrap import dedent

from vantage_agent.logger import logger
from vantage_agent.settings import SETTINGS
from vantage_agent.vantage_api_client import AsyncBackendClient


def create_backup(file_path):
    """Create a backup of slurm.conf."""
    backup_path = f"{SETTINGS.CACHE_DIR}/slurm.conf.bkp"
    copyfile(file_path, backup_path)
    logger.info('SLURM conf backup created')

def update_slurm_config(partitions):
    """Update the slurm.conf file with the given partitions."""
    # Backup slurm.conf file
    create_backup(SETTINGS.SLURM_CONF_PATH)

    with open(SETTINGS.SLURM_CONF_PATH, 'r') as f:
        slurm_config = f.readlines()

    new_partition_configs = []
    node_names_seen = set()

    for partition in partitions:
        # Build the new config for each partition
        is_default = "Yes" if partition["isDefault"] else "No"
        node_range = f"[0-{partition['maxNodeCount'] - 1}]"
        node_name = f"NodeName={partition['name']}-{partition['name']}-{node_range} State=CLOUD Weight=1 Feature=cloud CPUs=2\n" #noqa
        partition_name = f"PartitionName={partition['name']} Nodes={partition['name']}-{partition['name']}-{node_range} MaxTime=INFINITE State=UP Default={is_default}\n" #noqa

        new_partition_configs.append(node_name)
        new_partition_configs.append(partition_name)

        # Toggle node as done
        node_names_seen.add(partition['name'])

    # Filter the lines that don't belong to any existent partition
    filtered_config = []
    for line in slurm_config:
        if line.startswith('NodeName=') or line.startswith('PartitionName='):
            partition_name = line.split('=')[1].split('-')[0]
            if partition_name not in node_names_seen:
                continue
        filtered_config.append(line)

    # Add the new partitions to the end of slurm.conf file and write a new file
    filtered_config += new_partition_configs
    with open(SETTINGS.SLURM_CONF_PATH, 'w') as f:
        f.writelines(filtered_config)
    node_names = ', '.join(node_names_seen)
    logger.info(f'SLURM conf file updated with the partitions {node_names}')

async def get_cluster_partitions():
    """Get the partitions from the api."""
    query = dedent(
        """
        query($filters: JSONScalar!, $first: Int, $after: Int) {
            partitions(filters: $filters, after: $after, first: $first) {
                edges {
                    node {
                        clusterName
                        id
                        isDefault
                        maxNodeCount
                        name
                        nodeType
                    }
                }
            }
        }
        """
    )

    body = {
        "query": query,
        "variables": {
            "filters": {
                "clusterName": {
                    "eq": SETTINGS.CLUSTER_NAME
                }
            },
            "after": 1,
            "first": 100
        },
    }

    async with AsyncBackendClient() as backend_client:
        res = await backend_client.post("/cluster/graphql", json=body)
        res = res.json()
    partitions = res['data']['partitions']['edges']

    return partitions


def reconfigure_slurm():
    """Reload the slurm.conf to get the new changes in the slurm.conf."""
    try:
        logger.debug("Reloading SLURM config.")
        result = subprocess.run(['scontrol', 'reconfigure'], check=True, capture_output=True, text=True)
        logger.info(f"SLURM config reloaded:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while reloading SLURM conf:\n{e.stderr}")
        raise e

async def sync_cluster_partitions():
    """Sync the slurm partitions with the current partitions in the API."""
    try:
        logger.info("Syncing SLURM partitions.")

        partitions = await get_cluster_partitions()

        logger.debug("Updating SLURM config file.")
        update_slurm_config(partitions=partitions)

        logger.debug("Reloading SLURM config.")
        reconfigure_slurm()

        logger.info("SLURM partitions synced.")
    except Exception as e:
        logger.error(f'Error while syncing the partitions: {str(e)}')
