import * as React from 'react';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Input from '@mui/material/Input';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import { styled } from "@mui/material/styles";
import WorkloadChart from './WorkloadChart';
import axios from '../../util/axios';

const PrimaryToggleButton = styled(ToggleButton)({
  "&.Mui-selected, &.Mui-selected:hover": {
    backgroundColor: 'rgba(0, 155, 229, 0.25)'
  }
});

export default function TuneDatabaseContent() {
  const { id: databaseId } = useParams();
  const [workloads, setWorkloads] = useState();
  const [chartMetricType, setChartMetricType] = useState('num_queries');
  const [selectedWorkloadRange, setSelectedWorkloadRange] = useState();
  const [modalOpen, setModalOpen] = useState(false);
  const [allowedActions, setAllowedActions] = useState([]);
  const [tuningTimeout, setTuningTimeout] = useState(60);
  const [tuningName, setTuningName] = useState('My Tuning Session');
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

  const handleAllowedActionChange = (event, newAllowedActions) => {
    setAllowedActions(newAllowedActions);
  };

  const handleTuningTimeoutChange = (event) => {
    setTuningTimeout(Number(event.target.value));
  };

  const handleTuningNameChange = (event) => {
    setTuningName(event.target.value);
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
    if (metricType) {
      setChartMetricType(metricType);
    }
  };

  const handleModalOpen = () => setModalOpen(true);
  const handleModalClose = () => setModalOpen(false);

  return workloads && (
    <React.Fragment>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={4}></Grid>
        <Grid item xs={4}>
          <Typography variant="h6" component="div" align='center'>
            Select a Target Workload Range:
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

      <WorkloadChart workloads={workloads} metricType={chartMetricType} setSelectedWorkloadRange={setSelectedWorkloadRange}/>

      <Box sx={{ m: 3 }} align="center">
        <Button
          variant="contained"
          startIcon={<LibraryAdd />}
          // sx={{ '&.Mui-disabled': { bgcolor: 'primary.light' } }}
          onClick={handleModalOpen}
          disabled={!selectedWorkloadRange}
        >
          Tune!
        </Button>
      </Box>
      {/* The Tuning Parameter Modal */}
      <Dialog open={modalOpen} onClose={handleModalClose}>
        <DialogTitle>Gym Parameters</DialogTitle>
        <Divider />
        <DialogContent>
          <Typography>
            Target Workload Range:
          </Typography>
          <Typography mb={2}>
            {selectedWorkloadRange && `${selectedWorkloadRange[0]} ~ ${selectedWorkloadRange[1]}`}
          </Typography>
          <Typography>
            Allowed Actions:
          </Typography>
          <ToggleButtonGroup
            value={allowedActions}
            onChange={handleAllowedActionChange}
            size={'small'}
            sx={{ marginLeft: 'auto', mb: 2, '&.Mui-selected': {bgcolor: 'rgba(0, 155, 229)'} }}
            color='primary'
          >
            <PrimaryToggleButton value="add_index">
              Add indexes
            </PrimaryToggleButton>
            <PrimaryToggleButton value="drop_index">
              Drop indexes
            </PrimaryToggleButton>
            <PrimaryToggleButton value="non-restart-knob">
              Non-restart knobs
            </PrimaryToggleButton>
            <PrimaryToggleButton value="restart-knob">
              Restart knobs
            </PrimaryToggleButton>
          </ToggleButtonGroup>
          <Typography>
            Tuning Timeout (Seconds):
          </Typography>
          <Input
            value={tuningTimeout}
            size="small"
            onChange={handleTuningTimeoutChange}
            inputProps={{
              step: 10,
              min: 0,
              type: 'number',
            }}
            sx={{ mb: 2 }}
          />
          <Typography>
            Tuning Name:
          </Typography>
          <TextField
            id="name"
            variant="standard"
            value={tuningName}
            onChange={handleTuningNameChange}
          />
          <Typography variant="caption" color={'GrayText'} display="block" gutterBottom>
            This name will be used to identify the tuning result.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleModalClose}>Cancel</Button>
          <Button onClick={handleModalClose}>Tune</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  )
}
