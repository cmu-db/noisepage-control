import * as React from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { Link, Outlet } from "react-router-dom";
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Header from '../../components/Header';
import DetailContent from './DetailContent';

function ManageDatabase() {
  const { id } = useParams()
  const location = useLocation();

  const getPathOrDefault = () => {
    const path = location.pathname.split('/').at(-1);
    if (path === id) {
      return 'workloads';
    }
    return path;
  }

  return (
    <React.Fragment>
      <Header title={`Database ID: ${id}`} />
      <Box component="main" sx={{ flex: 1, py: 6, px: 6, bgcolor: '#eaeff1' }}>
        <Paper sx={{ minWidth: 275, mb: 4 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', p: 3 }}>
            <Typography variant="h5">Details</Typography>
          </Box>
          <Box sx={{ p: 3 }}>
            <DetailContent databaseId={id} />
          </Box>
        </Paper>
        <Paper sx={{ minWidth: 275 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', p: 1 }}>
            <Tabs value={getPathOrDefault()} >
              <Tab value="workloads" component={Link} to="workloads" label="Workloads" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="states" component={Link} to="states" label="States" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="tunes" component={Link} to="tunes" label="Tune Database" disableRipple sx={{ fontSize: 17 }} />
            </Tabs>
          </Box>
          <Box sx={{ p: 3 }}>
            <Outlet />
          </Box>
        </Paper>
      </Box>
    </React.Fragment>
  )
};

export default ManageDatabase;
