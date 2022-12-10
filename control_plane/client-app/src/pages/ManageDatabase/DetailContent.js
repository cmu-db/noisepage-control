import * as React from 'react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';
import Collapse from '@mui/material/Collapse';
import axios from '../../util/axios';
import detailFixure from '../../fixtures/databaseDetail';

const gridItemStyle = {
    borderRight: '1px solid',
  borderColor: 'rgba(0, 0, 0, 0.12)'
};

export default function DetailContent({ detailExpanded }) {
  const { id: databaseId } = useParams();
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
  <React.Fragment>
    <Grid container spacing={0} sx={{ pt: 1 }} >
      <Grid item xs={4} sx={gridItemStyle}>
        <ListItem>
          <ListItemText primary="Database ID" secondary={databaseDetail.database_id} />
        </ListItem>
      </Grid>
      <Grid item xs={4} sx={gridItemStyle}>
        <ListItem>
          <ListItemText primary="Database Name" secondary={detailFixure[databaseDetail.database_id].Name} />
        </ListItem>
      </Grid>
      <Grid item xs={4}>
        <ListItem>
          <ListItemText primary="Created" secondary={databaseDetail.created} />
        </ListItem>
      </Grid>
      <Grid item xs={4} sx={gridItemStyle}>
        <ListItem>
          <ListItemText primary="PostgrSQL Version" secondary={detailFixure[databaseDetail.database_id].Version} />
        </ListItem>
      </Grid>
      <Grid item xs={4} sx={gridItemStyle}>
        <ListItem>
          <ListItemText primary="Database Size" secondary={detailFixure[databaseDetail.database_id].Size} />
        </ListItem>
      </Grid>
      <Grid item xs={4}>
        <ListItem>
          <ListItemText primary="CPU" secondary={detailFixure[databaseDetail.database_id].CPU} />
        </ListItem>
      </Grid>
    </Grid>

    <Collapse in={detailExpanded} timeout="auto" unmountOnExit >
      <Grid container spacing={0} sx={{ pb: 1 }} >
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="Memory" secondary={detailFixure[databaseDetail.database_id].Memory} />
          </ListItem>
        </Grid>
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="Environment Type" secondary={databaseDetail.environment_type} />
          </ListItem>
        </Grid>
        <Grid item xs={4}>
          <ListItem>
            <ListItemText primary="Errors" secondary={databaseDetail.errors} />
          </ListItem>
        </Grid>
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="PostgreSQL Database Name" secondary={databaseDetail.db_name} />
          </ListItem>
        </Grid>
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="Primary Host" secondary={databaseDetail.primary_host} />
          </ListItem>
        </Grid>
        <Grid item xs={4}>
          <ListItem>
            <ListItemText primary="Primary PG Port" secondary={databaseDetail.primary_pg_port} />
          </ListItem>
        </Grid>
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="Primary PG User" secondary={databaseDetail.primary_pg_user} />
          </ListItem>
        </Grid>
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="Primary SSH Port" secondary={databaseDetail.primary_ssh_port} />
          </ListItem>
        </Grid>
        <Grid item xs={4}>
          <ListItem>
            <ListItemText primary="Primary SSH User" secondary={databaseDetail.primary_ssh_user} />
          </ListItem>
        </Grid>
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="Replica Host" secondary={databaseDetail.replica_host} />
          </ListItem>
        </Grid>
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="Replica PG Port" secondary={databaseDetail.replica_pg_port} />
          </ListItem>
        </Grid>
        <Grid item xs={4}>
          <ListItem>  
            <ListItemText primary="Replica PG User" secondary={databaseDetail.replica_pg_user} />
          </ListItem>
        </Grid>
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="Replica SSH Port" secondary={databaseDetail.replica_ssh_port} />
          </ListItem>
        </Grid>
        <Grid item xs={4} sx={gridItemStyle}>
          <ListItem>
            <ListItemText primary="Replica SSH User" secondary={databaseDetail.replica_ssh_user} />
          </ListItem>
        </Grid>
      </Grid>
    </Collapse>
  </React.Fragment>
  );
};
