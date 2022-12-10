import * as React from 'react';
import { useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { Link, Outlet } from "react-router-dom";
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import Header from '../../components/Header';
import DetailContent from './DetailContent';
import databaseDetails from '../../fixtures/databaseDetail';

function ManageDatabase() {
  const { id } = useParams();
  const location = useLocation();
  const [detailExpanded, setDetailExpanded] = useState(false);

  const getPathOrDefault = () => {
    const path = location.pathname.split('/').at(-1);
    if (path === id) {
      return 'tune';
    }
    return path;
  }

  return (
    <React.Fragment>
      {/* TODO: uncomment back <Header title={`Database ID: ${id}`} /> */}
      <Header title={`${databaseDetails[id].Name}`} />

      <Box sx={{ flex: 1, pt: 6, px: 6 }}>
        <Paper sx={{ minWidth: 275 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', p: 3 }}>
            <Typography variant="h6">
              Database Summary for {id} ({databaseDetails[id].Name})
            </Typography>
          </Box>
          <Box sx={{ px: 3 }}>
            <DetailContent id={id} detailExpanded={detailExpanded} />
          </Box>
        </Paper>
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'center', height: 0 }}>
        <Button
          disableRipple
          onClick={() => setDetailExpanded(!detailExpanded)}
          sx={{
            transform: 'scale(0.9)',
            top: '-30px',
            textDecoration: 'none',
            borderStyle: 'solid',
            borderRadius: '50%',
            borderColor: 'gray',
            background: 'white',
            boxShadow: '0px 2px 1px -1px rgba(0,0,0,0.2),0px 1px 1px 0px rgba(0,0,0,0.14),0px 1px 3px 0px rgba(0,0,0,0.12)',
            width: 60, height: 60, color: 'inherit',
            opacity: 0.8,
            '&:hover': {
              backgroundColor: 'white',
            },
          }}
        >
          {detailExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        </Button>
      </Box>

      <Box component="main" sx={{ flex: 1, py: 6, px: 6 }}>
        <Paper sx={{ minWidth: 275 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', p: 1 }}>
            <Tabs value={getPathOrDefault()} >
              <Tab value="tune" component={Link} to="tune" label="Tune Database" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="tuning-history" component={Link} to="tuning-history" label="Tuning History" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="workloads" component={Link} to="workloads" label="Workloads" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="states" component={Link} to="states" label="States" disableRipple sx={{ fontSize: 17 }} />
              <Tab value="details" component={Link} to="details" label="Details" disableRipple sx={{ fontSize: 17 }} />
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
