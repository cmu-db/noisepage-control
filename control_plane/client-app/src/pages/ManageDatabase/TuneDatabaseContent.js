import * as React from 'react';
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import LoadingButton from '@mui/lab/LoadingButton';
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
import BuildIcon from '@mui/icons-material/Build';
import CancelIcon from '@mui/icons-material/Cancel';
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
  const navigate = useNavigate();
  const [workloads, setWorkloads] = useState();
  const [chartMetricType, setChartMetricType] = useState('num_queries');
  const [selectedWorkloadRange, setSelectedWorkloadRange] = useState();
  const [modalOpen, setModalOpen] = useState(false);
  const [allowedActions, setAllowedActions] = useState(['add-index', 'drop-index', 'restart-knob', 'non-restart-knob']);
  const [maxTuningDuration, setMaxTuningDuration] = useState(3);
  const [tuningName, setTuningName] = useState('2022-12-06 07:23:00 PM');
  const [tuningSubmitLoading, setTuningSubmitLoading] = useState(false);

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
    setMaxTuningDuration(Number(event.target.value));
  };

  const handleTuningNameChange = (event) => {
    setTuningName(event.target.value);
  };

  const handleTuneDatabase = async (event) => {
    event.preventDefault();
    console.log(`Submit tune database`);
    setTuningSubmitLoading(true);

    // try {
    //   const body = {
    //     workload_id: selectedWorkloadId,
    //     state_id: selectedStateId,
    //     friendly_name: name,
    //   }
    //   const res = await axios.post(
    //     `/database_manager/databases/${databaseId}/tune`,
    //     body
    //   );
    //   console.log(res);
    //   setSubmitSuccess(true);
    //   window.location.reload();
    // } catch (error) {
    //   console.error(error);
    // } finally {
    //   setSubmitLoading(false);
    // }
    setTimeout(() => {
      setTuningSubmitLoading(false);
      handleModalClose();
      navigate('../tuning-history');  
    }, 2000);
  };

  const handleChartMetricToggle = (event, metricType) => {
    if (metricType) {
      setChartMetricType(metricType);
    }
  };

  const handleModalOpen = () => setModalOpen(true);
  const handleModalClose = () => setModalOpen(false);

  return workloads && (
    <React.Fragment>
      {/* Instructions */}
      <Box sx={{ px: 3, mb: 5 }}>
        <Typography variant="h5" fontWeight={500} align='center'>
          Instructions
        </Typography>
        <ol>
          <li>
            <Typography variant="p" align='left'>
              Select a target range of workloads which you want to optimize the database for, based on the past query rates or p99 latencies.
            </Typography>
          </li>
          <li>
            <Typography variant="p" align='left'>
              Click the tune button and specify the tuning parameters.
            </Typography>
          </li>
          <li>
            <Typography variant="p" align='left'>
              Wait for the tuning process to complete.
            </Typography>
          </li>
          <li>
            <Typography variant="p" align='left'>
              Once the tuning process is complete, you can view and apply the recommended actions
              in the Tuning History tab.
            </Typography>
          </li>
        </ol>
      </Box>

      <Grid container spacing={2} sx={{ mb: 1 }}>
        <Grid item xs={4}></Grid>
        <Grid item xs={4}>
          <Typography variant="h5" fontWeight={500} align='center'>
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

      <WorkloadChart workloads={workloads} metricType={chartMetricType} setSelectedWorkloadRange={setSelectedWorkloadRange}/>

      <Box sx={{ m: 3 }} align="center">
        <Button
          variant="contained"
          startIcon={<BuildIcon />}
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
            <PrimaryToggleButton value="add-index">
              Add indexes
            </PrimaryToggleButton>
            <PrimaryToggleButton value="drop-index">
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
            Max Tuning Duration (Minutes):
          </Typography>
          <Input
            value={maxTuningDuration}
            size="small"
            onChange={handleTuningTimeoutChange}
            inputProps={{
              step: 1,
              min: 1,
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
        <DialogActions sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
          <Button
            color="error"
            sx={{ width: '100px' }}
            variant="contained"
            startIcon={<CancelIcon />}
            onClick={handleModalClose}
          >
            Cancel
          </Button>
          <LoadingButton
            color="primary"
            sx={{ width: '100px' }}
            variant="contained"
            startIcon={<BuildIcon />}
            loading={tuningSubmitLoading}
            onClick={handleTuneDatabase}
            disabled={tuningSubmitLoading}
          >
            Tune!
          </LoadingButton>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  )
}
