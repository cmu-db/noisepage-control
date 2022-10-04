import * as React from 'react';
import { useParams } from 'react-router-dom';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Header from '../../components/Header';
import DetailContent from './DetailContent';
import WorkloadContent from './WorkloadContent';
import StateContent from './StateContent';

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

function ManageDatabase() {
  // const [databaseInfos, setDatabaseInfos] = useState();
  const { id } = useParams()

  // useEffect(() => {
    // async function fetchDatabaseInfos() {
    //   const res = await axios.get('/database_manager/');
    //   console.log(res);
    //   setDatabaseInfos(res.data);
    // }
    // fetchDatabaseInfos();
  // }, []);

  const [activeTabIdx, setActiveTabIdx] = React.useState(0);

  const handleChange = (event, newValue) => {
    setActiveTabIdx(newValue);
  };

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
            <Tabs value={activeTabIdx} onChange={handleChange} aria-label="basic tabs example">
              <Tab label="Workloads" disableRipple sx={{ fontSize: 17 }} {...a11yProps(0)} />
              <Tab label="States" disableRipple sx={{ fontSize: 17 }} {...a11yProps(1)} />
              <Tab label="Generated Actions" disableRipple sx={{ fontSize: 17 }} {...a11yProps(2)} />
              <Tab label="Tuning History" disableRipple sx={{ fontSize: 17 }} {...a11yProps(3)} />
            </Tabs>
          </Box>
          <TabPanel value={activeTabIdx} index={0}>
            <WorkloadContent databaseId={id} />
          </TabPanel>
          <TabPanel value={activeTabIdx} index={1}>
            <StateContent databaseId={id} />
          </TabPanel>
          <TabPanel value={activeTabIdx} index={2}>
            Generated Actions
          </TabPanel>
          <TabPanel value={activeTabIdx} index={3}>
            Tuning History
          </TabPanel>
        </Paper>
      </Box>
    </React.Fragment>
  )
};

export default ManageDatabase;
