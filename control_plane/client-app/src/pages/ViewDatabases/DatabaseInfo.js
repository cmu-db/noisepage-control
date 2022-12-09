import { Link } from 'react-router-dom';
import Card from '@mui/material/Card';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import DatabaseRegisterState from '../../util/databaseRegisterState';
import parseDateTime from '../../util/parseDateTime';
import postgresLogo from './postgres.png';

// TODO: make these real
const databaseDetails = [
  {
    Name: 'Restaurant Ordering Website',
    Version: 'PostgreSQL 14.5',
    Size: '1.2 GB',
    CPU: 'Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz (2 cores)',
    Memory: '16.0 GB',
  },
  {
    Name: 'Analytic',
    Version: 'PostgreSQL 14.5',
    Size: '10.3 GB',
    CPU: 'Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz (2 cores)',
    Memory: '16.0 GB',
  }
];

export default function DatabaseInfo(props) {
  const { databaseInfo: info, index } = props;

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
          <Typography variant="h4" pt={1}>
            {/* TODO: uncoment this Database ID: {info.database_id} */}
            <Link to={`/databases/${info.database_id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
              {databaseDetails[index].Name}
            </Link>
          </Typography>
        </Grid>
        <Grid item xs={12} md={3}>
          <Typography variant="h6" sx={{ display: 'inline-block' }}>State: &nbsp;</Typography>
          <Typography variant="h6" sx={{ display: 'inline-block' }} color={getStateColor(info.state)}>{DatabaseRegisterState[info.state]}</Typography>
        </Grid>
        <Grid item xs={12} md={9}>
          <Grid container alignItems="center">
            <Grid item xs={9}>
              {
                Object.keys(databaseDetails[index]).map(key => {
                  if (key === 'Name') {
                    return null;
                  }
                  return (
                    <Typography variant="caption" color='GrayText' display="block">
                      {key}: {databaseDetails[index][key]}
                    </Typography>
                  )
                })
              }
            </Grid>
            <Grid item xs={3}>
              <Link to={`/databases/${info.database_id}`}>
                <Button variant="contained" >Manage</Button>
              </Link>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12} md={3}>
          <Typography sx={{ fontSize: '0.9rem', pt: 0 }}>Created At: {parseDateTime(info.created)}</Typography>
        </Grid>
      </Grid>
    </Card>
  );
}
