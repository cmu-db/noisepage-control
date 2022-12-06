import * as React from 'react';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import useInterval from 'react-useinterval';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Collapse from '@mui/material/Collapse';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import LibraryAdd from '@mui/icons-material/LibraryAdd';
import DoneOutlineIcon from '@mui/icons-material/DoneOutline';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import CircularProgress from '@mui/material/CircularProgress';
import axios from '../../util/axios';
import parseDateTime from '../../util/parseDateTime';

const TUNING_INSTANCES = [
  {
    "tuning_instance_id": 1,
    "friendly_name": "My Tuning Session",
    "status": "RUNNING",
    "started_at": "2021-12-06T19:23:00.000Z",
  },
  {
    "tuning_instance_id": 2,
    "friendly_name": "Optimize for 11/15 evening request spike",
    "status": "FINISHED",
    "started_at": "2021-11-17T06:03:12.000Z",
  }
]

const ACTIONS = [
  {
    "tuning_action_id": 1,
    "command": "CREATE INDEX idx_review_rating_uid ON review_rating (u_id);",
    "status": "NOT_APPLIED",
    "benefit": 100,
    "reboot_required": false,
  },
  {
    "tuning_action_id": 2,
    "command": "CREATE INDEX idx_trust_sid ON trust (source_u_id);",
    "status": "NOT_APPLIED",
    "benefit": 200,
    "reboot_required": false,
  },
  {
    "tuning_action_id": 3,
    "command": "ALTER SYSTEM SET shared_buffers TO '400MB';",
    "status": "NOT_APPLIED",
    "benefit": 500,
    "reboot_required": true,
  },
]

function TuningInstanceRow({ databaseId, tuningInstance, parseDateTime }) {
  const [actions, setActions] = useState();
  const [open, setOpen] = useState(false);
  const [actionSent, setActionSent] = useState({});

  async function fetchActions() {
    try {
      const res = await axios.get(
        `/database_manager/databases/${databaseId}/actions?tuning_instance_id=${tuningInstance.tuning_instance_id}`
      );
      console.log(res);
      setActions(res.data);

      // Reset actionSent
      const newActionSent = {};
      res.data.forEach(action => {
        newActionSent[action.tuning_action_id] = false;
      });
      setActionSent(newActionSent);
    } catch (error) {
      console.error(error)
    }
  }

  // useInterval(fetchActions, 2000);

  const handleApplyAction = async (event, tuningActionId) => {
    event.preventDefault();
    // setActionSent({ ...actionSent, [tuningActionId]: true });

    // console.log("Submit apply action", tuningActionId);
    // try {
    //   const res = await axios.post(
    //     `/database_manager/action/apply/${tuningActionId}`
    //   );
    //   console.log(res);
    // } catch (error) {
    //   console.error(error)
    // }
  }

  const notApplied = (action) => action.status === 'NOT_APPLIED';

  return (
    <React.Fragment>
      <TableRow>
        <TableCell>{tuningInstance.friendly_name}</TableCell>
        <TableCell>
          {tuningInstance.status === 'RUNNING' && <CircularProgress disableShrink size={15} sx={{ mr: 1 }} />}
          <Typography variant='p'>{tuningInstance.status}</Typography>
        </TableCell>
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
      <TableRow>
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
                  {ACTIONS && ACTIONS.map((action) => (
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
                          onClick={e => handleApplyAction(e, action.tuning_action_id)}
                          disabled={!notApplied(action) || actionSent[action.tuning_action_id]}
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

export default function TuningHistoryContent() {
  const { id: databaseId } = useParams();
  const [tuningInstances, setTuningInstances] = useState();
  
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

    // fetchTuningInstances();
  }, [databaseId]);

  return TUNING_INSTANCES && (
    <React.Fragment>
      <Typography variant="h6" sx={{ mx: 1, mb: 2 }}>Tuning History</Typography>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Started At</TableCell>
              <TableCell></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {TUNING_INSTANCES.sort((a, b) => new Date(b.started_at) - new Date(a.started_at)).map((tuningInstance) => (
              <TuningInstanceRow
                key={tuningInstance.tuning_instance_id}
                databaseId={databaseId}
                tuningInstance={tuningInstance}
                parseDateTime={parseDateTime}
              />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </React.Fragment>
  )
}
