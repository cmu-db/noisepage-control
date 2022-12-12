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
import LoadingButton from '@mui/lab/LoadingButton';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import PlayCircleIcon from '@mui/icons-material/PlayCircle';
import TaskAltIcon from '@mui/icons-material/TaskAlt';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import CancelIcon from '@mui/icons-material/Cancel';
import CircularProgress from '@mui/material/CircularProgress';
import axios from '../../util/axios';
import parseDateTime from '../../util/parseDateTime';

const TUNING_INSTANCES = [
  {
    "tuning_instance_id": 1,
    "friendly_name": "2022-12-06 07:23:00 PM",
    "status": "RUNNING",
    "started_at": "2022-12-06T19:23:00.000Z",
    "duration": "-"
  },
  {
    "tuning_instance_id": 2,
    "friendly_name": "Optimize for 11/15 evening request spike",
    "status": "FINISHED",
    "started_at": "2022-11-17T06:03:12.000Z",
    "duration": "3",
  }
];

const ACTIONS = [
  {
    "tuning_action_id": 1,
    "type": "Add Index",
    "command": "CREATE INDEX idx_review_rating_uid ON review_rating (u_id);",
    "status": "Applied",
    "benefit": 100,
    "reboot_required": false,
  },
  {
    "tuning_action_id": 2,
    "type": "Add Index",
    "command": "CREATE INDEX idx_trust_sid ON trust (source_u_id);",
    "status": "NOT_APPLIED",
    "benefit": 200,
    "reboot_required": false,
  },
  {
    "tuning_action_id": 3,
    "type": "Restart Knob",
    "command": "ALTER SYSTEM SET shared_buffers TO '4GB';",
    "status": "NOT_APPLIED",
    "benefit": 500,
    "reboot_required": true,
  },
  {
    "tuning_action_id": 4,
    "type": "Non-Restart Knob",
    "command": "ALTER SYSTEM SET effective_cache_size = '8GB';",
    "status": "NOT_APPLIED",
    "benefit": 500,
    "reboot_required": false,
  },
];

function ActionRow({ action }) {
  const [modalOpen, setModalOpen] = useState(false);
  const [actionSent, setActionSent] = useState(false);

  const handleApplyAction = async (event) => {
    event.preventDefault();
    setActionSent(true);
    handleModalClose();

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

  const handleModalOpen = () => setModalOpen(true);
  const handleModalClose = () => setModalOpen(false);

  const notApplied = (action) => action.status === 'NOT_APPLIED';

  return (
    <React.Fragment>
      <TableRow key={action.tuning_action_id} sx={{ '&:last-child td': {borderBottom: 'unset'}}}>
        <TableCell>{action.type}</TableCell>
        <TableCell>{action.command}</TableCell>
        <TableCell align="center">{action.benefit}</TableCell>
        <TableCell align="center">{String(action.reboot_required)}</TableCell>
        <TableCell align="center">
          <Button
            color="success"
            variant="contained"
            // TODO: remove the actionSent hack
            startIcon={actionSent ? <CircularProgress disableShrink size={15} sx={{ opacity: 0.5, color: '#2e7d32' }} />
              : notApplied(action) ? <PlayCircleIcon />
              : <TaskAltIcon />
            }
            sx={{
              my: 2,
              // '&.Mui-disabled': {
              //   bgcolor: '#f6685e',
              //   color: 'white',
              //   opacity: '0.9'
              // },
              // backgroundColor: '#f44336',
              width: '100px'
            }}
            // onClick={e => handleApplyAction(e, action.tuning_action_id)}
            onClick={handleModalOpen}
            disabled={!notApplied(action) || actionSent}
          >
            {/* {notApplied(action) ? 'Apply!' : action.status} */}
            {/* TODO: remove the actionSent hack */}
            {actionSent ? 'Applying' : notApplied(action) ? 'Apply!' : action.status}
          </Button>
        </TableCell>
      </TableRow>
      <Dialog open={modalOpen} onClose={handleModalClose}>
        <DialogTitle>Apply Action</DialogTitle>
        <Divider />
        <DialogContent>
          <Typography variant="h6">
            Do you confirm to apply this action?
          </Typography>
          <Typography mb={1} mt={2}>
            {action.command}
          </Typography>
        </DialogContent>
        <DialogActions sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
          <Button
            color="error"
            sx={{ width: '100px' }}
            variant="outlined"
            startIcon={<CancelIcon />}
            onClick={handleModalClose}
          >
            Cancel
          </Button>
          <LoadingButton
            color="success"
            sx={{ width: '100px' }}
            variant="contained"
            startIcon={<PlayCircleIcon />}
            onClick={handleApplyAction}
          >
            Apply!
          </LoadingButton>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}

function TuningInstanceRow({ databaseId, tuningInstance, parseDateTime }) {
  const [actions, setActions] = useState();
  const [open, setOpen] = useState(false);
  // const [actionSent, setActionSent] = useState({});

  async function fetchActions() {
    try {
      const res = await axios.get(
        `/database_manager/databases/${databaseId}/actions?tuning_instance_id=${tuningInstance.tuning_instance_id}`
      );
      console.log(res);
      setActions(res.data);

      // Reset actionSent
      // const newActionSent = {};
      // res.data.forEach(action => {
      //   newActionSent[action.tuning_action_id] = false;
      // });
      // setActionSent(newActionSent);
    } catch (error) {
      console.error(error)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case "RUNNING":
        return 'warning.light';
      case "FINISHED":
        return 'success.main';
    }
  }

  // useInterval(fetchActions, 2000);

  return (
    <React.Fragment>
      <TableRow>
        <TableCell>{tuningInstance.friendly_name}</TableCell>
        <TableCell>
          {tuningInstance.status === 'RUNNING' && <CircularProgress disableShrink size={15} sx={{ mr: 1, opacity: 0.5, color: '#2e7d32' }} />}
          <Typography variant='p' color={getStatusColor(tuningInstance.status)}>{tuningInstance.status}</Typography>
        </TableCell>
        <TableCell>{parseDateTime(tuningInstance.started_at)}</TableCell>
        <TableCell>{tuningInstance.duration}</TableCell>
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
                    <TableCell>Action Type</TableCell>
                    <TableCell>SQL Statement</TableCell>
                    <TableCell align="center">Expected Benefit</TableCell>
                    <TableCell align="center">Reboot Required</TableCell>
                    <TableCell align="center">Apply</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {ACTIONS && ACTIONS.map((action) => (
                    <ActionRow key={action.tuning_action_id} action={action}/>
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
              <TableCell>Duration (minute)</TableCell>
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
