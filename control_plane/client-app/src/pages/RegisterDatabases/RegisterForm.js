import { useState, useReducer } from 'react';
import { Navigate } from 'react-router-dom';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import LoadingButton from '@mui/lab/LoadingButton';
import Typography from '@mui/material/Typography';
import FormHelperText from '@mui/material/FormHelperText';
import UploadFile from '@mui/icons-material/UploadFile';
import Send from '@mui/icons-material/Send';
import Done from '@mui/icons-material/Done';
import axios from '../../util/axios';

function RegisterForm({ environment }) {
  const [formInput, setFormInput] = useReducer(
    (state, newState) => ({ ...state, ...newState }),
    {
      environment: environment,
      db_name: 'postgres',
      primary_host: 'ec2-54-242-174-185.compute-1.amazonaws.com',
      primary_ssh_port: '22',
      primary_ssh_user: 'ubuntu',
      primary_pg_user: 'postgres',
      primary_pg_port: '10000',
      primary_key_file: null,
      replica_host: 'ec2-54-226-115-17.compute-1.amazonaws.com',
      replica_ssh_port: '22',
      replica_ssh_user: 'ubuntu',
      replica_pg_user: 'postgres',
      replica_pg_port: '10001',
      replica_key_file: null
    }
  );
  const [registerLoading, setRegisterLoading] = useState(false);
  const [registerSuccess, setRegisterSuccess] = useState(false);
  const [formSubmitted, setFormSubmitted] = useState(false);

  const handleSubmit = async e => {
    e.preventDefault();
    console.log(formInput);
    setRegisterLoading(true);

    const formData = new FormData();
    Object.keys(formInput).forEach(key => {
      formData.append(key, formInput[key]);
    });
    
    try {
      const res = await axios.post('/database_manager/register/', formData)
      console.log(res);
      setRegisterSuccess(true);
      setFormSubmitted(true);
    } catch (error) {
      console.error(error);
    } finally {
      setRegisterLoading(false);
    }
  }

  const handleInput = e => {
    const name = e.target.name;
    const newValue = e.target.value;
    setFormInput({ [name]: newValue });
  }

  const handleUpload = e => {
    const name = e.target.name;
    const file = e.target.files[0];
    setFormInput({ [name]: file });
  }

  return formSubmitted ? <Navigate replace to="/databases" /> : (
    <Box
      component="form"
      sx={{
        '& .MuiTextField-root': { m: 1, width: '25ch' },
        '& .MuiTypography-root': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
      onSubmit={handleSubmit}
    >
      <Grid container>
        <Grid item xs={12} sm={4}>
          <Typography variant="h5">Primary Database</Typography>
          <TextField
            required
            id="db-name"
            name="db_name"
            label="Database Name"
            variant="standard"
            defaultValue="postgres"
            onChange={handleInput}
          />
          <TextField
            required
            id="primary-host"
            name="primary_host"
            label="Primary Host"
            variant="standard"
            defaultValue="ec2-54-242-174-185.compute-1.amazonaws.com"
            onChange={handleInput}
          />
          <TextField
            required
            id="primary-ssh-port"
            name="primary_ssh_port"
            label="Primary SSH Port"
            variant="standard"
            defaultValue="22"
            onChange={handleInput}
          />
          <TextField
            required
            id="primary-ssh-user"
            name="primary_ssh_user"
            label="Primary SSH User"
            variant="standard"
            defaultValue="ubuntu"
            onChange={handleInput}
          />
          <TextField
            required
            id="primary-pg-user"
            name="primary_pg_user"
            label="Primary Postgres User"
            variant="standard"
            defaultValue="postgres"
            onChange={handleInput}
          />
          <TextField
            required
            id="primary-pg-port"
            name="primary_pg_port"
            label="Primary Postgres Port"
            variant="standard"
            defaultValue="10000"
            onChange={handleInput}
          />
          <Button variant="contained" component="label" startIcon={<UploadFile />} sx={{ m: 1, mt: 2 }}>
            Upload Primary Key
            <input type="file" name="primary_key_file" hidden onChange={handleUpload}/>
          </Button>
          {
            formInput.primary_key_file
              ? <FormHelperText sx={{ m: 1 }} variant="body1">{formInput.primary_key_file.name}</FormHelperText>
              : <FormHelperText sx={{ m: 1 }} error variant="body1">No file selected</FormHelperText>
          }
        </Grid>
        <Grid item xs={12} sm={4}>
          <Typography variant="h5">Replica Database</Typography>
          <TextField
            required
            id="replica-host"
            name="replica_host"
            label="Replica Host"
            variant="standard"
            defaultValue="ec2-54-226-115-17.compute-1.amazonaws.com"
            onChange={handleInput}
          />
          <TextField
            required
            id="replica-ssh-port"
            name="replica_ssh_port"
            label="Replica SSH Port"
            variant="standard"
            defaultValue="22"
            onChange={handleInput}
          />
          <TextField
            required
            id="replica-ssh-user"
            name="replica_ssh_user"
            label="Replica SSH User"
            variant="standard"
            defaultValue="ubuntu"
            onChange={handleInput}
          />
          <TextField
            required
            id="replica-pg-user"
            name="replica_pg_user"
            label="Replica Postgres User"
            variant="standard"
            defaultValue="postgres"
            onChange={handleInput}
          />
          <TextField
            required
            id="replica-pg-port"
            name="replica_pg_port"
            label="Replica Postgres Port"
            variant="standard"
            defaultValue="10001"
            onChange={handleInput}
          />
          <Button variant="contained" component="label" startIcon={<UploadFile />} sx={{ m: 1, mt: 2 }}>
            Upload Replica Key
            <input type="file" name="replica_key_file" hidden onChange={handleUpload}/>
          </Button>
          {
            formInput.replica_key_file
              ? <FormHelperText sx={{ m: 1 }} variant="body1">{formInput.replica_key_file.name}</FormHelperText>
              : <FormHelperText sx={{ m: 1 }} error variant="body1">No file selected</FormHelperText>
          }
        </Grid>
        <Grid item xs={12} sx={{ p: 1, py: 3 }}>
          <LoadingButton
            variant="contained"
            color="secondary"
            startIcon={registerSuccess ? <Done /> : <Send />}
            type="submit"
            size="large"
            loading={registerLoading}
            loadingPosition="start"
            disabled={registerSuccess}
            sx={{ '&.Mui-disabled': { bgcolor: '#a5d6a7' } }}
          >
            Register
          </LoadingButton>
        </Grid>
      </Grid>
    </Box>
  )
}

export default RegisterForm;
