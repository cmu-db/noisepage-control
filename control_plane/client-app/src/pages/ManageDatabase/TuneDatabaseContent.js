import * as React from 'react';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import LoadingButton from '@mui/lab/LoadingButton';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import WorkloadChart from './WorkloadChart';
import axios from '../../util/axios';

export default function TuneDatabaseContent() {
  const { id: databaseId } = useParams();
  const [workloads, setWorkloads] = useState();
  const [name, setName] = useState('');
  const [chartMetricType, setChartMetricType] = useState('num_queries');
  // const [workloadSubmitLoading, setWorkloadSubmitLoading] = useState(false);
  // const [workloadSubmitSuccess, setWorkloadSubmitSuccess] = useState(false);
  
  useEffect(() => {
    async function fetchWorkloads() {
      try {
        const res = await axios.get(`/database_manager/databases/${databaseId}/workloads`);
        console.log(res);
        setWorkloads(res.data.sort((a, b) => new Date(a.collected_at) - new Date(b.collected_at)));  
      } catch (error) {
        console.error(error)
      }
    }
    fetchWorkloads();
  }, [databaseId]);

  const handleNameInputChange = (event) => {
    setName(event.target.value);
  };

  // const handleTuneDatabase = async (event) => {
  //   if (!selectedWorkloadId || !selectedStateId) {
  //     return;
  //   }

  //   event.preventDefault();
  //   console.log(`Submit tune database`);
  //   setSubmitLoading(true);

  //   try {
  //     const body = {
  //       workload_id: selectedWorkloadId,
  //       state_id: selectedStateId,
  //       friendly_name: name,
  //     }
  //     const res = await axios.post(
  //       `/database_manager/databases/${databaseId}/tune`,
  //       body
  //     );
  //     console.log(res);
  //     setSubmitSuccess(true);
  //     window.location.reload();
  //   } catch (error) {
  //     console.error(error);
  //   } finally {
  //     setSubmitLoading(false);
  //   }
  // };

  const handleChartMetricToggle = (event, metricType) => {
    setChartMetricType(metricType);
  };

  return workloads && (
    <React.Fragment>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={4}></Grid>
        <Grid item xs={4}>
          <Typography variant="h6" component="div" align='center'>
            Select a Target Workload Range
          </Typography>
        </Grid>
        <Grid item xs={4}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
            <ToggleButtonGroup
              value={chartMetricType}
              exclusive
              onChange={handleChartMetricToggle}
              size={'small'}
              sx={{ marginLeft: 'auto' }}
            >
              <ToggleButton value="num_queries">
                # of queries
              </ToggleButton>
              <ToggleButton value="p99">
                P99 latency
              </ToggleButton>
            </ToggleButtonGroup>
          </Box>
        </Grid>
      </Grid>

      <WorkloadChart workloads={workloads} metricType={chartMetricType}/>

      <Box sx={{ m: 2 }} align="center">
        <LoadingButton
          variant="contained"
          startIcon={<LibraryAdd />}
          sx={{ mt: 4, '&.Mui-disabled': { bgcolor: '#a5d6a7' } }}
          // onClick={handleTuneDatabase}
          // loading={submitLoading}
          // loadingPosition="start"
          // disabled={submitSuccess}
        >
          Tune!
        </LoadingButton>
      </Box>
    </React.Fragment>
  )
}
