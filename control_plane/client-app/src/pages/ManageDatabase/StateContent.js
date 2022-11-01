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
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import Done from '@mui/icons-material/Done';
import axios from '../../util/axios';
import parseDateTime from '../../util/parseDateTime';

export default function StateContent({ databaseId }) {
  const [states, setStates] = useState();
  const [friendlyName, setFriendlyName] = useState('');
  const [stateSubmitLoading, setStateSubmitLoading] = useState(false);
  const [stateSubmitSuccess, setStateSubmitSuccess] = useState(false);
  
  useEffect(() => {
    async function fetchStates() {
      try {
        const res = await axios.get(`/database_manager/databases/${databaseId}/states`);
        console.log(res);
        setStates(res.data);  
      } catch (error) {
        console.error(error)
      }
    }
    fetchStates();
  }, [databaseId]);

  const handleFriendlyNameInputChange = (event) => {
    setFriendlyName(event.target.value);
  };

  const handleCollectState = async (event) => {
    event.preventDefault();
    console.log(`Submit collect state`);
    setStateSubmitLoading(true);

    try {
      const body = { friendly_name: friendlyName };
      const res = await axios.post(`/database_manager/databases/${databaseId}/states`, body);
      console.log(res);
      setStateSubmitSuccess(true);
      window.location.reload();
    } catch (error) {
      console.error(error);
    } finally {
      setStateSubmitLoading(false);
    }
  };

  return states && (
    <React.Fragment>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Friendly Name</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Collected At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {states.map((state) => (
              <TableRow
                key={state.resource_id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell>{state.friendly_name}</TableCell>
                <TableCell>
                  {state.available
                    ?
                    <Link href={`${axios.defaults.baseURL}/database_manager/state/${state.resource_id}`} underline="always">
                      Available
                    </Link>
                    : 'Collecting'
                  }
                </TableCell>
                <TableCell>{parseDateTime(state.collected_at)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Box sx={{ m: 1, mt: 4 }}>
        <Typography variant="h6">Collect a New State</Typography>
        <Box sx={{ display: 'flex', mt: 3 }}>
          <Typography sx={{ mr: 1, mt: 0.4 }}>
            Friendly Name:
          </Typography>
          <TextField
            required
            id="state-friendly-name"
            variant="standard"
            onChange={handleFriendlyNameInputChange}
          />
        </Box>
        <LoadingButton
          variant="contained"
          startIcon={stateSubmitSuccess ? <Done /> : <LibraryAdd />}
          sx={{ mt: 4, '&.Mui-disabled': { bgcolor: '#a5d6a7' } }}
          onClick={handleCollectState}
          loading={stateSubmitLoading}
          loadingPosition="start"
          disabled={stateSubmitSuccess}
        >
          Collect!
        </LoadingButton>
      </Box>
    </React.Fragment>
  )
}
