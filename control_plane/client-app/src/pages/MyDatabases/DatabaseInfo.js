import { Link } from 'react-router-dom';
import Card from '@mui/material/Card';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import DatabaseRegisterState from '../../util/databaseRegisterState';
import parseDateTime from '../../util/parseDateTime';
import postgresLogo from './postgres.png';

export default function DatabaseInfo(props) {
  const { databaseInfo: info } = props;

  const getStateColor = (state) => {
    switch (DatabaseRegisterState[state]) {
      case DatabaseRegisterState.HEALTHY:
        return 'success.main';
      case DatabaseRegisterState.UNHEALTHY:
        return 'error';
      default:
        return 'warning.light';
    }
  }

  return (
    <Card sx={{ minWidth: 275, mb: 4, p: 1, display: 'flex', alignItems: 'center' }}>
      <img
        src={postgresLogo}
        alt="pg-logo"
        style={{ width: '100px', height: '100px', paddingLeft: '24px', objectFit: 'contain' }}
      />
      <Grid container spacing={2} alignItems="center" sx={{ p: 2, px: 3 }} >
        <Grid item xs={12} md={9}>
          <Typography variant="h4" pt={1}>Database ID: {info.database_id}</Typography>
        </Grid>
        <Grid item xs={12} md={3}>
          <Typography variant="h6" sx={{ display: 'inline-block' }}>State: &nbsp;</Typography>
          <Typography variant="h6" sx={{ display: 'inline-block' }} color={getStateColor(info.state)}>{DatabaseRegisterState[info.state]}</Typography>
        </Grid>
        <Grid item xs={12} md={9}>
          <Link to={`/databases/${info.database_id}`}>
            <Button sx={{ pt: 0 }}>Manage</Button>
          </Link>
        </Grid>
        <Grid item xs={12} md={3}>
          <Typography sx={{ fontSize: '0.9rem', pt: 0 }}>Created At: {parseDateTime(info.created)}</Typography>
        </Grid>
      </Grid>
    </Card>
  );
}
