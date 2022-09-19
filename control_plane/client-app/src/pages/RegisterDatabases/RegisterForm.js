import { useReducer } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import FormHelperText from '@mui/material/FormHelperText';

import UploadFile from '@mui/icons-material/UploadFile';
import axios from '../../util/axios';

function RegisterForm({ environment }) {
  const [formInput, setFormInput] = useReducer(
    (state, newState) => ({ ...state, ...newState }),
    {
      environment: environment,
      primary_host: '',
      primary_ssh_port: '',
      primary_ssh_user: '',
      primary_pg_user: '',
      primary_pg_port: '',
      primary_key_file: null,
      replica_host: '',
      replica_ssh_port: '',
      replica_ssh_user: '',
      replica_pg_user: '',
      replica_pg_port: '',
      replica_key_file: null
    }
  );

  const handleSubmit = async e => {
    e.preventDefault();
    console.log(formInput);

    const formData = new FormData();
    Object.keys(formInput).forEach(key => {
      formData.append(key, formInput[key]);
    });
    
    try {
      const res = await axios.post('/database_manager/register/', formData)
      console.log(res);
    } catch (error) {
      console.error(error);
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

  return (
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
            id="primary-host"
            name="primary_host"
            label="Primary Host"
            variant="standard"
            onChange={handleInput}
          />
          <TextField
            required
            id="primary-ssh-port"
            name="primary_ssh_port"
            label="Primary SSH Port"
            variant="standard"
            onChange={handleInput}
          />
          <TextField
            required
            id="primary-ssh-user"
            name="primary_ssh_user"
            label="Primary SSH User"
            variant="standard"
            onChange={handleInput}
          />
          <TextField
            required
            id="primary-pg-user"
            name="primary_pg_user"
            label="Primary Postgres User"
            variant="standard"
            onChange={handleInput}
          />
          <TextField
            required
            id="primary-pg-port"
            name="primary_pg_port"
            label="Primary Postgres Port"
            variant="standard"
            onChange={handleInput}
          />
          <Button variant="contained" component="label" sx={{ m: 1, mt: 2 }}>
            <UploadFile />
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
            onChange={handleInput}
          />
          <TextField
            required
            id="replica-ssh-port"
            name="replica_ssh_port"
            label="Replica SSH Port"
            variant="standard"
            onChange={handleInput}
          />
          <TextField
            required
            id="replica-ssh-user"
            name="replica_ssh_user"
            label="Replica SSH User"
            variant="standard"
            onChange={handleInput}
          />
          <TextField
            required
            id="replica-pg-user"
            name="replica_pg_user"
            label="Replica Postgres User"
            variant="standard"
            onChange={handleInput}
          />
          <TextField
            required
            id="replica-pg-port"
            name="replica_pg_port"
            label="Replica Postgres Port"
            variant="standard"
            onChange={handleInput}
          />
          <Button variant="contained" component="label" sx={{ m: 1, mt: 2 }}>
            <UploadFile />
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
          <Button variant="contained" color="secondary" type="submit" size="large">
            Register
          </Button>
        </Grid>
      </Grid>
    </Box>
  )
}

export default RegisterForm;
