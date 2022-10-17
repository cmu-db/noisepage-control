import * as React from 'react';
import { useEffect, useState } from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import axios from '../../util/axios';

export default function DetailContent({ databaseId }) {
  const [databaseDetail, setDatabaseDetail] = useState();
  
  useEffect(() => {
    async function fetchDatabaseDetail() {
      try {
        const res = await axios.get(`/database_manager/databases/${databaseId}`);
        console.log(res);
        setDatabaseDetail(res.data);
      } catch (error) {
        console.error(error)
      }
    }
    fetchDatabaseDetail();
  }, [databaseId]);

  return databaseDetail && (
    <List>
      <ListItem>
        <ListItemText primary="Database ID" secondary={databaseDetail.database_id} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Created" secondary={databaseDetail.created} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Environment Type" secondary={databaseDetail.environment_type} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Errors" secondary={databaseDetail.errors} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Database Name" secondary={databaseDetail.db_name} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Primary Host" secondary={databaseDetail.primary_host} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Primary PG Port" secondary={databaseDetail.primary_pg_port} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Primary PG User" secondary={databaseDetail.primary_pg_user} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Primary SSH Port" secondary={databaseDetail.primary_ssh_port} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Primary SSH User" secondary={databaseDetail.primary_ssh_user} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Replica Host" secondary={databaseDetail.replica_host} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Replica PG Port" secondary={databaseDetail.replica_pg_port} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Replica PG User" secondary={databaseDetail.replica_pg_user} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Replica SSH Port" secondary={databaseDetail.replica_ssh_port} />
      </ListItem>
      <Divider/>
      <ListItem>
        <ListItemText primary="Replica SSH User" secondary={databaseDetail.replica_ssh_user} />
      </ListItem>
    </List>
    // <React.Fragment>
    //   <h1>Detail Content</h1>
    // </React.Fragment>
  )
}
