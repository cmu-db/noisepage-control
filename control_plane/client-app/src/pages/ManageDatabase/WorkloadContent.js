import * as React from 'react';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
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
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import Done from '@mui/icons-material/Done';
import axios from '../../util/axios';
import parseDateTime from '../../util/parseDateTime';

function addMinutes(date, minutes) {
  return new Date(date.getTime() + minutes*60000);
}

export default function WorkloadContent() {
  const { id: databaseId } = useParams();
  const [workloads, setWorkloads] = useState();
  const [timePeriod, setTimePeriod] = useState(10);
  const [name, setName] = useState('');
  const [workloadSubmitLoading, setWorkloadSubmitLoading] = useState(false);
  const [workloadSubmitSuccess, setWorkloadSubmitSuccess] = useState(false);
  
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

  const handleTimePeriodInputChange = (event) => {
    setTimePeriod(event.target.value === '' ? 10 : Number(event.target.value));
  };

  const handleNameInputChange = (event) => {
    setName(event.target.value);
  };

  const handleCollectWorkload = async (event) => {
    event.preventDefault();
    console.log(`Submit collect workload for ${timePeriod} seconds`);
    console.log(`Name: ${name}`);
    setWorkloadSubmitLoading(true);

    try {
      const body = {
        time_period: timePeriod,
        friendly_name: name
      };
      const res = await axios.post(`/database_manager/databases/${databaseId}/workloads`, body);
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
      <TableContainer component={Paper} sx={{ mt: 3 }}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Start</TableCell>
              <TableCell>End</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {workloads.reverse().map((workload) => (
              <TableRow
                key={workload.resource_id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell>{workload.friendly_name}</TableCell>
                <TableCell>
                  {workload.available
                    ?
                    <Link href={`${axios.defaults.baseURL}/database_manager/workload/${workload.resource_id}`} underline="always">
                      Available
                    </Link>
                    : 'Collecting'
                  }
                </TableCell>
                <TableCell>{parseDateTime(workload.collected_at)}</TableCell>
                <TableCell>{parseDateTime(addMinutes(new Date(workload.collected_at), 5))}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      {/* <Grid container sx={{ m: 1, mt: 4 }}>
        <Grid item xs={12} sm={6} lg={4}>
          <Typography variant="h6" sx={{ mb: 3 }}>Collect a New Workload</Typography>
          <Box sx={{ display: 'flex' }}>
            <Typography id="input-slider" sx={{ mr: 3, mt: 0.1 }}>
              Time Period:
            </Typography>
            <Input
              value={timePeriod}
              size="small"
              onChange={handleTimePeriodInputChange}
              inputProps={{
                step: 10,
                min: 10,
                type: 'number',
                'aria-labelledby': 'input-slider',
              }}
              sx={{ maxWidth: 70 }}
            />
          </Box>
          <Box sx={{ display: 'flex', mt: 3 }}>
            <Typography sx={{ mr: 1, mt: 0.4 }}>
              Name:
            </Typography>
            <TextField
              required
              id="workload-name"
              variant="standard"
              onChange={handleNameInputChange}
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
      </Grid> */}
    </React.Fragment>
  )
}
