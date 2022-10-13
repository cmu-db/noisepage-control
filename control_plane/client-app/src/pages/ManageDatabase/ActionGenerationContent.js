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

export default function ActionGenerationContent({ databaseId }) {
  const [actions, setActions] = useState();
  const [workloads, setWorkloads] = useState();
  const [states, setStates] = useState();
  const [selctedWorkloadId, setSelectedWorkloadId] = useState('');
  const [selectedStateId, setSelectedStateId] = useState('');
  
  const [submitLoading, setSubmitLoading] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  
  // TODO: move api calls to a separate file
  useEffect(() => {
    async function fetchActions() {
      try {
        const res = await axios.get(`/database_manager/databases/${databaseId}/actions`);
        console.log(res);
        setActions(res.data);  
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

    fetchActions();
    fetchWorkloads();
    fetchStates();
  }, [databaseId]);

  const handleGenerateAction = async (event) => {
    // if (!selctedWorkloadId || !selectedStateId) {
    //   return;
    // }

    event.preventDefault();
    console.log(`Submit generate action`);
    setSubmitLoading(true);

    try {
      const res = await axios.post(
        `/database_manager/databases/${databaseId}/actions`,
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

  return actions && (
    <React.Fragment>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Action ID</TableCell>
              <TableCell>Action Name</TableCell>
              <TableCell>Workload ID</TableCell>
              <TableCell>State ID</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {actions.map((action) => (
              <TableRow
                key={action.action_id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {action.available
                    ?
                    <Link href={`${axios.defaults.baseURL}/database_manager/action/${action.action_id}`} underline="always">
                      {action.action_id}
                    </Link>
                    :
                    action.action_id
                  }
                </TableCell>
                <TableCell>{action.action_name}</TableCell>
                <TableCell>{action.workload_id}</TableCell>
                <TableCell>{action.action_id}</TableCell>
                <TableCell>{action.available ? 'Available' : 'Generating'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Box sx={{ m: 1, mt: 4 }}>
        <Typography variant="h6">Generate New Action</Typography>
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
                value={selctedWorkloadId}
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
          onClick={handleGenerateAction}
          loading={submitLoading}
          loadingPosition="start"
          disabled={submitSuccess}
        >
          Generate Action!
        </LoadingButton>
      </Box>
    </React.Fragment>
  )
}
