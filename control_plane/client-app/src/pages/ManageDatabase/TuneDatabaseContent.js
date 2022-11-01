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
import Collapse from '@mui/material/Collapse';
import LoadingButton from '@mui/lab/LoadingButton';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import DoneOutlineIcon from '@mui/icons-material/DoneOutline';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import axios from '../../util/axios';
import parseDateTime from '../../util/parseDateTime';

function TuningInstanceRow({ databaseId, tuningInstance, getWorkloadName, getStateName, parseDateTime }) {
  const [actions, setActions] = useState();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    async function fetchActions() {
      try {
        const res = await axios.get(
          `/database_manager/databases/${databaseId}/actions?tuning_instance_id=${tuningInstance.tuning_instance_id}`
        );
        console.log(res);
        setActions(res.data);  
      } catch (error) {
        console.error(error)
      }
    }
    fetchActions();
  }, [databaseId, tuningInstance.tuning_instance_id]);

  const notApplied = (action) => action.status === 'NOT_APPLIED';

  return (
    <React.Fragment>
      <TableRow
        // sx={{ '& > *': { border: 0 } }}
      >
        {/* <TableCell component="th" scope="row">{tuningInstance.tuning_instance_id}</TableCell> */}
        <TableCell>{tuningInstance.friendly_name}</TableCell>
        <TableCell>{getWorkloadName(tuningInstance.workload_id)}</TableCell>
        <TableCell>{getStateName(tuningInstance.state_id)}</TableCell>
        <TableCell>{tuningInstance.status}</TableCell>
        <TableCell>{parseDateTime(tuningInstance.started_at)}</TableCell>
        <TableCell>
          {tuningInstance.status === 'FINISHED' &&
            <IconButton
              aria-label="expand row"
              size="small"
              onClick={() => setOpen(!open)}
            >
              {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
            </IconButton>
          }
        </TableCell>
      </TableRow>
      <TableRow
        // sx={{ '& > td': {borderBottom: 'unset'} }}
      >
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              <Typography variant="h6" gutterBottom component="div" sx={{ my: 2 }}>
                Recommended Actions
              </Typography>
              <Table size="small" aria-label="actions">
                <TableHead>
                  <TableRow>
                    <TableCell>SQL statement</TableCell>
                    <TableCell align="center">Expected benefit</TableCell>
                    <TableCell align="center">Reboot required</TableCell>
                    <TableCell align="center">Apply</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {actions && actions.map((action) => (
                    <TableRow key={action.tuning_action_id} sx={{ '&:last-child td': {borderBottom: 'unset'}}}>
                      <TableCell>
                        {action.command}
                      </TableCell>
                      <TableCell align="center">{action.benefit}</TableCell>
                      <TableCell align="center">{String(action.reboot_required)}</TableCell>
                      <TableCell align="center">
                        <Button
                          variant="contained"
                          startIcon={notApplied(action) ? <LibraryAdd /> : <DoneOutlineIcon />}
                          sx={{ my: 2, '&.Mui-disabled': { bgcolor: '#f6685e' }, backgroundColor: '#f44336' }}
                          // onClick={handleApplyAction}
                          disabled={!notApplied(action)}
                        >
                          {notApplied(action) ? 'Apply!' : action.status}
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>

  )
}

export default function TuneDatabaseContent({ databaseId }) {
  const [tuningInstances, setTuningInstances] = useState();
  const [workloads, setWorkloads] = useState();
  const [states, setStates] = useState();
  const [selectedWorkloadId, setSelectedWorkloadId] = useState('');
  const [selectedStateId, setSelectedStateId] = useState('');
  const [friendlyName, setFriendlyName] = useState('');
  
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
    if (!selectedWorkloadId || !selectedStateId) {
      return;
    }

    event.preventDefault();
    console.log(`Submit tune database`);
    setSubmitLoading(true);

    try {
      const body = {
        workload_id: selectedWorkloadId,
        state_id: selectedStateId,
        friendly_name: friendlyName,
      }
      const res = await axios.post(
        `/database_manager/databases/${databaseId}/tune`,
        body
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

  const handleFriendlyNameInputChange = (event) => {
    setFriendlyName(event.target.value);
  };

  const getWorkloadName = (workloadId) => {
    return workloads && workloads.find(w => w.resource_id === workloadId).friendly_name;
  };

  const getStateName = (stateId) => {
    return states && states.find(w => w.resource_id === stateId).friendly_name;
  };

  return tuningInstances && (
    <React.Fragment>
      <Typography variant="h6" sx={{ mx: 1, mb: 2 }}>Tuning History</Typography>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Friendly Name</TableCell>
              <TableCell>Workload Name</TableCell>
              <TableCell>State Name</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Started At</TableCell>
              <TableCell></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tuningInstances.sort((a, b) => new Date(b.started_at) - new Date(a.started_at)).map((tuningInstance) => (
              <TuningInstanceRow
                key={tuningInstance.tuning_instance_id}
                databaseId={databaseId}
                tuningInstance={tuningInstance}
                getWorkloadName={getWorkloadName}
                getStateName={getStateName}
                parseDateTime={parseDateTime}
              />
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
                value={selectedWorkloadId}
                onChange={handleSelectedWorkloadIdChange}
              >
                {workloads.map((workload) => (
                  <MenuItem key={workload.resource_id} value={workload.resource_id}>{getWorkloadName(workload.resource_id)}</MenuItem>
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
                  <MenuItem key={state.resource_id} value={state.resource_id}>{getStateName(state.resource_id)}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>      
        }
        <Box sx={{ display: 'flex', mt: 3 }}>
          <Typography sx={{ mr: 1, mt: 0.4 }}>
            Friendly Name:
          </Typography>
          <TextField
            required
            id="tune-friendly-name"
            variant="standard"
            onChange={handleFriendlyNameInputChange}
          />
        </Box>
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
