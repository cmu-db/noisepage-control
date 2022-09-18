import Input from '@mui/material/Input';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import { Typography } from '@mui/material';

function RegisterForm() {
  return (
    <Box
      component="form"
      sx={{
        '& .MuiTextField-root': { m: 1, width: '25ch' },
        '& .MuiTypography-root': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <Grid container>
        <Grid item xs={12} sm={4}>
          <Typography variant="h5">Primary Database</Typography>
          <TextField
            required
            id="primary-host"
            label="Primary Host"
            variant="standard"
          />
          <TextField
            required
            id="primary-ssh-port"
            label="Primary SSH Port"
            variant="standard"
          />
          <TextField
            required
            id="primary-ssh-user"
            label="Primary SSH User"
            variant="standard"
          />
          <TextField
            required
            id="primary-pg-user"
            label="Primary Postgres User"
            variant="standard"
          />
          <TextField
            required
            id="primary-pg-port"
            label="Primary Postgres Port"
            variant="standard"
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <Typography variant="h5">Replica Database</Typography>
          <TextField
            required
            id="replica-host"
            label="Replica Host"
            variant="standard"
          />
          <TextField
            required
            id="replica-ssh-port"
            label="Replica SSH Port"
            variant="standard"
          />
          <TextField
            required
            id="replica-ssh-user"
            label="Replica SSH User"
            variant="standard"
          />
          <TextField
            required
            id="replica-pg-user"
            label="Replica Postgres User"
            variant="standard"
          />
          <TextField
            required
            id="replica-pg-port"
            label="Replica Postgres Port"
            variant="standard"
          />
        </Grid>
        <Grid item xs={12} sx={{ p: 1, py: 3 }}>
          <Button variant="contained" color="primary" type="submit" size="large">
            Register
          </Button>
        </Grid>
      </Grid>
    </Box>
  )
}

export default RegisterForm;
