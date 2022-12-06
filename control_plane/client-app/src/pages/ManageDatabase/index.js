import * as React from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { Link, Outlet } from "react-router-dom";
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Header from '../../components/Header';

function ManageDatabase() {
  const { id } = useParams()
  const location = useLocation();

  const getPathOrDefault = () => {
    const path = location.pathname.split('/').at(-1);
    if (path === id) {
      return 'detail';
    }
    return path;
  }

  return (
    <React.Fragment>
      {/* TODO: uncomment back <Header title={`Database ID: ${id}`} /> */}
      <Header title={`Database Name: ${id === '62d09efd-3602-483d-8a8d-60445385adec' ? 'Restaurant Ordering Website' : 'Analytic' }`} />
      <Box component="main" sx={{ flex: 1, py: 6, px: 6, bgcolor: '#eaeff1' }}>
        <Paper sx={{ minWidth: 275 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', p: 1 }}>
            <Tabs value={getPathOrDefault()} >
              <Tab value="detail" component={Link} to="detail" label="Detail" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="tune" component={Link} to="tune" label="Tune Database" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="tuning-history" component={Link} to="tuning-history" label="Tuning History" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="workloads" component={Link} to="workloads" label="Workloads" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="states" component={Link} to="states" label="States" disableRipple sx={{ fontSize: 17 }} />
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
