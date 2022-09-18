import * as React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Header from '../../components/Header';
import RegisterForm from './RegisterForm';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

function RegisterDatabase() {
  const [activeTabIdx, setActiveTabIdx] = React.useState(0);

  const handleChange = (event, newValue) => {
    setActiveTabIdx(newValue);
  };
  
  return (
    <React.Fragment>
      <Header title="Register Database" />
      <Box component="main" sx={{ flex: 1, py: 6, px: 4, bgcolor: '#eaeff1' }}>
        <Paper sx={{ maxWidth: 936, margin: 'auto', overflow: 'hidden' }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={activeTabIdx} onChange={handleChange} aria-label="basic tabs example">
              <Tab label="Self-managed Postgres" disableRipple {...a11yProps(0)} />
              <Tab label="AWS RDS Postgres" disableRipple {...a11yProps(1)} />
            </Tabs>
          </Box>
          <TabPanel value={activeTabIdx} index={0}>
            <RegisterForm environment="SELF_MANAGED_POSTGRES" />
          </TabPanel>
          <TabPanel value={activeTabIdx} index={1}>
            Item Two
          </TabPanel>
        </Paper>
      </Box>
    </React.Fragment>
  )
};

export default RegisterDatabase;
