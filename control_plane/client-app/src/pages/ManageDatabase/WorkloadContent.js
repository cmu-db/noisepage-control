import * as React from 'react';
import { useState, useEffect } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import LoadingButton from '@mui/lab/LoadingButton';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Input from '@mui/material/Input';
import Grid from '@mui/material/Grid';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import Done from '@mui/icons-material/Done';
import axios from '../../util/axios';

export default function WorkloadContent({ databaseId }) {
  const [workloads, setWorkloads] = useState();
  const [timePeriod, setTimePeriod] = useState(10);
  const [workloadSubmitLoading, setWorkloadSubmitLoading] = useState(false);
  const [workloadSubmitSuccess, setWorkloadSubmitSuccess] = useState(false);
  
  useEffect(() => {
    async function fetchWorkloads() {
      try {
        const res = await axios.get(`/database_manager/databases/${databaseId}/workloads`);
        console.log(res);
        setWorkloads(res.data);  
      } catch (error) {
        console.error(error)
      }
    }
    fetchWorkloads();
  }, [databaseId]);

  const handleInputChange = (event) => {
    setTimePeriod(event.target.value === '' ? 10 : Number(event.target.value));
  };

  const handleCollectWorkload = async (event) => {
    event.preventDefault();
    console.log(`Submit collect workload for ${timePeriod} seconds`);
    setWorkloadSubmitLoading(true);

    try {
      const res = await axios.post(`/database_manager/databases/${databaseId}/workloads`, {time_period: timePeriod});
      console.log(res);
      setWorkloadSubmitSuccess(true);
      window.location.reload();
    } catch (error) {
      console.error(error);
    } finally {
      setWorkloadSubmitLoading(false);
    }
  };

  return workloads && (
    <React.Fragment>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Workload ID</TableCell>
              <TableCell>Workload Name</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {workloads.map((workload) => (
              <TableRow
                key={workload.resource_id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {workload.available
                    ?
                    <Link href={`${axios.defaults.baseURL}/database_manager/workload/${workload.resource_id}`} underline="always">
                      {workload.resource_id}
                    </Link>
                    :
                    workload.resource_id
                  }
                </TableCell>
                <TableCell>{workload.resource_name}</TableCell>
                <TableCell>{workload.available ? 'Available' : 'Collecting'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Grid container sx={{ m: 1, mt: 4 }}>
        <Grid item xs={12} sm={6} lg={4}>
          <Typography variant="h6" sx={{ mb: 3 }}>Collect a New Workload</Typography>
          <Box sx={{ display: 'flex' }}>
            <Typography id="input-slider" sx={{ mr: 1, mt: 0.1 }}>
              Time Period:
            </Typography>
            <Input
              value={timePeriod}
              size="small"
              onChange={handleInputChange}
              inputProps={{
                step: 10,
                min: 10,
                type: 'number',
                'aria-labelledby': 'input-slider',
              }}
              sx={{ maxWidth: 70 }}
            />
          </Box>
          <LoadingButton
            variant="contained"
            startIcon={workloadSubmitSuccess ? <Done /> : <LibraryAdd />}
            sx={{ mt: 4, '&.Mui-disabled': { bgcolor: '#a5d6a7' } }}
            onClick={handleCollectWorkload}
            loading={workloadSubmitLoading}
            loadingPosition="start"
            disabled={workloadSubmitSuccess}
          >
            Collect!
          </LoadingButton>
        </Grid>
      </Grid>
    </React.Fragment>
  )
}
