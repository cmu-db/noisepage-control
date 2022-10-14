import * as React from 'react';
import { useState, useEffect } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import FormControl from '@mui/material/FormControl';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import LoadingButton from '@mui/lab/LoadingButton';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import axios from '../../util/axios';
import TuningStatus from '../../util/tuningStatus';

export default function TuneDatabaseContent({ databaseId }) {
  const [tuningInstances, setTuningInstances] = useState();
  const [workloads, setWorkloads] = useState();
  const [states, setStates] = useState();
  const [selctedWorkloadId, setSelectedWorkloadId] = useState('');
  const [selectedStateId, setSelectedStateId] = useState('');
  
  const [submitLoading, setSubmitLoading] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  
  // TODO: move api calls to a separate file
  useEffect(() => {
    async function fetchTuningInstances() {
      try {
        const res = await axios.get(`/database_manager/databases/${databaseId}/tune`);
        console.log(res);
        setTuningInstances(res.data);  
      } catch (error) {
        console.error(error)
      }
    }
    async function fetchWorkloads() {
      try {
        const res = await axios.get(`/database_manager/databases/${databaseId}/workloads`);
        console.log(res);
        setWorkloads(res.data);  
      } catch (error) {
        console.error(error)
      }
    }
    async function fetchStates() {
      try {
        const res = await axios.get(`/database_manager/databases/${databaseId}/states`);
        console.log(res);
        setStates(res.data);  
      } catch (error) {
        console.error(error)
      }
    }

    fetchTuningInstances();
    fetchWorkloads();
    fetchStates();
  }, [databaseId]);

  const handleTuneDatabase = async (event) => {
    if (!selctedWorkloadId || !selectedStateId) {
      return;
    }

    event.preventDefault();
    console.log(`Submit tune database`);
    setSubmitLoading(true);

    try {
      const res = await axios.post(
        `/database_manager/databases/${databaseId}/tune`,
        {workload_id: selctedWorkloadId, state_id: selectedStateId}
      );
      console.log(res);
      setSubmitSuccess(true);
      window.location.reload();
    } catch (error) {
      console.error(error);
    } finally {
      setSubmitLoading(false);
    }
  };

  const handleSelectedWorkloadIdChange = (event) => {
    setSelectedWorkloadId(event.target.value);
  };

  const handleSelectedStateIdChange = (event) => {
    setSelectedStateId(event.target.value);
  };

  return tuningInstances && (
    <React.Fragment>
      <Typography variant="h6" sx={{ mx: 1, mb: 2 }}>Tuning History</Typography>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Tuning Instance ID</TableCell>
              <TableCell>Action Name</TableCell>
              <TableCell>Workload ID</TableCell>
              <TableCell>State ID</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tuningInstances.map((tuningInstance) => (
              <TableRow
                key={tuningInstance.tuning_instance_id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component="th" scope="row">{tuningInstance.tuning_instance_id}</TableCell>
                <TableCell>{tuningInstance.action_name}</TableCell>
                <TableCell>{tuningInstance.workload_id}</TableCell>
                <TableCell>{tuningInstance.state_id}</TableCell>
                <TableCell>{tuningInstance.status}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Box sx={{ m: 1, mt: 4 }}>
        <Typography variant="h6">Tune Database</Typography>
        {workloads &&
          <Box sx={{ display: 'flex', mt: 4 }}>
            <Typography sx={{ mr: 3 }}>
              Workload ID
            </Typography>
            <FormControl variant="standard" sx={{ top: -4, minWidth: 120 }}>
              <Select
                labelId="demo-simple-select-filled-label"
                id="demo-simple-select-filled"
                value={selctedWorkloadId}
                onChange={handleSelectedWorkloadIdChange}
              >
                {workloads.map((workload) => (
                  <MenuItem key={workload.resource_id} value={workload.resource_id}>{workload.resource_id}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        }
        {states &&
          <Box sx={{ display: 'flex', mt: 4 }}>
            <Typography sx={{ mr: 3 }}>
              State ID
            </Typography>
            <FormControl variant="standard" sx={{ top: -4, minWidth: 120 }}>
              <Select
                labelId="demo-simple-select-filled-label"
                id="demo-simple-select-filled"
                value={selectedStateId}
                onChange={handleSelectedStateIdChange}
              >
                {states && states.map((state) => (
                  <MenuItem key={state.resource_id} value={state.resource_id}>{state.resource_id}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>      
        }
        <LoadingButton
          variant="contained"
          startIcon={<LibraryAdd />}
          sx={{ mt: 4, '&.Mui-disabled': { bgcolor: '#a5d6a7' } }}
          onClick={handleTuneDatabase}
          loading={submitLoading}
          loadingPosition="start"
          disabled={submitSuccess}
        >
          Tune!
        </LoadingButton>
      </Box>
    </React.Fragment>
  )
}
