import * as React from 'react';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import LoadingButton from '@mui/lab/LoadingButton';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import WorkloadChart from './WorkloadChart';
import axios from '../../util/axios';

export default function TuneDatabaseContent() {
  const { id: databaseId } = useParams();
  const [workloads, setWorkloads] = useState();
  const [name, setName] = useState('');
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

  return workloads && (
    <React.Fragment>
      <Typography variant="h6" sx={{ mb: 3 }} align="center">Select a Target Workload Range</Typography>
      <WorkloadChart workloads={workloads}/>

      {/* <Box sx={{ m: 2 }} align="center">
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
      </Box> */}
      <Box sx={{ display: 'flex', m: 2 }}>
        <Typography sx={{ mr: 1, mt: 0.4 }}>
          Name:
        </Typography>
        <TextField
          required
          id="tune-name"
          variant="standard"
          onChange={handleNameInputChange}
        />
      </Box>
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
    </React.Fragment>
  )
}
