import subprocess

def get_data_directory(port):
    args = ['sudo', '-u', 'postgres', 'psql', '-c', 'show data_directory;', '-p', str(port)]
    res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    """Example output:
            data_directory
    ------------------------------------
    /var/lib/postgresql/14/main
    (1 row)
    """
    if res.returncode != 0:
        return None
    return res.stdout.decode('utf-8').strip().split('\n')[2].strip()
